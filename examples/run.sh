#!/bin/bash

python3 v2v.py -dd ../dataset/mtits-malicious-dataset/DENM-dataset/datasetDen_1.25x_std_40.csv -dc ../dataset/mtits-dataset/CAM-dataset/datasetCam.csv -r ../dataset/mtits-dataset/initial_reputations.csv --startTime "2017-06-26 12:00:00" -c ../dataset/mtits-dataset/coverage.json -tr 'mean' -o './output_dir/40/' -t &
python3 v2v.py -dd ../dataset/mtits-malicious-dataset/DENM-dataset/datasetDen_1.25x_std_40.csv -dc ../dataset/mtits-dataset/CAM-dataset/datasetCam.csv -r ../dataset/mtits-dataset/initial_reputations.csv --startTime "2017-06-26 12:00:00" -c ../dataset/mtits-dataset/coverage.json -tr 'mode' -o './output_dir/40/' -t & 
python3 v2v.py -dd ../dataset/mtits-malicious-dataset/DENM-dataset/datasetDen_1.25x_std_40.csv -dc ../dataset/mtits-dataset/CAM-dataset/datasetCam.csv -r ../dataset/mtits-dataset/initial_reputations.csv --startTime "2017-06-26 12:00:00" -c ../dataset/mtits-dataset/coverage.json -tr 'median' -o './output_dir/40/' -t & 
python3 v2v.py -dd ../dataset/mtits-malicious-dataset/DENM-dataset/datasetDen_1.25x_std_40.csv -dc ../dataset/mtits-dataset/CAM-dataset/datasetCam.csv -r ../dataset/mtits-dataset/initial_reputations.csv --startTime "2017-06-26 12:00:00" -c ../dataset/mtits-dataset/coverage.json -tr '90percentile' -o './output_dir/40/' -t &

