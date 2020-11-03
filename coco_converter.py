import os
import argparse
from shutil import copyfile
from datasetcsgo import CsgoDataset
from tqdm import tqdm

root_path = 'e:/documento/outputs'
new_path = "e:/ai/coco-csgo2/"

parser = argparse.ArgumentParser(description='convert csgo-data style dataset into coco-style dataset')
parser.add_argument('-rp', help='the absolute path to the root directory of the csgo-data dataset', type=str)
parser.add_argument('-np', help='the absolute path the root directory of the new coco-style dataset to be created', type=str)
parser.add_argument('-split', help='''the percentage (value between 0 and 1) of the dataset destinated to training. 
                                      The remaining images will be destinated to validation.''', type=float)
parser.add_argument('-width', help='the dataset\'s images width', type=int)
parser.add_argument('-height', help='the dataset\'s images height', type=int)
args = parser.parse_args()

root_path = args.rp
new_path = args.np
split = args.split
img_rez = (args.width, args.height)

#---- create directories and paths ----
if not(os._exists(new_path)):
    os.mkdir(new_path)
os.mkdir(os.path.join(new_path,"images"))
os.mkdir(os.path.join(new_path,"labels"))

img_train_path = os.path.join(new_path,"images", "train")
img_val_path = os.path.join(new_path,"images", "val")
lbl_train_path = os.path.join(new_path,"labels", "train")
lbl_val_path = os.path.join(new_path,"labels", "val") 
os.mkdir(img_train_path)
os.mkdir(img_val_path)
os.mkdir(lbl_train_path)
os.mkdir(lbl_val_path)

#---- load dataset's dict ----
dset = CsgoDataset(root_path)
dset_dict = dset.dict_dataset
train_len = int(dset.length * split)

# for every image in dataset 
for idx, img in enumerate(tqdm(dset_dict.keys())):
    img_path = dset.get_image_path(idx)

    #if the image should be destinated to training directory
    if idx <= train_len:
        img_final_path = os.path.join(img_train_path, img[1]) + ".png" 
        lbl_final_path = os.path.join(lbl_train_path, img[1]) + ".txt"
    #else, go to validation
    else:
        img_final_path = os.path.join(img_val_path, img[1]) + ".png" 
        lbl_final_path = os.path.join(lbl_val_path, img[1]) + ".txt"

    copyfile(img_path, img_final_path) 

    #---- creating label for the image ----
    with open(lbl_final_path, "w+") as lbl_file:
        #for every bounding box's label 
        for d_idx, lbl in enumerate(dset_dict[img][0]):
            if lbl == "ct":
                w_lbl = 0
            elif lbl == "tr":
                w_lbl = 1
            
            #bbox correspondent to that label (lbl)
            bbox = dset_dict[img][1][d_idx]

            #x1 - x0, and y1 - y0 to find width and height
            #normalize all according to img size
            bbox_width = bbox[2] - bbox[0]
            bbox_height = bbox[3] - bbox[1]
            bbox_center = (((bbox_width/2)+bbox[0])/img_rez[0], \
                        ((bbox_height/2)+bbox[1])/img_rez[1])
            bbox_width = (bbox_width)/img_rez[0]
            bbox_height = (bbox_height)/img_rez[1]
            full_line = f"{w_lbl} {bbox_center[0]:.5f} {bbox_center[1]:.5f} {bbox_width:.5f} {bbox_height:.5f}"
            lbl_file.write(full_line + "\n")

    