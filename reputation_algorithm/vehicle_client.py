import os
import argparse
import pandas as pd
from datetime import datetime
from threshold_utils import get_threshold_set_from_type
import matplotlib.pyplot as plt
import re


def load_source(filename):
    sources = []
    with open(args.malicious, 'r') as fd:
        for line in fd:
            rep = {'[': '', ']': '', ' ':'', '\n': ''}
            rep = dict((re.escape(k), v) for k, v in rep.items()) 
            pattern = re.compile("|".join(rep.keys()))
            text = pattern.sub(lambda m: rep[re.escape(m.group(0))], line)
            for source in text.split(','):
                sources.append(int(source))
    return sources


def main(args):

    folder = args.folder
    dataset_name = args.dataset

    denm = pd.read_csv(dataset_name, sep = ";")
    malicious_sources = []
    dataset_name = dataset_name.split('/')[-1].replace('.csv', '')

    if not args.malicious is None:
        # Loading malicious sources
        malicious_sources = load_source(args.malicious)
        


    dfs = {
        'mean': pd.DataFrame({
            'beta': [],
            'event_type': [],
            'discarded': [],
            'correctly_discarded': [],
            'incorrectly_discarded': [],
            'amount_cor_discarded': [],
            'total_to_discard':[],
            'amount_incor_discarded': [],
            'total_not_discard':[],
            }),
        'mode': pd.DataFrame({
            'beta': [],
            'event_type': [],
            'discarded': [],
            'correctly_discarded': [],
            'incorrectly_discarded': [],
            'amount_cor_discarded': [],
            'total_to_discard':[],
            'amount_incor_discarded': [],
            'total_not_discard':[],
            }),
        'median': pd.DataFrame({
            'beta': [],
            'event_type': [],
            'discarded': [],
            'correctly_discarded': [],
            'incorrectly_discarded': [],
            'amount_cor_discarded': [],
            'total_to_discard':[],
            'amount_incor_discarded': [],
            'total_not_discard':[],
            }),
        '90percentile': pd.DataFrame({
            'beta': [],
            'event_type': [],
            'discarded': [],
            'correctly_discarded': [],
            'incorrectly_discarded': [],
            'amount_cor_discarded': [],
            'total_to_discard':[],
            'amount_incor_discarded': [],
            'total_not_discard':[],
            }),
    
    }

    # Fixing position
    denm['eventPos_long'] = denm['eventPos_long']/1e7
    denm['eventPos_lat'] = denm['eventPos_lat']/1e7

    # Data pre-processing
    
    # SimTime starts from zero, we need it in ms TAI format
    tai_sync = datetime.strptime('2004-01-01 00:00:00', '%Y-%m-%d %H:%M:%S') 
    # The former value is usually based on your local timezone. We need to convert to UTC as the time used in the dataset
    utc_tai_sync = datetime.utcfromtimestamp(tai_sync.timestamp()) 
    try:
        temp_start_time = datetime.strptime(args.startTime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD hh:mm:ss")
    
    new_start_time = (temp_start_time.timestamp()*1000) - (utc_tai_sync.timestamp() * 1000)
    denm['message_reception_time'] =  (denm['simulation_time']*1000) + new_start_time

    # Checking information quality
    denm = denm.loc[denm['situation_informationQ'] > 0.6]

    # Group by simTime (receiving time), source, situationEventType
    # This excludes message propagations
    # In a simulated scenario we can apply drop duplicates as all the data in the columns are the same
    denm = denm.drop_duplicates()
    

    # Order the dataset using time of message reception
    # We use this to simulate a real system
    denm = denm.sort_values(by=['message_reception_time'])

    
    files = sorted(os.listdir(folder))
    i = 0
    print('Analysing dir: {}'.format(folder))
    for filename in files:
        print('Processed {}/{}'.format(i, len(files)))
        i += 1
        if not filename.endswith('csv'):
            print('{} not a csv file'.format(filename))
            continue
        
        reputations = pd.read_csv('{}/{}'.format(folder,filename), sep=';')
        
        # if not dataset_name in filename:
        #     print('{} skipping'.format(filename))
        #     continue

        beta_value = filename.split('beta')[1].split('_')[2].replace('.csv','')
        if beta_value == '-1':
            print('changing beta value')
            beta_value = '1'
        threshold_type = filename.split('_')[2]
        
        discarded = {}
        correctly_discarded = {}
        total_to_be_discarded = {}
        incorrectly_discarded = {}
        total_not_to_be_discarded = {}
        total_processed = {}
        j = 0
        for index, row in denm.iterrows():
            source_reputation = reputations.loc[reputations['vehicle_did']==row['source']]['score'].values

            message_age = row['message_reception_time'] - row['detection_time']
            time_threshold = get_threshold_set_from_type(threshold_type)[row['situation_eventType']][0] * 1000
            if message_age > time_threshold:
                #print('Skipping... message too old')
                j += 1
                continue
            if not (row['situation_eventType'], threshold_type) in discarded.keys():
                discarded[(row['situation_eventType'], threshold_type)] = 0
                total_processed[(row['situation_eventType'], threshold_type)] = 0
                correctly_discarded[(row['situation_eventType'], threshold_type)] = 0
                total_to_be_discarded[(row['situation_eventType'], threshold_type)] = 0
                incorrectly_discarded[(row['situation_eventType'], threshold_type)] = 0
                total_not_to_be_discarded[(row['situation_eventType'], threshold_type)] = 0
            
            if not ('total', threshold_type) in discarded.keys():
                discarded[('total', threshold_type)] = 0
                total_processed[('total', threshold_type)] = 0
                correctly_discarded[('total', threshold_type)] = 0
                total_to_be_discarded[('total', threshold_type)] = 0
                incorrectly_discarded[('total', threshold_type)] = 0
                total_not_to_be_discarded[('total', threshold_type)] = 0


            total_processed[(row['situation_eventType'], threshold_type)] += 1
            total_processed[('total', threshold_type)] += 1
            # Messages coming from this sources should be discarded always
            if row['source'] in  malicious_sources:
                total_to_be_discarded[('total', threshold_type)] += 1
                total_to_be_discarded[(row['situation_eventType'], threshold_type)] += 1

            if source_reputation < 0.3:
                discarded[(row['situation_eventType'], threshold_type)] += 1
                discarded[('total', threshold_type)] += 1
                if row['source'] in malicious_sources:
                    correctly_discarded[(row['situation_eventType'], threshold_type)] += 1
                    correctly_discarded[('total', threshold_type)] += 1
                else:
                    incorrectly_discarded[(row['situation_eventType'], threshold_type)] += 1
                    incorrectly_discarded[('total', threshold_type)] += 1

            if not row['source'] in malicious_sources or len(malicious_sources) == 0:
                total_not_to_be_discarded[(row['situation_eventType'], threshold_type)] += 1
                total_not_to_be_discarded[('total', threshold_type)] += 1   
            # if j > 100:
            #     break
            # j += 1
        # Recording elements
        for key in discarded.keys():
            value = (discarded[key]/total_processed[key]) * 100
            if total_to_be_discarded[key] != 0:
                value_correctly = (correctly_discarded[key]/total_to_be_discarded[key]) * 100
            else:
                value_correctly = -1

            if total_not_to_be_discarded[key] != 0:
                value_incorrectly = (incorrectly_discarded[key]/total_not_to_be_discarded[key]) * 100
            else:
                value_incorrectly = -1

            dfs[key[1]].loc[len(dfs[key[1]].index)] = [beta_value, key[0], value, value_correctly, value_incorrectly, correctly_discarded[key], total_to_be_discarded[key], incorrectly_discarded[key], total_not_to_be_discarded[key]]
        print('Total skipped: {}'.format(j))
        j = 0
        print(total_processed)
    for key in dfs.keys():
        df = dfs[key]
        df.to_csv('{}/result_{}_{}.csv'.format(args.out_dir, dataset_name, key), sep=';')    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Vehicle client evaluating V2V messages")
    
    parser.add_argument('-f', '--folder', metavar='<folder>',
                        help='folder containing csv files', type=str, required=True)
    parser.add_argument('-s', '--startTime', metavar='<simulation start time>',
                        help='simulation start time (check omnetpp.ini) file', type=str, default="2017-06-26 12:00:00")
    parser.add_argument('-d', '--dataset', metavar='<dataset name>',
                        help='dataset name to process (one at a time supported)', type=str, required=True)
    parser.add_argument('-m', '--malicious',
                        help='indicates folder containing malicious sources ', type=str, default=None)
    parser.add_argument('-o', '--out_dir',
                        help='indicates folder containing malicious sources ', type=str, default='.')
    
    args = parser.parse_args()
    main(args)