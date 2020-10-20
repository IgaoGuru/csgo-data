import os
import sys
import os
import time
import cv2
from mss import mss
import numpy as np
import pandas as pd
import pyautogui

def screen_record(output_dir_path, timer, view_img=False, save_img=True): 
    #timer represents number of seconds for which the function is running
    last_time = time.time()
    initial_time = last_time
    with mss() as sct:
        while (time.time()-initial_time) < timer:
            # 1280 windowed mode for CS:GO, at the top left position of your main screen.
            # 26 px accounts for title bar. 
            monitor = {"top": 26, "left": 0, "width": 1280, "height": 720}
            printscreen = np.asarray(sct.grab(monitor))

            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()

            if view_img:
                cv2.imshow('window', printscreen)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            if save_img:
                cv2.imwrite(f'{output_dir_path}{int(last_time*1000)}.png', printscreen)

def match(csv_path, img_dir_path, output_path):
    '''
    loops through every image in img_dir_path, and outputs every bounding box in csv that matches the time of the image

    --- [INPUTS] ---
    csv_path = the path with the CSGO_LOG csv file (more about it in general documentation)
    img_dir_path = path to directory containing the screenshots from game. (All images must be png and their names should be
    output_path = path to ANNOTATION CSV, where the function will append all of its results 
    '''
    
    names = ['time','frame','team','enemy','x0','y0','x1','y1']
    csv = pd.read_csv(str(csv_path), names=names)
    current_time = time.time()
    current_time=str(int(current_time)*1000)

    with open(output_path, 'w+') as output:
        timetable = np.asarray(csv['time'])
        output.write(f'{csv_path}\n')
        output.write(f'{img_dir_path}\n')

        #loop through every image and find the best matching bbox's indexes in csv
        for img in os.listdir(img_dir_path):
            img_name = img[:-4]

            #if no match is found, go to next image
            match_idx = special_bin_search(timetable, int(img_name))
            if match_idx == -1:
                continue

            match_frame = csv.iloc[match_idx]['frame']
            matches_idxs = []

            #check for any bboxes of the same frame, 7 below and 7 above the match found (makes sure no bbox goes undetected)
            #while checking, makes list of all bboxes of same frame (matches_idxs), and outputs them (one bbox per line) in the output file
            for i in range(14):
                idx = match_idx-7+i
                if csv.iloc[(match_idx-7+i)]['frame'] == match_frame:
                    matches_idxs.append(match_idx-7+i)

                    output.write(f'{img_name}')
                    out_line = f"{csv.iloc[idx]['x0']},{csv.iloc[idx]['y0']},{csv.iloc[idx]['x1']},{csv.iloc[idx]['y1']}"
                    out_line = str(csv.iloc[idx]['team']) + ',' + str(csv.iloc[idx]['enemy']) + ',' + out_line 

                    output.write(f',{out_line}\n')
                if idx + 1 == len(csv['frame']) - 1:
                    break
            print(f'all the matches were: {matches_idxs}')
    return current_time

def plot_bbox(img_path, bboxes, sleeptime=False):
    '''
    receives a singurar image's path, and a list (bboxes), containing lists of 4 elements, which correspond to each bboxes 4 coordinates (x0, y0, x1, y1).
    sleeptime sets time between each image's exibition
    '''
    #load image and draw bboxes with cv2
    img = cv2.imread(img_path)
    print(bboxes)
    for bbox in bboxes:
        img = cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 255), 1)

    cv2.imshow('img', img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    if sleeptime != False:
        time.sleep(sleeptime)

def launch_plot_bboxes(img_dir_path, annotation_path, sleeptime=False):
    '''
    this function applies the plot_bbox function for all images in a directory, using for reference the ANNOTATION CSV (general docs)
    '''
    names = ['img','frame','team','enemy','x0','y0','x1','y1']
    df_annotation = pd.read_csv(str(annotation_path), names=names, skiprows=2)
    bboxes = []

    #combine all bboxes from same frame into one list (bboxes)
    #then, pass bboxes one by one into plot_bbox
    for idx, row in df_annotation.iterrows():
        bbox = list(row[['x0','y0','x1','y1']].values)
        bboxes.append(bbox)
        if idx == len(df_annotation) - 1:
            break
        if row['img'] != df_annotation.iloc[idx+1]['img']:
            img_name = str(row[['img']].values[0])
            img_path = img_dir_path + img_name + '.png'
            plot_bbox(img_path, bboxes, sleeptime=sleeptime)
            bboxes = []


def special_bin_search(array, x):
    '''
    binary search that returns the closest value to x (within an arbitrary threshold) in an sorted array
    '''

    n = len(array)
    L = 0
    R = n-1
    threshold = 1 #in ms
    
    #if x is smaller/bigger than every element in array, return the smallest/biggest value in array (if in range) 
    #if not in range, there is no value that matches x (return -1)
    if array[0] > x: 
        if abs(array[0]-x) <= threshold:
            return 0
        else:
            return -1
    if array[R] < x: 
        if abs(array[R]-x) <= threshold:
            return R
        else:
            return -1

    while True:
        mid = int(np.floor((L+R)/2))
        if array[mid] < x:
            L = mid + 1
        elif array[mid] > x:
            R = mid - 1
        #if left and right pointers get close enough, return the closest value inside L:R range
        if abs(L-R) <= 2 and abs(L-R) >= 0:
            idx = find_nearest(array[L:R+5], x)
            idx = L+idx
            if abs(array[idx] - x) <= threshold:
                return idx
            else:
                break
        elif array[mid] == x:
            return mid
    #if no match is found inside L:R range, return -1
    return -1

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def cleaner(img_dir_path, annotation_path):
    '''
    deletes unused images in img_dir_path to reduce wasted space
    '''

    names = ['img','frame','team','enemy','x0','y0','x1','y1']
    df_annotation = pd.read_csv(str(annotation_path), names=names, skiprows=2)
    imgs = list(df_annotation['img'])
    print(imgs)

    for img in os.listdir(img_dir_path):
        img_name = img[:-4]
        if int(img_name) not in imgs:
            print(f'deleted file: {img_name}')
            os.remove(img_dir_path + '\\' + img)