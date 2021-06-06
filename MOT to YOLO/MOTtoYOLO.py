# MOT to YOLO converter

"""
Contact Author:

https://github.com/MrAsimZahid
https://www.linkedin.com/in/mrasimzahid/
"""

import pandas as pd
import os 
import os.path
import csv
from pathlib import Path
import shutil
from tqdm import tqdm
from natsort import natsorted
import glob
import pandas as pd
import cv2

"""
1-Clean path and prepare for new image(done)
2-Get image name(done)
3-Load annotations dataframe(done)
4-filter annotation with corresponding image
5-extract points(done)
6-process points(done)
7-remove df header
8-save annotaion in .txt file.
"""

#cwd = os.getcwd()
#print(f'cwd: {cwd}')


# Celta-Huesca\Celta-Huesca_inAir_2\img1\000001.jpg

# Celta-Huesca_inAir_2\img1\000001.jpg

# image
'*\*\img1\*.jpg'

# gt
'*\*\gt\*.txt'

#annot_df = ""

"""
Conversion check
https://github.com/ultralytics/yolov5/issues/1523


imgheight,imgwidth = img.size
x,y,w,h = a['hbox']   //for each tag in gtboxes object
x_min = x 
x_max = (x+w)
y_min = y
y_max = (y+h)
x_center = (x_min+x_max)/2.
y_center = (y_min+y_max)/2.
yolo_x = x_center/imgheight
yolo_w = w/imgwidth
yolo_y = y_center/imgwidth
yolo_h = h/imgheight

"""





"""
for annot_df in glob.glob('./*/*/gt/gt.txt'):
    print(annot_df)
    print('next')
    print(annot_df)
    print('next')
    for name in glob.glob(f'./*/*/img1/*.jpg'):
        print('next next')
        print(name)
"""


def modify_path(path):
    """
    Modify image path
    """
    x = path.replace('\img1', '').replace("\\", "_").replace(".jpg", "")
    #x = path.split('/', 1)[1:]
    x = '_'.join(x.split('_', 2)[2:])
    return x

def file_name(path):
    """
    get file name
    """
    return Path(path).stem

def annot_file_to_df(annotation_file):
    """
    Annotation file read ad return dataframe
    """
    df = pd.read_csv(annotation_file, delimiter=',', header=None)
    df.columns=['FRAME','ID','BB_LEFT','BB_TOP','BB_WIDTH','BB_HEIGHT','CONF','X','Y','Z']
    ball_frames = df.loc[df['ID'] == 1]
    return ball_frames


def extract_img_annot(df, frame_num):
    """
    Extract annotations point form txt files and send send to process
    """
    # flag = []
    # flag.append(frame_num)
    # return df.loc[df['FRAME'].isin(flag)]
    row = df.loc[df['FRAME'] == frame_num] 
    x1 = row.iloc[0]['BB_LEFT']
    y1 = row.iloc[0]['BB_TOP']
    x2 = row.iloc[0]['BB_WIDTH']
    y2 = row.iloc[0]['BB_HEIGHT']
    return x1, y1, x2, y2

def check_annot(df, img_name):
    """
    return bool whether annotation available or not in df  
    """
    flag = []
    flag.append(img_name)
    return df.loc[df['FRAME'].isin(flag)].shape[0] != 0

def convert_annot_to_yolov5(x_min, y_min, x_max, y_max, img):
    """
    Convert annotations into required yolov5 formamt
    x_center, y_center, width, height
    """
    w = x_max - x_min
    h = y_max - y_min
    imgheight,imgwidth = img.shape[0], img.shape[1]
    #x,y,w,h = a['hbox']   //for each tag in gtboxes object
    """
    x_min = x 
    x_max = (x+w)
    y_min = y
    y_max = (y+h)
    """
    x_center = (x_min+x_max)/2.
    y_center = (y_min+y_max)/2.
    yolo_x = x_center/imgheight
    yolo_w = w/imgwidth
    yolo_y = y_center/imgwidth
    yolo_h = h/imgheight
    return yolo_x, yolo_w, yolo_y, yolo_h
    #return x_center, y_center, w, h

def write_img(new_path, img):
    cv2.imwrite(f"../custom_data/images/{new_path}.jpg", img)

def write_txt(new_path, yolo_x, yolo_w, yolo_y, yolo_h):
    with open(f'../custom_data/labels/{new_path}.txt', 'w') as file:
        file.write(f"1 {yolo_x} {yolo_w} {yolo_y} {yolo_h}")
    file.close()


for subdir, dirs, files in os.walk('.'):
    #print(files)
    for file in files:
        file_path = os.path.join(subdir, file)
        if file_path.endswith(".txt"):
            try:
                annot_df = annot_file_to_df(file_path)
                #print(annot_df)
            except Exception as e:
                print(file_path)
                print("Error occured: ")
                print(e)
                break
        elif file_path.endswith(".jpg"):
            try:
                new_img_name = modify_path(file_path)
                #print(new_img_name)
                img_name = int(Path(file_path).stem)
                #print(type(img_name))
            except Exception as e:
                print(file_path)
                print("Error occured: ")
                print(e)
                continue
            try:
                if True == check_annot(annot_df, img_name):
                    x_min, y_min, x_max, y_max = extract_img_annot(annot_df, img_name)
                    #print(x_min, y_min, x_max, y_max)
                    frame = cv2.imread(file_path)
                    yolo_x, yolo_w, yolo_y, yolo_h = convert_annot_to_yolov5(x_min, y_min, x_max, y_max, frame)
                    #print(1, yolo_x, yolo_w, yolo_y, yolo_h)
                    write_img(new_img_name, frame)
                    write_txt(new_img_name, yolo_x, yolo_w, yolo_y, yolo_h)                
                else:
                    pass
            except Exception as e:
                print(file_path)
                print("Error occured: second try except ")
                print(e)
                continue
            finally:
                pass
                #print(file_path)
            #print(path)

