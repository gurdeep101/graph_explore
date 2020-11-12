#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:42:48 2020

@author: gurdeep
"""
'''
https://www.analyticsvidhya.com/blog/2020/02/network-analysis-ipl-data/?utm_source=blog&utm_medium=introduction-graph-theory-applications-python
nodes - batsment; 
edges 
- if batsmen batted together
- Direction of edge indicates who contributes more
Contribution - ratio of higher median/total median

'''
import pandas as pd
import numpy as np
import networkx as nx
from tqdm import tqdm
import warnings
from statistics import median
import matplotlib.pyplot as plt

# espn cricinfo bating partnerships for 2019 semi-finals
df = pd.read_csv('ipl_batting_partnerships.csv')
print(df.head())

# data preparation for delhi capitals
dc = df[df['team'] == 'Delhi Capitals']
dc.head()

dc.partners = 