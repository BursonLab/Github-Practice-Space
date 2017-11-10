#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 12:38:33 2017

@author: chengqiguo
"""

def read(filename):
    with open(filename, 'r') as ins:
        array = []
        for line in ins:
            array.append(line)
    bigList = []
    for each in array:
        smallList = []
        if '\t' in each:
            smallList = each.split('\t')
            #get rid of \n
            last = smallList[-1]
            new = last[:-1]
            smallList[-1] = new
            #smallList[0] = smallList[0].decode('utf-8') 
            for i in range(1, len(smallList)):
                smallList[i] = float(smallList[i])
            bigList.append(smallList)
    return bigList
