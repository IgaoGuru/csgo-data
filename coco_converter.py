import argparse
from PIL import Image
from shutil import copyfile
from datasetcsgo import CsgoDataset
from tqdm import tqdm

from random import shuffle
from random import seed
from os.path import exists
from os.path import join
from os import mkdir

parser = argparse.ArgumentParser(description='convert csgo-data style dataset into coco-style dataset')
parser.add_argument('-rp', help='the absolute path to the root directory of the csgo-data dataset', type=str)
parser.add_argument('-np', help='the absolute path the root directory of the new coco-style dataset to be created', type=str)
parser.add_argument('-split', help='''the percentage (value between 0 and 1) of the dataset destinated to training. 
                                      The remaining images will be destinated to validation.''', type=float)
parser.add_argument('-width', help='the dataset\'s images width', type=int)
parser.add_argument('-height', help='the dataset\'s images height', type=int)
parser.add_argument('-img', help='the image\'s new size (square) in pixels', type=int)
parser.add_argument('-seed', help='seed for dataset\'s random order', type=int, nargs='?', default=42)
args = parser.parse_args()

root_path = args.rp
new_path = args.np
split = args.split
img_rez = (args.width, args.height)
img_size = args.img

print(f'using seed: {args.seed}')
seed(args.seed)  

#---- create directories and paths ----

img_train_path = join(new_path,"images", "train")
img_val_path = join(new_path,"images", "val")
lbl_train_path = join(new_path,"labels", "train")
lbl_val_path = join(new_path,"labels", "val") 

if not(exists(new_path)):
    mkdir(new_path)
    mkdir(join(new_path,"images"))
    mkdir(join(new_path,"labels"))
    mkdir(img_train_path)
    mkdir(img_val_path)
    mkdir(lbl_train_path)
    mkdir(lbl_val_path)
    complete_np = False
else:
    if exists(join(new_path, "images")) and exists(join(new_path, "labels")):
        if exists(join(new_path, "images", "train")) and exists(join(new_path, "images", "val")) \
            and exists(join(new_path, "labels", "train")) and exists(join(new_path, "labels", "val")):
            complete_np = True
        else:
            raise Exception("the new path (-np) already contains a incomplete dataset!")
    else:
        raise Exception("the new path (-np) already contains a incomplete dataset!")

#---- create yaml file ----

with open(join(new_path, "coco-csgo") + ".yml", "w+") as yml:
    yml.write(f"train: your_path_here \n")
    yml.write(f"val: your_path_here \n")
    yml.write("\n")
    yml.write(f"nc: 2 \n")
    yml.write("\n")
    yml.write(f"names: [\'ct\', \'tr\']")

#---- load dataset's dict ----
dset = CsgoDataset(root_path)
dset_dict = dset.dict_dataset
train_len = int(dset.length * split)

#---- shuffle dataset's dict ----
order_keys = list(dset_dict.keys())
shuf_keys = list(dset_dict.keys())
shuffle(shuf_keys)

# for every image in dataset 
for idx, img in enumerate(tqdm(shuf_keys)):
    # img_path = dset.get_image_path(idx)
    img_idx = order_keys.index(img)
    img_path = dset.get_image_path(img_idx)

    #if the image should be destinated to training directory
    if idx <= train_len:
        img_final_path = join(img_train_path, img[1]) + ".png" 
        lbl_final_path = join(lbl_train_path, img[1]) + ".txt"
    #else, go to validation
    else:
        img_final_path = join(img_val_path, img[1]) + ".png" 
        lbl_final_path = join(lbl_val_path, img[1]) + ".txt"

    #resize img and save
    img_t = Image.open(img_path)
    img_t = img_t.resize((img_size, img_size))
    img_t = img_t.save(img_final_path)
    # copyfile(img_path, img_final_path) 

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
            bbox_center = [((bbox_width/2)+bbox[0])/img_rez[0], \
                        ((bbox_height/2)+bbox[1])/img_rez[1]]
            bbox_width = bbox_width/img_rez[0]
            bbox_height = bbox_height/img_rez[1]
            # if bbox_width > 1:
            #     bbox_width = 0.99999
            # if bbox_height > 1:
            #     bbox_height = 0.99999
            # if bbox_center[0] > 1:
            #     bbox_center[0] = 0.99999
            # if bbox_center[1] > 1:
            #     bbox_center[1] = 0.99999

            full_line = f"{w_lbl} {bbox_center[0]:.5f} {bbox_center[1]:.5f} {bbox_width:.5f} {bbox_height:.5f}"
            lbl_file.write(full_line + "\n")

    