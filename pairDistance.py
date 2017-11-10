#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 18:49:23 2017

@author: chengqiguo
"""
import math
import matplotlib.pyplot as plt
import numpy as np
from readlines import read

def reading(filename):
    siList = []
    oList = []
    biggestList = read(filename)
    for each in biggestList:
        if each[0] == 'Si':
            siList.append(each)
        elif each[0] == 'O':
            oList.append(each)
    return siList, oList

def pairDist(lst1, lst2):
    return math.sqrt((lst1[0] - lst2[0]) ** 2 + (lst1[1] - lst2[1]) ** 2 \
                     + (lst1[2] - lst2[2]) ** 2)


def whichPair():
    x = input('Which pair distance do you want to plot? Enter 0 for Si-Si\
              1 for Si-O, 2 for O-O ')  
    return x

def histogram1(filename, x=None, binsize=5000):
    siList, oList = reading(filename)
    #x = whichPair()
    distList = []
    if x == '0':
        if siList == []:
            raise ValueError('There is no Silicon atom.')
        for i in range(len(siList)):
            for j in range(i + 1, len(siList)):
                distList.append(pairDist(siList[i][1:], siList[j][1:]))

    elif x == '1':
        if oList == []:
            raise ValueError('There is no Oxygen atom.')
        elif siList == []:
            raise ValueError('There is no Silicon atom.')
        for i in range(len(siList)):
            for j in range(len(oList)):
                distList.append(pairDist(siList[i][1:], oList[j][1:]))

    elif x == '2':
        if oList == []:
            raise ValueError('There is no Oxygen atom.')
        for i in range(len(siList)):
            for j in range(i + 1, len(oList)):
                distList.append(pairDist(oList[i][1:], oList[j][1:]))
                
    bins, edges = np.histogram(distList, bins=binsize, normed=False)
    left,right = edges[:-1],edges[1:]
    X = np.array([left,right]).T.flatten()
    Y = np.array([bins,bins]).T.flatten()
    return (X, Y, distList)

#histogram(x, siList, oList)
    