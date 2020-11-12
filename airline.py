#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 13:35:40 2020

@author: gurdeep
"""

# https://www.analyticsvidhya.com/blog/2018/09/introduction-graph-theory-applications-python/

import os
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
# import pygraphviz

print(os.getcwd())

data = pd.read_csv('airlines_data.csv')
pd.set_option('display.max_columns', None) # None = see all columns; 2 = show 2 columns
print(data.head())
print(data.describe())

pd.reset_option('max_columns')
print(data.head())

# other args display. = max_colwidth, max_columns, max_rows, min_rows, 

df = nx.from_pandas_edgelist(data, source = 'Origin', target = 'Dest', edge_attr=True)
print(df.nodes)
print(df.edges)

plt.figure(figsize = (12,8))
nx.draw_networkx(df, with_labels=True)
plt.show()

# calcualate shortest path between AMA and PBI
shortest_path_distance = nx.dijkstra_path(df, source = 'AMA', target  = 'PBI', weight = 'Distance')
print(shortest_path_distance)

shortest_path_airtime = nx.dijkstra_path(df, source = 'AMA', target = 'PBI', weight = 'AirTime')
print(shortest_path_airtime)
