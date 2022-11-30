# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:45:54 2022

@author: Mathieu
"""

import pandas as pd
import math
import numpy as np
import itertools as ite

def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


ville = pd.read_csv('C:/Users/Mathieu/Desktop/Villes_marchant.csv')

ville_tab = pd.DataFrame(columns=('Ville', 'Latitude', 'Longitude'))

for i in ville.index:
    information = ville.iloc[i].str.split(';')
    data = pd.DataFrame({'Ville':information[0][0], 'Latitude':information[0][5], 'Longitude':information[0][6]}, index=(0, 1, 2))
    ville_tab = pd.concat([ville_tab, data[0:1]], ignore_index=True)

ville_tab['Latitude'] = ville_tab['Latitude'].astype(float)
ville_tab['Longitude'] = ville_tab['Longitude'].astype(float)


distance = round(haversine(ville_tab.iloc[1][[1,2]].values, ville_tab.iloc[0][[1,2]].values)/1000)
print("L'ecart entre", ville_tab.iloc[1][0], "et" , ville_tab.iloc[0][0], "est de",  distance, 'km')

####################################################################################################################
#meilleur chemin pour les 5 meilleures villes méthode explosion combinatoire

print(ville_tab[0:5])

test_distance = pd.DataFrame(columns=('Ville1', 'Ville2', 'Distance'), index=np.arange(0, 5*5))

print(ville_tab['Ville'][0])
for j in ville_tab.index:
    for i in ville_tab.index:
        test_distance['Ville1'][j] = ville_tab['Ville'][j]
        test_distance['Ville2'][j] = ville_tab['Ville'][i]
        test_distance['Distance'][j] = round(haversine(ville_tab.iloc[j][[1,2]].values, ville_tab.iloc[i][[1,2]].values)/1000)

test_distance['Distance'] = test_distance['Distance'].replace(0, np.nan).dropna()
#print(test_distance['Distance'])        
print(test_distance[test_distance['Distance'] == min(test_distance['Distance'])])







distance = 20000000



liste = np.arange(0, len(ville_tab[0:5]))

permut = list(ite.permutations(liste))

df = pd.DataFrame({'Trajet':permut, 'Distance':1})
for i in range(len(df)):
    d = 0
    k = df['Trajet'][i] 
    for j in k:
        if(j == k[-1]):
           d = d + round(haversine(ville_tab.iloc[j][[1,2]].values, ville_tab.iloc[k[0]][[1,2]].values)/1000)
        else:
            d = d + round(haversine(ville_tab.iloc[j][[1,2]].values, ville_tab.iloc[j+1][[1,2]].values)/1000)        
    df['Distance'][i] = d + round(haversine(ville_tab.iloc[k[-1]][[1,2]].values, ville_tab.iloc[k[0]][[1,2]].values)/1000)
print(df[df['Distance'] == min(df['Distance'])])

for i in permut:
    d = 0
    for j in i:
        if(j == i[-1]):
           d = d + round(haversine(ville_tab.iloc[j][[1,2]].values, ville_tab.iloc[i[0]][[1,2]].values)/1000)
        else:
            d = d + round(haversine(ville_tab.iloc[j][[1,2]].values, ville_tab.iloc[j+1][[1,2]].values)/1000)
    
    if(d<=distance):
        distance = d 
        trajet = i
        
distance = distance #+ round(haversine(ville_tab.iloc[trajet[-1]][[1,2]].values, ville_tab.iloc[trajet[0]][[1,2]].values)/1000)        

print(trajet, distance)
print(trajet[-1], trajet[0], round(haversine(ville_tab.iloc[trajet[-1]][[1,2]].values, ville_tab.iloc[trajet[0]][[1,2]].values)/1000) )





d = 0.0
print(type(d))

j = (0, 4, 3, 2, 1)
for k in range(len(j)):
        if(j[k] == j[-1]):
           d = d + round(haversine(ville_tab.iloc[j[-1]][[1,2]].values, ville_tab.iloc[j[0]][[1,2]].values)/1000)
           print(ville_tab['Ville'][j[-1]], ville_tab['Ville'][j[0]])
        else:
            d = d + round(haversine(ville_tab.iloc[j[k]][[1,2]].values, ville_tab.iloc[j[k+1]][[1,2]].values)/1000)   
            print( ville_tab['Ville'][j[k]], ville_tab['Ville'][j[k+1]])
        print(d)
            
print(d)
