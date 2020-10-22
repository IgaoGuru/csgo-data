import pandas as pd
from os import remove
from os.path import isfile
from os import stat
from os import mkdir
import numpy as np
from utils import csgodata
import time

'''
├── outputs
│   ├── 293849238
│   │   ├── imgs
│   │   │   ├── 293849238.png
│   │   │   ├── 293849239.png
│   │   │   ├── ...
│   │   ├── annotation_293849238.csv
│   ├── 38029831
│   │   ├── imgs
│   │   │   ├── 38029835.png
│   │   │   ├── 38029904.png
│   │   │   ├── ...
│   │   ├── annotation_38029831.csv

this file executes the entire data collection cycle, in the following steps:

1: take screenshots for 50 seconds
2: match screenshots with bounding boxes provided by the injected dll
3: clean all unused (unmatched) images from img_dir_path's directory (optimizing space)
4: rinse n' repeat 

'''
output_path = 'E:\\Documento\\outputs\\'
STANDARD_CSV_PATH = 'C:\\csgolog\\csgolog.txt' 

current_time = str(int(time.time()))
output_path = output_path+current_time+'\\'
img_dir_path = output_path+'imgs\\'
annotation_path = output_path+'annotation_'+current_time+'.txt'

mkdir(output_path)
mkdir(img_dir_path)

with open(annotation_path, 'w') as myfile:
    pass

while True:
    
    while not isfile(STANDARD_CSV_PATH):
        time.sleep(0.2)
    while stat(STANDARD_CSV_PATH).st_size == 0:
        time.sleep(0.2)

    saved_frames = csgodata.screen_record(img_dir_path, 15)

    matched_frames = csgodata.match(csv_path=STANDARD_CSV_PATH,\
                            img_dir_path=img_dir_path, output_path=annotation_path)

    kept_frames, deleted_frames = csgodata.cleaner(img_dir_path, annotation_path)
    
    print(f'saving around {saved_frames} frames per minute.')
    print(f'matching around {matched_frames} frames per minute.')
    print(f'keeping around {kept_frames} frames per minute.')
    print(f'deleting around {deleted_frames} frames per minute.')

    remove(STANDARD_CSV_PATH)

    time.sleep(10)