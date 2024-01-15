import argparse
import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import logging
from dtaidistance import dtw_ndim
from datetime import datetime
import numpy as np
# import shapely
from shapely.geometry import shape, Point, MultiPoint
from shapely import centroid
from geopy import distance
from threshold_utils import get_threshold_set_from_type


logging.basicConfig(filename='algorithm.log', filemode='a', format='%(levelname)s:%(message)s')
# debug rep changes
# 0 - den coherency neg
# 1 - den coherency pos
# 2 - not in the area
# 3 - rsu
# 4 - cam coherency NEG
# 5 - cam coherency pos
rep_changes = [0] * 6

def calculate_space_centroid(points):
    length = len(points)
    sum_lon = np.sum(points[:, 0])
    sum_lat = np.sum(points[:, 1])
    return sum_lon/length, sum_lat/length



def check_distance(den_pos, cam_pos, r=50):
    return distance.distance(den_pos, cam_pos).m <= r

def check_cam(denm, cams):
    count = 0
    for cam in cams:
        d = distance.distance(denm, cam).m <= 100
        if not d:
            count += 1
            break
    print(count)

def check_cov_intersection(geojson, point):
    """
    point: represents the position of the vehicle
    geojson: file containing the coverage area of the edge node
    """
    for feature in geojson['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return True
    return False

def find_similar_event(event_collector, event, thresholds_type='mean'):
    eventType, p, t = event
    time_threshold, radius = get_threshold_set_from_type(thresholds_type)[eventType]
    time_threshold = time_threshold * 1000 # from secs to millisecs
    for key in event_collector:
        time_centroid = event_collector[key]["time_centroid"]
        space_centroid = event_collector[key]["space_centroid"]
        # TODO how to deal with this distance: so far the threshold considered for DEN distance coherency is the same used for 
        # CAM coherency. We shouldd conduct a separate study that analyzes this.
        if event_collector[key]["eventType"] == eventType \
            and abs(time_centroid - t) <= time_threshold \
                and check_distance((p.y, p.x), (space_centroid.y, space_centroid.x), r=radius) :
            event_collector[key]["time_centroid"] = (event_collector[key]["time_centroid"] + t ) / 2
            event_collector[key]["space_centroid"] = centroid(MultiPoint([event_collector[key]["space_centroid"], p]))
            return key
    return None


def compare_with_rsu(den):
    """
        This method returns True if the data received from that vehicle
        match with data provided by the RSU
    """
    return True

def normalize(x):
    # nomralization mapping
    # from [-1,1] ([a,b]) to [0,1] ([c,d])
    # y = (x - a) * (d - c) / (b - a) + c
    y = (x + 1) / 2
    return y


def update_reputation_beta_range(dataset_name, initial_reputations, source, reputation_score, start_value=0, end_value=1.1, step_value=0.1, thresholds_type='mean', output_folder='{}'):
    
    for i in np.arange(start_value, end_value, step_value):
        if i != 1:
            out_string = str(i).split('.')[1]
        else:
            out_string = str('-{}'.format(i))
        filename = "{}/new_reputations_{}_{}_beta_0_{}.csv".format(output_folder, thresholds_type,dataset_name, out_string)
        df_reputations = pd.DataFrame()
        if not os.path.isfile(filename):
            # use initial reputation csv
            df_reputations = pd.read_csv(initial_reputations, sep=';').drop(['Unnamed: 0'],axis=1) 
        else:
            # loading created reputations csv
            df_reputations = pd.read_csv(filename, sep=';').drop(['Unnamed: 0'],axis=1) 

        # print(df_reputations)
        update_reputation(df_reputations, source, reputation_score, alfa=(1-i), beta=i)

        df_reputations.to_csv(filename, sep=';')


def update_reputation(df_reputations, source, reputation_score, alfa, beta):
    
    # fetching old reputation
    old_rep = df_reputations.loc[df_reputations['vehicle_did'] == source]['score'].values[0]
    
    # Computing new reputation
    new_rep = (alfa * old_rep) + (beta * (old_rep + reputation_score))

    # Cap
    if new_rep < 0:
        new_rep = 0
    elif new_rep > 1:
        new_rep = 1
    
    # updating reputations
    df_reputations.loc[df_reputations['vehicle_did'] == source] = [source, new_rep]

    return

def check_similar_event_by_source(event, source):
    for denms in event['denms']:
        if denms[3] == source:
            return True
    return False

def process_event_similarity(event_collector, actual_time, reputations, alfa, beta, dataset_name=None, reputation_dataset=None, thresholds_type='mean', output_folder='new_reputations'):
    keys_to_delete = []
    for key in event_collector:
        rep_score = 0.25 if len(event_collector[key]['denms']) > 2 else -0.25 # CHANGE THESE VALUES ACCORDINGLY
        time_threshold = get_threshold_set_from_type(thresholds_type)[event_collector[key]['eventType']][0] * 1000
        # Checking time
        if rep_score < 0 and event_collector[key]['time_centroid'] > (actual_time - time_threshold) and event_collector[key]['time_centroid'] < actual_time:
            # Leave this in the event_collector
            continue
             
        for denm in event_collector[key]['denms']:
            if not dataset_name is None and not reputation_dataset is None:
                update_reputation_beta_range(dataset_name, reputation_dataset, denm[3], reputation_score=rep_score, thresholds_type=thresholds_type, output_folder=output_folder)
            else:
                update_reputation(df_reputations=reputations,source=denm[3], reputation_score=rep_score, alfa=alfa, beta=beta)
            
            if rep_score < 0:
                rep_changes[0] += 1
            else:
                rep_changes[1] += 1

        keys_to_delete.append(key)
    
    for key in keys_to_delete:
        del event_collector[key]

def main(args):
    
    # Loading parameters
    cam_time_window = args.time_window_cam * 1000 # from sec to ms
    denm_time_window = args.time_window_denm * 1000 # from sec to ms
    geojson_file = args.coverage

    alfa = args.alfa
    beta = args.beta

    denm_dataset = args.denmdataset
    cam_dataset = args.camdataset
    reputation_dataset = args.reputation

    output_folder = args.out_folder

    thresholds = get_threshold_set_from_type(args.thresholds_type)
    if not thresholds:
        print('error threshold type not found')
        exit(-1)
    if not os.path.isdir(output_folder):
        print('Folder not found: creating...')
        os.mkdir(output_folder)
    if not os.path.isfile(geojson_file):
        print("Coverage geojson file not found")
        exit()
    
    if not os.path.isfile(cam_dataset):
        print("{} file not found".format(cam_dataset))
        exit()

    if not os.path.isfile(denm_dataset):
        print("{} file not found".format(denm_dataset))
        exit()

    if (alfa+beta) != 1:
        print("alfa+beta should be = 1 - instead beta={} and alfa={}".format(beta, alfa))
        exit()
    
    # Loading geojson file
    with open(geojson_file) as f:
        geojson = json.load(f)
    

    # Loading dataset
    denm = pd.read_csv(denm_dataset, sep=';')
    cam = pd.read_csv(cam_dataset, sep = ";")

    dataset_name = denm_dataset.split('/')[2]

    
    reputations = pd.read_csv(reputation_dataset, sep=";").drop(['Unnamed: 0'],axis=1) 
    
    # Fixing position
    # denm['eventPos_long'] = denm['eventPos_long']/1e7
    # denm['eventPos_lat'] = denm['eventPos_lat']/1e7

    cam['referencePositionLong'] = cam['referencePositionLong']/1e7
    cam['referencePositionLat'] = cam['referencePositionLat']/1e7

    # Data pre-processing
    
    # 1. SimTime starts from zero, we need it in ms TAI format
    tai_sync = datetime.strptime('2004-01-01 00:00:00', '%Y-%m-%d %H:%M:%S') 
    # The former value is usually based on your local timezone. We need to convert to UTC as the time used in the dataset
    utc_tai_sync = datetime.utcfromtimestamp(tai_sync.timestamp()) 
    try:
        temp_start_time = datetime.strptime(args.startTime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD hh:mm:ss")
    
    new_start_time = (temp_start_time.timestamp()*1000) - (utc_tai_sync.timestamp() * 1000)
    denm['message_reception_time'] =  (denm['simulation_time']*1000) + new_start_time
    cam['message_reception_time'] =  (cam['simulationTime']*1000) + new_start_time

    # 2. Checking information quality
    denm = denm.loc[denm['situation_informationQ'] > 0.6]

    # 3. Group by simTime (receiving time), source, situationEventType
    # This excludes message propagations
    # In a simulated scenario we can apply drop duplicates as all the data in the columns are the same
    denm = denm.drop_duplicates()
    cam = cam.drop_duplicates()
    # In other scenarios we may also want to aggregate same messages generated from a certain source within a time interval

    # 4. TODO Cam preprocessing
    # deleting from the dataset messages not in the coverage area


    # 5. Order the dataset using time of message reception
    # We use this to simulate a real system
    denm = denm.sort_values(by=['message_reception_time'])
    cam = cam.sort_values(by=['message_reception_time'])

    # 6. deleting wrong formatted messages
    denm = denm.dropna(subset=['eventPos_long','eventPos_lat'])
    cam = cam.dropna(subset=['referencePositionLat','referencePositionLong'])

    # 7. drop the last column which is empty
    denm = denm.dropna(how='all', axis='columns')
    event_collector = {}
    i = 0

    for index, row in denm.iterrows():
        # print("Analysed {}/{}".format(i, len(denm)))
        i += 1
        # Resetting reputation score (as it change for each received message)
        reputation_score = 0

        # Time-based selection
        # Exclude all the DEN messages with a detection time too old in terms of receiving time
        # this may depend on the type of event
        # We use the time when we receive the message as refernce point
        message_age = row['message_reception_time'] - row['detection_time']
        time_threshold = thresholds[row['situation_eventType']][0] * 1000
        if message_age > time_threshold:
            # print('Skipping... message too old')
            continue

        # If the event is not within the timewindow den similarity computation should be computed
        if (new_start_time + denm_time_window) < row['message_reception_time'] or i == (len(denm)-1):
            par1 = None
            par2 = None
            if args.test_beta:
                par1 = dataset_name
                par2 = reputation_dataset

            # Computing reputation based on event similarity
            process_event_similarity(event_collector, actual_time=row['message_reception_time'], reputations=reputations, alfa=alfa, beta=beta, dataset_name=par1, reputation_dataset=par2, thresholds_type=args.thresholds_type, output_folder=output_folder)
            # Updating start time
            new_start_time = row['message_reception_time']

        # Spatial-based selection
        # Ignore messages generated by vehicles not in the edge node area
        # This may represent two conditions:
        #   1. Problem on vehicle sensor, so better to avoid this data (decrease reputation (?))
        #   2. Disinformation attack
        p = Point(row['eventPos_long'], row['eventPos_lat'])

        if not check_cov_intersection(geojson, p):
            reputation_score -= 0.25
            rep_changes[2] += 1
        else:
            reputation_score += 0.1
        # Comparing DEN message information with information provided by RSU (if any)
        if not compare_with_rsu(row):
            # Decrease the reputation
            reputation_score -= 1
            rep_changes[3] += 1
        else:
            # Considering that in our case we do not have RSU, it does not influence the reputation score
            # reputation_score += 0.1
            reputation_score += 0

        # For each DEN message received we need all the cam received in the past 'time_window' 
        # from the same source
        # We would use generation time, however it is obtained following this forumla: TimestampIts mod 65536, which makes it unusable for our scenario
        cam_from_source = cam.loc[(cam['source']==row['source']) & (cam['message_reception_time'] < row['detection_time']) & (cam['message_reception_time'] >  row['detection_time'] - cam_time_window)]

        inherent_cam_counter = 0
        if len(cam_from_source.index) > 0:
            for index, cam_row in cam_from_source.iterrows():
                if check_distance(den_pos=(row['eventPos_lat'], row['eventPos_long']), cam_pos=(cam_row['referencePositionLat'], cam_row['referencePositionLong']), r=thresholds[row['situation_eventType']][1]):
                    inherent_cam_counter += 1
            coherency_percentage = (inherent_cam_counter/len(cam_from_source.index)) * 100
        else:
            # For now, we do not give a reputation score
            coherency_percentage = -1
       
        # print("Percentage of coherent cam messages {}%".format(coherency_percentage))
        if coherency_percentage == -1:
            reputation_score += 0
        elif coherency_percentage < 10:
            reputation_score -= 0.25
            rep_changes[4] += 1

        elif coherency_percentage >= 10 and coherency_percentage < 30:
            # In this case the message is not considered for reputation update as it could be true
            # but we don't have enough CAMs to say that
            reputation_score += 0
        else:
            reputation_score += 0.25
            rep_changes[5] += 1
        
        eventType = row['situation_eventType']
        t = row['detection_time']

        # Event type collector selection
        if event_collector:
            similar_event = find_similar_event(event_collector, (eventType,p,t), thresholds_type=args.thresholds_type)
            if similar_event:
                # check if a similar message generated by the same source is already present:
                if not check_similar_event_by_source(event_collector[similar_event], row['source']):
                    event_collector[similar_event]["denms"] += [(eventType, p, t, row['source'])]
            else:
                event_collector[hash((eventType, p, t))] = {  "eventType" : eventType, 
                                                    "space_centroid" : p, 
                                                    "time_centroid" : t, 
                                                    "denms" : [(eventType, p, t, row['source'])]}
        else:
            event_collector[hash((eventType, p, t))] = {  "eventType" : eventType, 
                                                    "space_centroid" : p, 
                                                    "time_centroid" : t, 
                                                    "denms" : [(eventType, p, t, row['source'])]}
        if args.test_beta:
            update_reputation_beta_range(dataset_name, reputation_dataset, row['source'], reputation_score, thresholds_type=args.thresholds_type, output_folder=output_folder)
        else:
            update_reputation(df_reputations=reputations,source=row['source'], reputation_score=reputation_score, alfa=alfa, beta=beta)


    out_string = str(beta).split('.')[1]
    if not args.test_beta:
        reputations.to_csv("{}/new_reputations_{}_{}_beta_0_{}.csv".format(output_folder, args.thresholds_type, dataset_name, out_string), sep=";")
    
    logging.debug('{}_{}_den_sim_neg:{}'.format(dataset_name, out_string, rep_changes[0]))
    logging.debug('{}_{}_den_sim_pos:{}'.format(dataset_name, out_string, rep_changes[1]))
    logging.debug('{}_{}_not_in_area:{}'.format(dataset_name, out_string, rep_changes[2]))
    logging.debug('{}_{}_rsu:{}'.format(dataset_name, out_string, rep_changes[3]))
    logging.debug('{}_{}_cam_sim_neg:{}'.format(dataset_name, out_string, rep_changes[4]))
    logging.debug('{}_{}_cam_sim_pos:{}'.format(dataset_name, out_string, rep_changes[5]))





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Disinformation attack detection algorithm for VANET alert messages - \
                                     Command example: python3 v2v.py -dd ../dataset/mtits-dataset/DENM-dataset/datasetDen.csv -dc ../dataset/mtits-dataset/CAM-dataset/datasetCam.csv")

    parser.add_argument('-wc', '--time_window_cam', metavar='<time in secs>',
                        help='time used for CAM sampling during DENM evaluation', type=float, default=600)
    
    parser.add_argument('-wd', '--time_window_denm', metavar='<time in secs>',
                        help='time used for reputation score computation (collection of similar DENM)', type=float, default=20)
    
    parser.add_argument('-c', '--coverage', metavar='<geojson file path>',
                        help='geojson file defining the coverage of the edge node', type=str, default='coverage.json')
    
    parser.add_argument('-a', '--alfa', metavar='<value>',
                        help='alfa value for new reputation computation (old reputation)', type=float, default=0.5)
    
    parser.add_argument('-b', '--beta', metavar='<value>',
                        help='beta value for new reputation computation (reputation factor)', type=float, default=0.5)

    parser.add_argument('-dd', '--denmdataset', metavar='<den dataset location>',
                        help='denm dataset path', type=str, required=True)
    
    parser.add_argument('-dc', '--camdataset', metavar='<cam dataset location>',
                        help='cam dataset path', type=str, required=True)

    parser.add_argument('-r', '--reputation', metavar='<initial reputation dataset location>',
                        help='initial reputation path', type=str, required=True)

    parser.add_argument('-s', '--startTime', metavar='<simulation start time>',
                        help='simulation start time (check omnetpp.ini) file', type=str, default="2017-06-26 12:00:00")
    
    parser.add_argument('-l', '--logger', metavar='<loglevel>',
                        help='logging level', type=str, default='DEBUG')

    parser.add_argument('-t', '--test_beta',
                        help='updates the reputation for different beta values (0, 1, 0.01)', action='store_true')
    
    parser.add_argument('-tr', '--thresholds_type',
                        help='type of threshold to be used (mean, mode, median, 90percentile)', type=str, default='mean')
    
    parser.add_argument('-o', '--out_folder',
                        help='where to store the new reputations', type=str, default='new_reputations')

    args = parser.parse_args()

    # setting logger
    logger = logging.getLogger()
    level = logging.getLevelName(args.logger)
    logger.setLevel(level)

    main(args)

