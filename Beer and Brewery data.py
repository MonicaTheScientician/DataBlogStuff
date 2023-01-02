#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
# To plot pretty figures

# Only in Jupyter
get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)


# In[9]:


beer = pd.read_csv('beers.csv')
brew = pd.read_csv('breweries.csv')


# In[10]:


beer


# In[11]:


brew


# In[14]:


beer.drop(columns=['Unnamed: 0'], inplace=True)


# In[43]:


brew = brew.rename(columns={'Unnamed: 0' : 'brewery_id'})


# In[44]:


brew


# In[16]:


beer.info()


# In[19]:


beer['style'].unique().tolist()

#Looking at the list of unique beer styles in this data set.


# In[26]:


abvbystyle = beer.groupby(by='style').mean()


# In[27]:


abvbystyle.drop(columns=['id', 'brewery_id'], inplace=True)


# In[30]:


abvbystyle.sort_values(by='abv', ascending=False)


# In[130]:


brew['state'].value_counts()
#looking at the states here and seeing how many breweries are in each state.


# In[127]:


brew['state'] = brew['state'].astype('string')
#first tried to see if I just  needed to convert it to a string. I didn't, it's already a string. 


# In[367]:


brew.loc[(brew['state'] == 'CO')]


# In[145]:


for state in brew['state']:
    state.strip()
    
#Tried looping through the column to remove spaces. Still didn't result in the .loc working.


# In[368]:


cobrew = brew[brew['state'].str.contains('CO', regex=False)]
cobrew

#This ended up working to filter out for Colorado 


# In[174]:


cobrew = cobrew.loc[(cobrew['city'] == 'Denver')]
cobrew
#decided to just filter down to Denver specifically.


# In[165]:


ncbrew = brew[brew['state'].str.contains('NC', regex=False)]
ncbrew

#charlotte, mooresville are the only cities within an hour from Charlotte.
#morganton is 1.2 hours away, raleigh is 2.5 hours away, pittsboro is 2 hrs away, waynesville is 2.5 hrs away


# In[166]:


ncbrew = ncbrew.loc[(ncbrew['city'] == 'Charlotte') | (ncbrew['city'] == 'Mooresville')]
ncbrew

#only 4 to visit within Charlotte area.


# In[157]:


cabrew = brew[brew['state'].str.contains('CA', regex=False)]
cabrew
#Looking at all of the CA breweries, I decided to only look at San Diego and nearby cities.


# In[158]:


cabrew['city'].value_counts()

#The majority are in SD anyway. 


# In[162]:


cabrew = cabrew.loc[(cabrew['city'] == 'San Diego') | (cabrew['city'] == 'Temecula') | (cabrew['city'] == 'Carlsbad') | (cabrew['city'] == 'Santee')]

cabrew
#decided to only pull San Diego, Temecula, Carlsbad and Santee.


# In[175]:


visitset = pd.concat([cabrew, cobrew, ncbrew], axis=0)
visitset
#concatenating all of my location datasets together into one.


# In[207]:


merged = visitset.merge(beer, how='inner', on='brewery_id').drop(columns=['ounces']).rename(columns={'name_x':'brewery_name', 'name_y':'beer_name'})

#merging the list of selected breweries together with the beer data set. 


# In[208]:


merged.head()


# In[209]:


merged.info()
#note that IBus are the only ones with null values. Will drop that column because IBU is sort of a made up measurement anyway.


# In[210]:


merged['abv'].sort_values()
#just to see which ones are NaN and looking for their indices.


# In[211]:


merged.iloc[99 : 103]
#Looking up the breweries with NaNs. 


# In[212]:


merged.drop([99, 100, 101, 102], inplace=True)
#I don't like these styles anyway, so I'll just drop these tuples.


# In[213]:


merged['style'].value_counts()

#This shows me which styles are from these breweries


# In[369]:


favestyles = merged.loc[(merged['style'] == 'Saison / Farmhouse Ale') | (merged['style'] == 'American IPA') | 
           (merged['style'] == 'Tripel') |  (merged['style'] == 'American Pale Ale (APA)') | (merged['style'] == 'Fruit / Vegetable Beer') | (merged['style'] == 'Belgian IPA') | 
           (merged['style'] == 'Belgian Pale Ale')].sort_values(by='style').drop(columns=['ibu'])

#Filtering down from my merged data set to onlly include my favorite beer styles. 


# In[370]:


favestyles[['brewery_name', 'city']].drop_duplicates()
#Just to be thorough, lets make sure there are no duplicates.
#based on this we can see that there's only one brewery that I 'must' go to in Charlotte


# In[371]:


merged.loc[merged['brewery_name'] == 'NoDa Brewing Company']
#There are only a few breweries in Charlotte, so I wanted to see an example of one's beer offerings.


# In[373]:


denverbrews = favestyles.loc[favestyles['city']=='Denver']
denverbrews.sort_values(by='abv', ascending=False)

#Looking at Denver beers.


# In[251]:


charbrews = favestyles.loc[(favestyles['city']=='Charlotte') | (favestyles['city']=='Mooresville')]
charbrews.sort_values(by='abv', ascending=False)

