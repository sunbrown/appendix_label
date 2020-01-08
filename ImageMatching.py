#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Brown

import cv2
import shutil
import os
import re


def read_history(path):
    idx = 0
    if os.path.exists(path):
        f = open(path, 'r+')
        f.seek(0)
        history = f.readlines()
        if history:
            idx = int(history[0])
        f.close()
    else:  # 进度文件不存在创建一个
        f = open(path, 'w+')
        f.close()
    return idx


def save_history(path, idx):
    with open(path, 'w+') as ff:
        ff.seek(0)
        ff.truncate()
        ff.writelines(str(idx) + '\n')


def listing_img(in_path):
    name_list = []
    dir_list = []
    for root1, dirs1, files1 in os.walk(in_path):
        for file1 in files1:
            if os.path.splitext(file1)[1] == ".jpg":
                path1 = os.path.join(root1, file1)
                dir_list.append(path1)
                name_list.append(file1)
    return dir_list, name_list


def del_old_img(path, flag):
    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if flag == 'H':
                a = re.search('^H\w+', filename)
                if a:
                    os.remove(parent + '/' + a.string)
            else:
                a = re.search('^V\w+', filename)
                if a:
                    os.remove(parent + '/' + a.string)


if __name__ == '__main__':
    read_path = r'./check'
    save_path = r'./check_result'
    history_path = r'done.txt'
    im_idx = read_history(history_path)
    file_list = listing_img(read_path)[0]
    file_counts = len(file_list)
    # cv2.setMouseCallback('src', on_mouse)
    while im_idx <= file_counts:
        print('第{}张图片'.format(im_idx + 1))

        img_read_path = file_list[im_idx]
        img_read_path_split = img_read_path.split('\\')
        img_read_dir = '/'.join(img_read_path_split[0:-1])
        img_save_path = save_path + img_read_path[1:]
        img_save_path_split = img_save_path.split('\\')
        img_save_dir = '/'.join(img_save_path_split[0:-1])
        img = cv2.imread(img_read_path)
        print(img_read_path_split[-1])
        if img is None:
            break
        cv2.namedWindow('src', 1)
        if re.search('H\w+', img_read_path):
            flag = 'H'
        else:
            flag = 'V'
        cur_read_file_list = listing_img(img_read_dir)[1]
        cur_save_file_list = listing_img(img_save_dir)[1]
        cur_counts = str(len(cur_read_file_list))
        cur_idx = str(cur_read_file_list.index(img_read_path_split[-1])+1)
        while 1:
            text = str(im_idx+1) + '/' + str(file_counts) + '  ||  ' + cur_idx + '/' + cur_counts
            if img_read_path_split[-1] in cur_save_file_list and flag == 'H':
                flag1 = True
                text += '   H'
            if img_read_path_split[-1] in cur_save_file_list and flag == 'V':
                flag2 = True
                text += '   V'

            org = (200, 60)
            fontFace = cv2.FONT_HERSHEY_COMPLEX
            fontScale = 1.5
            fontcolor = (0, 255, 0)  # BGR
            thickness = 1
            lineType = 4
            bottomLeftOrigin = 1
            # cv.putText(img, text, org, fontFace, fontScale, fontcolor, thickness, lineType, bottomLeftOrigin)
            cv2.putText(img, text, org, fontFace, fontScale, fontcolor, thickness, lineType)

            cv2.imshow('src', img)
            k = cv2.waitKey(1) & 0xFF
            # ------------按R键，重新扣图------------------------------------------------
            if k == 32:
                del_old_img(img_save_dir, flag)
                if not os.path.exists(img_save_dir):
                    os.makedirs(img_save_dir)
                shutil.copyfile(img_read_path, img_save_path)
                im_idx += 1
                save_history(history_path, im_idx)
                break
            if k == ord('a'):
                im_idx -= 1
                if im_idx < 0:
                    im_idx = 0
                save_history(history_path, im_idx)
                break
            if k == ord('d'):
                im_idx += 1
                save_history(history_path, im_idx)
                break
            if k == 27:
                break

        if k == 27 or k == ord('q'):
            print('程序终止')
            cv2.destroyAllWindows()
            break
