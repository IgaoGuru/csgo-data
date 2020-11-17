import numpy as np
import argparse
from PIL import Image
from shutil import copyfile
from datasetcsgo import CsgoDataset
from tqdm import tqdm
from time import sleep

from random import shuffle
from random import seed
from os.path import exists
from os.path import join
from os import mkdir
from os import walk
import seaborn as sb
import matplotlib.pyplot as plt

from utils.csgodata import plot_bbox

parser = argparse.ArgumentParser(description='convert csgo-data style dataset into coco-style dataset')
parser.add_argument('-rp', help='the absolute path the root directory of the coco-style dataset to be checked', type=str)
parser.add_argument('-width', help='the width in pixels of the dataset\'s images', type=int)
parser.add_argument('-height', help='the height in pixels of the dataset\'s images', type=int)
parser.add_argument('-img', help='the size, in pixels of the coco dataset\'s images', type=int)
args = parser.parse_args()

root_path = args.rp
width = args.width
height = args.height
img_size = args.img

#---- create directories and root_paths ----

img_train_path = join(root_path,"images", "train")
img_val_path = join(root_path,"images", "val")
lbl_train_path = join(root_path,"labels", "train")
lbl_val_path = join(root_path,"labels", "val") 

if exists(join(root_path, "images")) and exists(join(root_path, "labels")):
    if exists(join(root_path, "images", "train")) and exists(join(root_path, "images", "val")) \
        and exists(join(root_path, "labels", "train")) and exists(join(root_path, "labels", "val")):
        complete_np = True
    else:
        raise Exception("the new root_path (-path) already contains a incomplete dataset!")
else:
    raise Exception("the new root_path (-path) already contains a incomplete dataset!")

def coco_check1():
    matrix = np.zeros((height+1, width+1), int)
    class_matrix = np.zeros((11, 11), int)

    counter = 0
    # for every label in training dataset 
    for _, _, lbl_path in walk(lbl_train_path):
        for lbl_path in tqdm(lbl_path):
            with open(join(lbl_train_path, lbl_path), "r") as filezin:
                ct_count, tr_count = 0, 0
                lines = filezin.readlines()
                for line in lines:
                    coords = [x for x in line.split(" ")]
                    coords = list(map(float, coords))
                    ct_tr = int(coords[0])
                    x0 = int(coords[1]*width)
                    y0 = int(height - coords[2]*height)
                    x1 = int(coords[3]*width)
                    y1 = int(height - coords[4]*height)
                    # print(x0, y0, x1, y1)

                    matrix[y0, x0] += 1
                    matrix[y1, x0] += 1
                    # matrix[y0, x1] += 1
                    # matrix[y1, x1] += 1

                    if ct_tr == 1:
                        ct_count += 1
                    else:
                        tr_count += 1
                class_matrix[ct_count, tr_count] += 1
    return matrix, class_matrix

def coco_heatmap():
    # x_rol = np.zeros((width+1,), int)
    # y_rol = np.zeros((height+1,), int)
    x_rol = []
    y_rol = []
    class_matrix = np.zeros((11, 11), int)

    # for every label in training dataset 
    for _, _, lbl_path in walk(lbl_train_path):
        for lbl_path in tqdm(lbl_path):
            with open(join(lbl_train_path, lbl_path), "r") as filezin:
                ct_count, tr_count = 0, 0
                lines = filezin.readlines()
                #this is all wrong - check code in next function BRO HOW DID YOU MESS THAT UP BROOOOOO
                for line in lines:
                    coords = [x for x in line.split(" ")]
                    coords = list(map(float, coords))
                    ct_tr = int(coords[0])
                    x0 = int(coords[1]*width)
                    y0 = int(height - coords[2]*height)
                    x1 = int(coords[3]*width)
                    y1 = int(height - coords[4]*height)
                    # print(x0, y0, x1, y1)
                    
                    x_rol.append(x0)
                    x_rol.append(x1)
                    y_rol.append(y0)
                    y_rol.append(y1)

                    if ct_tr == 1:
                        ct_count += 1
                    else:
                        tr_count += 1
                class_matrix[ct_count, tr_count] += 1

    # matrix, class_matrix = coco_check1()
    x_rol, y_rol, class_matrix = coco_check2()
    plt.hist2d(x_rol, y_rol, bins=85)

    # summy = np.sum(matrix)
    # print(summy)
    # matrix = matrix/summy
    # heat_map = sb.heatmap(matrix)
    # heat_map_2 = sb.heatmap(class_matrix)
    plt.show()

def coco_show_images():
    for _, _, lbl_path in walk(lbl_train_path):
        for lbl_path in tqdm(lbl_path):
            img_path = lbl_path[:-3]
            img_path = join(img_train_path, img_path) + "png"
            bboxes = []

            with open(join(lbl_train_path, lbl_path), "r") as filezin:
                lines = filezin.readlines()
                for line in lines:
                    coords = [float(x) for x in line.split(" ")]
                    coords = coco_coord_2pixel(coords[1:], img_size)
                    bboxes.append(coords)

            plot_bbox(img_path, bboxes)
            sleep(0.2)

def coco_coord_2pixel(coco_coords, img_size):
    bbox_width = int(coco_coords[2]*img_size)
    bbox_height = int(coco_coords[3]*img_size)
    bbox_center_x = int(coco_coords[0]*img_size)
    bbox_center_y = int(coco_coords[1]*img_size)
    x0 = bbox_center_x - (bbox_width/2)
    y0 = bbox_center_y - (bbox_height/2)
    x1 = bbox_center_x + (bbox_width/2)
    y1 = bbox_center_y + (bbox_height/2)
    return list(map(int, [x0, y0, x1, y1]))

coco_show_images()

