#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


# In[2]:


import sys
sys.path.append('./ascData/PyGazeAnalyser-master/pygazeanalyser')
from edfreader import read_edf


# In[3]:


dataName = input()
data = './ascData/'+ dataName + '.asc'


# In[4]:


data_raw = read_edf(data, 'START', missing=0.0, debug=True)
type(data_raw), len(data_raw), type(data_raw[0]), data_raw[0].keys()


# In[5]:


df = pd.DataFrame(columns = ['Trial', 'X', 'Y', 'Start', 'End'])
for i in range(len(data_raw)):
    trial = i+1
    for j in range(len(data_raw[i]['events']['Efix'])):
        row = {'Trial':int(i), 'X':0, 'Y':0, 'Start':0, 'End':0}
        
        X = data_raw[i]['events']['Efix'][j][3]
        Y = data_raw[i]['events']['Efix'][j][4]
        start = data_raw[i]['events']['Efix'][j][0]
        end = data_raw[i]['events']['Efix'][j][1]
        
        row['X'] = X
        row['Y'] = Y
        row['Start'] = start
        row['End'] = end
        
        df = df.append(row, ignore_index=True)

df.Trial = df.Trial.astype(int)
                   
df


# In[6]:


asci_data = open(data, 'r')
lines = []
for line in asci_data:
    lines.append(line)


# In[7]:


for idx, line in enumerate(lines):
    if 'TimeStamp' in line:
        time_line = lines[idx-1].split()
        break

eyelink_time = int(time_line[1])
eyelink_time

unix_time_ml = int(float(time_line[-1]) * 1000)
unix_time_ml

diff = unix_time_ml - eyelink_time
diff

df['Start'] = (df.Start + diff) / 1000
df['End'] = (df.End + diff) / 1000
df.Start = df.Start.apply(lambda x: '%.3f' % x)
df.End = df.End.apply(lambda x: '%.3f' % x)

df


# In[8]:


df.to_csv('./data/el_data/el_events/' + dataName + '_events.csv', index = False)


# In[9]:


df_all = pd.DataFrame(columns = ['X', 'Y', 'Time'])
df_all

x = []
y = []
time = []

for i in range(len(data_raw)):
    x = x + list(data_raw[i]['x'])
    y = y + list(data_raw[i]['y'])
    time = time + list(data_raw[i]['trackertime'])

df_all.X = x
df_all.Y = y
df_all.Time = time

# df_all
df_all.Time = (df_all.Time + diff) / 1000
# df_all.Time = df_all.Time.apply(lambda x: '%.3f' % x)

df_all


# In[10]:


df_all.to_csv('./data/el_data/' + dataName + '.csv', index = False)


# In[ ]:





# In[ ]:




