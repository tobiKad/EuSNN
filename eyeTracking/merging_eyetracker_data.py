#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
pd.set_option('display.max_columns', None)


# In[2]:


lb = pd.read_csv('./data/lb_data/timeseries_data/test.csv')
el = pd.read_csv('./data/el_data/test.csv')


# In[3]:


# Formating and Name Changing of the Labvanced and Eyelink Data.
el.Time = el.Time.apply(lambda x: int('%.0f' % (x * 1000)))
lb_fix = lb[lb['variable_name']=="fixations"]
lb = lb[lb['Task_Name'] == "large_grid"]
lb = lb[lb['variable_name'] == "XYTC"]
# df.rename(columns={"A": "a", "B": "c"})
lb = lb.rename(columns={"values":"X_lb","Unnamed: 12":"Y_lb","Unnamed: 13":"time_lb","Unnamed: 14":'c'})
lb['difference'] = lb['time_lb'] - lb['times']
# print(lb.mean())
# lb['time_lb'] = lb['time_lb'] - 1959600
# Format time column
lb['times'] = lb['times'].fillna(0)
lb = lb[(lb[['times']] != 0).all(axis=1)]

lb['time_lb'] = lb['time_lb'].fillna(0)
lb = lb[(lb[['time_lb']] != 0).all(axis=1)]
lb.time_lb = lb.time_lb.apply(lambda x: int('%.0f' % x))

# # Sort data towards the time column
# lb.sort_values('time_lb', inplace=True)

# # Fill all nan values with 0
lb[['X_lb','Y_lb']] = lb[['X_lb','Y_lb']].fillna(0)

# lb[['X_lb','Y_lb']] = lb[['X_lb','Y_lb']] + 200
# # Convert the coordinates points from floats to intergers
lb[['X_lb','Y_lb']] = lb[['X_lb','Y_lb']].apply(np.int64)
lb = lb[(lb[['X_lb']] != 0).all(axis=1)]


# In[4]:


lb['tsDiff'] = lb['time_lb'].diff()
print('The median difference is')
print(lb.tsDiff.median())


# In[5]:


correction = input()
lb['time_lb'] = lb['time_lb'] - int(correction)


# In[6]:


# EYE LINK DATA rename the eyelink columns
el = el.rename(columns={'X':'X_el','Y':'Y_el','Time':'t'})
el['time_el'] = el['t']


# In[7]:


#If so delete this row
el = el[(el[['X_el','Y_el','time_el']] != 0).all(axis=1)]
el.dropna(inplace=True)
#Check once agian
print('show missing data in eyelink dataset')
(el == 0).sum(axis=0)


# In[8]:


# set the index column
el = el.set_index('t')
df_xy = lb.set_index('time_lb')
# df_xy.info()


# ## Interpolation of the eyelink data

# In[9]:


# Interpolate data
df_temp = pd.concat([el, df_xy.index.to_frame()]).sort_index().interpolate()
df_temp = df_temp[~df_temp.index.duplicated(keep='first')]
df_xy = df_xy.merge(df_temp, left_index=True, right_index=True, how='left')
# df_xy


# In[10]:


#Check if you have any 0 or Nan values it might mess up the data and the calculation 
(df_xy.isnull()).sum(axis=0)


# In[11]:


(df_xy == 0).sum(axis=0)


# In[12]:


#If so delete this row
df_xy = df_xy[(df_xy[['X_el','Y_el','time_lb']] != 0).all(axis=1)]
#Check once agian
(df_xy == 0).sum(axis=0)


# In[13]:


# Save cleaned data in the folder
df_xy.to_csv('./data/bothEyetrackesrData/timeseries_data.csv', index=False)


# In[14]:


# df_xy = df_xy.loc[1631625944217:1631625948279]
df_xy.drop(columns="time_lb", inplace=True)
df_xy = df_xy.reset_index()
el = el.reset_index()
df_xy.time_el = df_xy.time_el.apply(lambda x: int('%.0f' % x))
# df_xy['t'] = pd.to_datetime(df_xy['t'], unit='ms')
df_xy.head()


# In[15]:


df_xy = df_xy.loc[500:600]
df_xy


# ## Calculation on the whole data set Labvanced and ET comp after downsampling

# In[16]:


print('fragment of the data over time')
x1 = df_xy.time_lb
y1 = df_xy.Y_lb
    
x2 = df_xy.time_el
y2 = df_xy.Y_el

# plot
plt.legend()
plt.xlabel('Time in the miliseconds', fontsize=34)
plt.ylabel('Coordinates Y in pixels', fontsize=34)
plt.plot(x1,y1, c='b', label='Labvanced', linewidth=4, alpha=0.75)
plt.plot(x2,y2, c='r', label='EyeLink', linewidth=4, alpha=0.75)
# plt.legend(loc='upper left')
# plt.gcf().autofmt_xdate()
plt.gcf().set_size_inches((20, 11))
# ALWAYS FLIP y AXIS!!!!!!!!!!!!!!!
plt.gca().invert_yaxis()
plt.grid()
plt.show()

x1 = df_xy.time_lb
y1 = df_xy.X_lb
    
x2 = df_xy.time_el
y2 = df_xy.X_el

# plot
plt.legend()
plt.xlabel('Time in the miliseconds', fontsize=34)
plt.ylabel('Coordinates X in pixels', fontsize=34)
plt.plot(x1,y1, c='b', label='Labvanced', linewidth=4, alpha=0.75)
plt.plot(x2,y2, c='r', label='EyeLink', linewidth=4, alpha=0.75)
# plt.legend(loc='upper left')
# plt.gcf().autofmt_xdate()
plt.gcf().set_size_inches((20, 11))
# ALWAYS FLIP y AXIS!!!!!!!!!!!!!!!
plt.gca().invert_yaxis()
plt.grid()
plt.show()


# In[17]:


print('whole data')
x1 = lb.time_lb
y1 = lb.Y_lb
    
x2 = el.time_el
y2 = el.Y_el

# plot
plt.legend()
plt.xlabel('Time in the miliseconds', fontsize=20)
plt.ylabel('Coordinates Y in pixels', fontsize=20)
plt.plot(x1,y1, c='b', label='Labvanced', linewidth=4, alpha=0.75)
plt.plot(x2,y2, c='r', label='EyeLink', linewidth=4, alpha=0.75)
# plt.legend(loc='upper left')
# plt.gcf().autofmt_xdate()
plt.gcf().set_size_inches((20, 11))
# ALWAYS FLIP y AXIS!!!!!!!!!!!!!!!
plt.gca().invert_yaxis()
plt.grid()
plt.show()

