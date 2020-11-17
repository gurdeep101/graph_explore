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

pd.set_option('display.max_columns', None) # None = see all columns; 2 = show 2 columns

# espn cricinfo bating partnerships for 2019 semi-finals
df = pd.read_csv('ipl_batting_partnerships.csv')
print(df.head())

# data preparation for delhi capitals
dc = df[df['team'] == 'Delhi Capitals']
dc.head()

# record of all DC partnerships in IPL 2019
dc['partners'] = [sorted([i,j]) for i,j in zip(dc.player_1, dc.player_2)]
dc['partnership'] = [' '.join(i) for i in dc.partners]
dc.head()

# aggregate data to construct network

# empty list to store players name
p1 = []
p2 = []

# empty list to store median of runs
r1 = []
r2 = []

for p in dc['partnership'].unique():
    # get temp df for each partnership
    temp = dc[dc['partnership'] == p]
    # get 1st row and column value of player_1; player_2
    p1.append(temp.iloc[0]['player_1'])
    p2.append(temp.iloc[0]['player_2'])
    
    # empty lists to store scores of both players
    a = []
    b = []
    
    # extract individual scores for both players
    for index, row in temp.iterrows():
        # scores of player 1
        a.append(row['score_1'])
        # scores of player_2
        b.append(row['score_2'])
        
    # append median of the score
    r1.append(median(a))
    r2.append(median(b))
    
# aggregate the data in a dataframe
team_df= pd.DataFrame({'p1' : p1, 'p2' : p2, 'r1' : r1, 'r2' : r2})
team_df.head()

# compute performance metric - overall contribution
# new column if r1>r2 return p1 else index p2
team_df['lead'] = np.where(team_df['r1'] > team_df['r2'], team_df['p1'], team_df['p2'])
team_df['follower'] = np.where(team_df['lead'] == team_df['p1'], team_df['p2'], team_df['p1'])
team_df['larger_score'] = np.where(team_df['r1'] >= team_df['r2'], team_df.r1, team_df.r2)
team_df['total_score'] = team_df.r1 + team_df.r2

# performance ratio
team_df['performance'] = team_df['larger_score']/(team_df['total_score']+0.01)

# construct network
g = nx.from_pandas_edgelist(team_df, source = 'follower', target = 'lead', edge_attr = ['performance'], create_using = nx.MultiDiGraph())

# get edge weights
_, wt = zip(*nx.get_edge_attributes(g, 'performance').items())

# plot the network
plt.figure(figsize = (9,9))
pos = nx.spring_layout(g, k =  20,seed = 21) #  k regualtes the distance between nodes
nx.draw(g, with_labels = True, node_color = 'skyblue', node_size = 4000, pos = pos, edgelist = g.edges(), edge_color = 'g', arrowsize = 15)
plt.show()

# get count of all the edges, node-wise
list(g.degree)

# count of incoming edges node-wise
list(g.in_degree)



