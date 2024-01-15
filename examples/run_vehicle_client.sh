#!/bin/bash

# echo "Repetition number $i"
python3 vehicle_client.py -d ../dataset/mtits-malicious-dataset/DENM-dataset/datasetDen_1.25x_std.csv -f new_reputations/reputations_malicious_H_formula_1.25x_20 -m ../dataset/mtits-malicious-dataset/malicious_sources_1.25x_std.txt
python3 vehicle_client.py -d ../dataset/mtits-malicious-dataset/DENM-dataset/datasetDen_1.25x_std_30.csv -f output_dir/30 -m ../dataset/mtits-malicious-dataset/malicious_sources_1.25x_std_30.txt 
python3 vehicle_client.py -d ../dataset/mtits-malicious-dataset/DENM-dataset/datasetDen_1.25x_std_40.csv -f output_dir/40 -m ../dataset/mtits-malicious-dataset/malicious_sources_1.25x_std_40.txt
