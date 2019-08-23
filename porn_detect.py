
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,stat
import urllib.request 
import sys
from PIL import ImageFilter
from PIL import ImageDraw
from PIL import Image
import string
import numpy
import time;
import logger as L
import utils

def grey_world(nimg):  
    nimg = nimg.transpose(2, 0, 1).astype(numpy.uint32)  
    avgB = numpy.average(nimg[0])  
    avgG = numpy.average(nimg[1])  
    avgR = numpy.average(nimg[2])  
 
    avg = (avgB + avgG + avgR) / 3  
    nimg[0] = numpy.minimum(nimg[0] * (avg / avgB), 255)  
    nimg[1] = numpy.minimum(nimg[1] * (avg / avgG), 255)  
    nimg[2] = numpy.minimum(nimg[2] * (avg / avgR), 255)  
    return  nimg.transpose(1, 2, 0).astype(numpy.uint8)

def pornDetect(image_path):


    save_image = True

    originImage = Image.open(image_path)
    if save_image : originImage.save("origin." + originImage.format, originImage.format)

    originW, originH = originImage.size

    prepareImage = originImage.resize((200, int(originH / originW * 200)))

    # 白平衡 Grey world
    nimage = numpy.array(prepareImage)
    nGreyWorldImage = grey_world(nimage);
    prepareImage = Image.fromarray(nGreyWorldImage).convert('RGB')
    if save_image : prepareImage.save("grey_world." + originImage.format, originImage.format)

    # print(img)
    # 平滑处理，类似低通滤波
    smoothImage = prepareImage.filter(ImageFilter.GaussianBlur())


    # smoothImage = originImage.filter(ImageFilter.SMOOTH_MORE)
    img = smoothImage.convert('YCbCr')

    if save_image : smoothImage.save("smoth." + originImage.format, originImage.format)
    w, h = img.size
    image_data = img.getdata()
    row_index = 0
    col_index = 0
    pixels =[]

    # 降噪参数
    scan_grid_pos = {'x':0, 'y':0}
    scan_grid_w = 4 #int(min(w,h) / 50)
    scan_grid = [];
    scan_grid_count = 0
    # print(splitData[0])
    draw = ImageDraw.Draw(smoothImage);
    for i, ycbcr in enumerate(image_data):
        if 0 == i % w :
            pixels.append([])
            if 0 != i:
                row_index +=1
            col_index = 0;
        
        y, cb, cr = ycbcr
        if 77 <= cb <= 127 and 133 <= cr <= 173:
            if save_image : draw.point((col_index, row_index), (0,0,0))
            pixels[row_index].append(1)
        else: 
            pixels[row_index].append(0)

        col_index +=1
        
    if save_image : smoothImage.save("selection." + originImage.format, originImage.format)
   
    # 降噪 以航为单位
    skin_cnt = 0;
    for row_index in range(len(pixels)):
        scan_grid_pos['x'] = 0
        col_index = 0;
        while col_index < len(pixels[row_index]):
            # print(col_index, row_index)
            if pixels[row_index][col_index] == 0:
                # noise
                for _x in range(scan_grid_pos['x'],min(scan_grid_pos['x'] +  scan_grid_w, w)):
                    pixels[row_index][_x]= 0
                    if save_image : draw.point((_x,row_index ), (255,0,0))
                col_index = scan_grid_pos['x'] +  scan_grid_w
            else:
                col_index += 1
            if 0 == col_index % scan_grid_w :
                scan_grid_pos['x'] = col_index
        scan_grid_pos['y'] += 1

    # 选择区域
    chosen_grid = { 
        'top' :0,
        'bottom': 0,
        'left' : 0,
        'right' : 0,
    }
    for row_index in range(len(pixels)):
        for row in pixels[row_index]:
            if row == 1:
                chosen_grid['top'] = row_index
                break;
        if 0 != chosen_grid['top']:
            break;

    for row_index in range(len(pixels) - 1, -1, -1):
        
        for row in pixels[row_index]:
            if row == 1:
                chosen_grid['bottom'] = row_index;
                break;
        if 0 != chosen_grid['bottom']:
            break;
    for col_index in range(len(pixels[0])):
        for row_index in range(len(pixels)):
            if pixels[row_index][col_index] == 1:
                chosen_grid['left'] = col_index;
                break;
        if 0 != chosen_grid['left']:
            break;

    for col_index in range(len(pixels[0])-1, -1, -1):
        for row_index in range(len(pixels)):
            if pixels[row_index][col_index] == 1:
                chosen_grid['right'] = col_index;
                break;
        if 0 != chosen_grid['right']:
            break;

    # 计算数值
    for row_index in range(chosen_grid['top'], chosen_grid['bottom']):
        scan_grid_pos['x'] = 0
        col_index = 0;
        for col_index in range(chosen_grid['left'], chosen_grid['right']):
            if pixels[row_index][col_index] == 1:
                skin_cnt += 1

    chosen_grid_size = ((chosen_grid['bottom'] - chosen_grid['top']) * (chosen_grid['right'] - chosen_grid['left']) );
    skin_rate = skin_cnt / (w * h )
    skin_grid_rate  = skin_cnt / (chosen_grid_size )

    if save_image : smoothImage.save("noise." + originImage.format, originImage.format)
    if save_image : cropImage = smoothImage.crop((chosen_grid['left'], chosen_grid['top'], chosen_grid['right'], chosen_grid['bottom']))
    if save_image : cropImage.save("crop." + originImage.format, originImage.format)
   
    print("皮肤占比:", skin_rate);
    print("皮肤占人体矩形比:", skin_grid_rate);
    print("是否识别为黄图:", skin_rate > 0.16 and skin_grid_rate > 0.31);


def printList(li):
    for row_index in range(len(li)):
        for col_index in range(len(li[row_index])):
            print(li[row_index][col_index], end="")
        print("");


# source = sys.argv[1];
L.info("argv: ", sys.argv)

current_path = os.getcwd();
L.info("current path: %s"%(current_path))

dir_path='%s/porn_detect_temp'%(current_path)

for argv_index in range(1, len(sys.argv)): 
    source = sys.argv[argv_index]
    if 'http' in source:
        file_path = utils.download(source, dir_path)
        L.info("download file path: %s"%(file_path))
    else :
        file_path = source;
    pornDetect(file_path)



