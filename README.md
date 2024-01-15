# DIVA

This repository provides the code of the outlier detection algorithm outlined in the paper *DIVA: A DID-based Reputation System for Secure Transmission in VANETs using IOTA*.

**Abstract**
Today's advancement in Vehicular Ad-hoc Networks (VANET) constitutes a cornerstone in ensuring traffic safety in Intelligent Transportation Systems (ITS). In this context, vehicle-to-vehicle (V2V) communications are a pivotal enabler for road safety, traffic optimization, and pedestrian protection. However, V2V communications lack effective and efficient security solutions that can adequately ensure the trustworthiness of the source of the transmitted content. In this work, we originally propose DIVA, i.e., a Decentralized Identifier-based reputation system for secure transmission in VAnets. In particular, we claim the suitability of utilizing IOTA, a Direct Acyclic Graph (DAG)-based ledger, to securely store reputation scores and of leveraging Decentralized Identifiers (DIDs) to identify participating vehicles. DIVA also incorporates and implements a reputation algorithm that computes reputation scores by analyzing both safety and non-safety messages, exchanged among vehicles and Road Side Units (RSUs) in compliance with the related European Telecommunications Standards Institute (ETSI) standards. Thus, DIVA is able to effectively identify malicious contributors and decrease their reputation scores. The reported experimental results clearly show the feasibility and effectiveness of DIVA, by working on an extended and comprehensive dataset of realistic V2V messages; the dataset has been made openly accessible to the research community, also to increase result reproducibility.

## Python Scripts
The directory [reputation_algorithm](./reputation_algorithm/) contains three python files:
```python
v2v.py
vehicle_client.py
threshold_utils.py
```

-  ``` v2v.py ``` provides the algorithm that computes the reputations which will be assigned to each vehicle sources belonging to a VANET.

- ```vehicle_client.py```  uses the reputations computed by ```v2v.py``` to determine whether a message can be trusted or not.

- ``` threshold_utils.py ``` is an utility file containing default threshold used in ``` v2v.py ```

## How to run
The initial script that should be run is ```v2v.py```, containing the implementation of the algorithm computing the reputations of each vehicle. he computation of these reputations is achieved through the analysis of a dataset providing V2X communications data adhering to the ETSI standard, which is accessible [here](https://github.com/MMw-Unibo/ETSI-V2V-Dataset). The script utilizes an initial set of reputations, as the one provided [here](./dataset/initial_reputations.csv), and a [coverage area](./dataset/coverage.json) defining the geographical area managed by an edge node.

The script is highly configurable for precise tuning of various parameters to accommodate diverse edge node locations.

The available options are listen below:
```
  -h, --help            show this help message and exit
  -wc <time in secs>, --time_window_cam <time in secs>
                        time used for CAM sampling during DENM evaluation
  -wd <time in secs>, --time_window_denm <time in secs>
                        time used for reputation score computation (collection of similar DENM)
  -c <geojson file path>, --coverage <geojson file path>
                        geojson file defining the coverage of the edge node
  -a <value>, --alfa <value>
                        alfa value for new reputation computation (old reputation)
  -b <value>, --beta <value>
                        beta value for new reputation computation (reputation factor)
  -dd <den dataset location>, --denmdataset <den dataset location>
                        denm dataset path
  -dc <cam dataset location>, --camdataset <cam dataset location>
                        cam dataset path
  -r <initial reputation dataset location>, --reputation <initial reputation dataset location>
                        initial reputation path
  -s <simulation start time>, --startTime <simulation start time>
                        simulation start time (check omnetpp.ini) file
  -l <loglevel>, --logger <loglevel>
                        logging level
  -t, --test_beta       updates the reputation for different beta values (0, 1, 0.01)
  -tr THRESHOLDS_TYPE, --thresholds_type THRESHOLDS_TYPE
                        type of threshold to be used (mean, mode, median, 90percentile)
  -o OUT_FOLDER, --out_folder OUT_FOLDER
                        where to store the new reputations
```


The script ```vehicle_client.py```  processes vehicle messages and assesses the reliability of the available information by leveraging the reputations generated in the previous script.

Examples of how to run these scripts are provided in the [examples](./examples) folder.


<!-- ## How to Cite
TBD -->