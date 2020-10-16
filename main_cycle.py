import pandas as pd
import numpy as np
from utils import csgodata
from time import time

'''
-- [INPUTS] --

├── outputs
│   ├── 293849238
│   │   ├── imgs
│   │   │   ├── 293849238.png
│   │   │   ├── 293849239.png
│   │   │   ├── ...
│   │   ├── annotation_293849238.csv
│   │   ├── csgolog.csv
│   ├── 38029831
│   │   ├── imgs
│   │   │   ├── 38029835.png
│   │   │   ├── 38029904.png
│   │   │   ├── ...
│   │   ├── annotation_38029831.csv
│   │   ├── csgolog.csv

this file executes the entire data collection cycle, in the following steps:

1: take screenshots for 50 seconds
2: match screenshots with bounding boxes provided by the injected dll
3: clean all unused (unmatched) images from img_dir_path's directory (optimizing space)
4: rinse n' repeat 

'''

output_path = 'E:\\Documento\\outputs\\'

current_time = str(int(time()))
output_path = output_path+current_time+'\\'
img_dir_path = output_path+'imgs\\'
annotation_path = output_path+'annotation_'+current_time+'.txt'

with open(annotation_path, 'w') as myfile:
    pass

while True:
    csgodata.screen_record(img_dir_path, 50)

    csv_idx = csgodata.match(csv_path='E:\\ProgramFiles(Terav1)\\csgolog.txt',\
                            img_dir_path=img_dir_path, output_path=annotation_path)

    csgodata.launch_plot_bboxes(img_dir_path, annotation_path)

    csgodata.cleaner(img_dir_path, annotation_path)