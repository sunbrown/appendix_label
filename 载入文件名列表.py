#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/20 21:01
# @Author  : Brown
# @FileName: 载入文件名列表.py
# @Software: PyCharm
import pickle
with open('./文件名列表.pk', 'rb+') as f:
    data = pickle.load(f)
print(data)