#Looking at Charlotte beers.


# In[255]:


sdbrews = favestyles.loc[(favestyles['city']=='San Diego') | (favestyles['city']=='Temecula') | 
(favestyles['city']=='Santee') | (favestyles['city']=='Carlsbad')]
sdbrews.sort_values(by='abv', ascending=False)

#Looking at San Diego beers.


# In[259]:


beer['style'].value_counts(ascending=True).head(10)

#Looking at oddball beers.


# In[269]:


rarebeer = beer.loc[(beer['style'] == 'Flanders Oud Bruin') | (beer['style'] == 'Grisette') | 
                    (beer['style'] == 'Smoked Beer') | (beer['style'] == 'Braggot') |
                   (beer['style'] == 'Kristalweizen')]
rarebeer
#Filtering out for those styles and seeing what beers they are.


# In[270]:


rarebeer = brew.merge(rarebeer, how='inner', on='brewery_id')
rarebeer
#merging it with the brewery info so I can see where they are located. 


# In[397]:


merged

#reminding myself of the merged data set so I can look at making some charts. 


# In[398]:


avgabv = merged.groupby(by=['style']).mean().sort_values(by='abv').drop(columns=['brewery_id', 'ibu', 'id'])
avgabv

#Looking at the average ABVs by style.


# In[399]:


std = merged.groupby(by=['style']).std().sort_values(by='abv').drop(columns=['brewery_id', 'ibu', 'id'])
std

#Determining the standard deviation for the error bars. 


# In[400]:


avgabv = std.merge(avgabv, on='style', suffixes=('_std', '_avg')).sort_values(by='abv_avg')
avgabv

#merging together dataframes so I can have average abv and standard deviations in one dataframe.


# In[401]:


error = avgabv['abv_std']

fig = plt.figure(figsize=(20,10))
names = avgabv.index
abv = avgabv['abv_avg']
positions = np.arange(len(avgabv['abv_avg']))
plt.bar(positions, abv, yerr=error, width = 0.6, color='g')
plt.xticks(positions, names, size=18)
plt.ylabel('ABV', size=25)
plt.xlabel('Styles', size=25)
plt.title('Average ABV per Style', size=25)

plt.axhline(y=np.nanmean(abv), ls='--', color='b')
plt.xticks(rotation = 90)
plt.yticks(size=18)
plt.show()


# In[402]:


merged.loc[merged['style']=='American Brown Ale']

#looking up why brown Ale has such a weird error bar. This makes sense.


# In[327]:


denverbrews

#reminding myself of denver dataframe


# In[334]:


#Visualizating how few belgian ales are available.

labels = 'American IPA', 'American Pale Ale (APA)', 'Belgian Ale', 'Other'
sizes = [47, 23, 12, 18]
explode = (0, 0, 0.1, 0)  

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('The Lack of Belgian Ales in Denver')

plt.show()


# In[406]:


# Creating dataset to see all of the datatypes
beerstyles = beer_list.index.tolist()
 
count = beer_list['count'].tolist()
 
 
# Creating explode data
#explode = (0.1, 0.0, 0., 0.0, 0.0, 0.0, 0.0)
 
# Creating color parameters
colors = ( "orange", "cyan", "brown",
          "grey", "indigo", "beige", "red", "purple", "yellow", "teal", "pink")
 
# Wedge properties
wp = { 'linewidth' : 1, 'edgecolor' : "green" }
 
# Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d})".format(pct, absolute)
 
# Creating plot
fig, ax = plt.subplots(figsize =(10, 7))
wedges, texts, autotexts = ax.pie(count,
                                  autopct = lambda pct: func(pct, count),
                                  #explode = explode,
                                  labels = beerstyles,
                                  shadow = True,
                                  colors = colors,
                                  startangle = 90,
                                  wedgeprops = wp,
                                  textprops = dict(color ="magenta"))
 
# Adding legend
ax.legend(wedges, beerstyles,
          title ="Styles",
          loc ="center left",
          bbox_to_anchor =(1, 0, 0.5, 1))
 
plt.setp(autotexts, size = 8, weight ="bold")
ax.set_title("Customizing pie chart")
 
# show plot
plt.show()

#Kind of messy but not quite sure how to clean it up. 


# In[403]:


mergedcopy = merged.copy()


# In[404]:


mergedcopy.loc[(mergedcopy['style'] == "Belgian Pale Ale")] = 'Belgian Ale'
mergedcopy.loc[(mergedcopy['style'] == "Pumpkin Ale")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "Schwarzbier")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "American Double / Imperial Stout")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "Old Ale")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "Munich Helles Lager")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "Fruit / Vegetable Beer")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "Chile Beer")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "Belgian IPA")] = 'Belgian Ale'
mergedcopy.loc[(mergedcopy['style'] == "Tripel")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "American Pale Lager")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "Wheat Ale")] = 'Other'
mergedcopy.loc[(mergedcopy['style'] == "Beglian Ale")] = 'Belgian Ale'


# In[405]:


beer_list = mergedcopy['style'].value_counts()
beer_list = pd.DataFrame(beer_list).rename(columns={'style':'count'})
beer_list


# In[ ]:





# In[ ]:




