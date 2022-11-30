# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:00:22 2022

@author: Mathieu
"""


import itertools as itt
import pandas as pd
import math
import folium
import webbrowser
import time
import numpy as np
start = time.time()
import random


#Fonction permettant de trouver la distance entre deux villes selon leur lattitudes et longitudes
def distance(lat1, lat2, lon1, lon2):
    R = 6372800  # Rayon de la Terre en mètre
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return round((2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a)))*10**(-3), 2)


#Ouverture de notre CSV et création d'un Dataframe: ville longitude et lattitude
ville = pd.read_csv('C:/Users/Mathieu/Desktop/Villes_marchant.csv')
villes = pd.DataFrame(columns=('Ville', 'Latitude', 'Longitude'))
for i in ville.index:
    information = ville.iloc[i].str.split(';')
    data = pd.DataFrame({'Ville':information[0][0], 'Latitude':information[0][5], 'Longitude':information[0][6]}, index=(0, 1, 2))
    villes = pd.concat([villes, data[0:1]], ignore_index=True)

villes['Latitude'] = villes['Latitude'].astype(float)
villes['Longitude'] = villes['Longitude'].astype(float)



#Creation d'un Dataframe avec toutes les distances entre chaque ville
dist = pd.DataFrame(index = villes.index, columns = villes.index)
for i in dist.index:
    for j in dist.columns:
        dist[j][i] = distance(villes['Latitude'][i], villes['Latitude'][j], villes['Longitude'][i], villes['Longitude'][j])



def Visualisation_carte( Parcours, lat, long):
    fmap = folium.Map(location=[lat[Parcours[0]], long[Parcours[0]]])
    points=(len(Parcours)+1)*[0]
    for k in range(len(points)-1):
        points[k]= lat[Parcours[k]],long[Parcours[k]]
        folium.Marker(points[k]).add_to(fmap)
    points[-1]= lat[Parcours[0]], long[Parcours[0]]
    folium.PolyLine(points,  color='blue', weight=2.5, opacity=0.8).add_to(fmap)
    fmap.save('chemin2.html')
    return 0

def Representation(chemin, villes_utilisées):
    lat=len(villes_utilisées)*[0]
    long=len(villes_utilisées)*[0]
    for i in range(len(villes_utilisées)):
        lat[i]=villes_utilisées.iloc[i][1]
        long[i]=villes_utilisées.iloc[i][2]
    Visualisation_carte(chemin, lat, long)
    return 0


def Markov_Question2(itération, nbr_villes):
    villes_utilisées = villes[:nbr_villes]
   # permut = list(itt.permutations(villes_utilisées.index))
    X = random.sample(range(nbr_villes),nbr_villes)
    
    
    for n in range(0, itération):
    
        T = 2   #Température fixée pour la question 2
        g = list(X)   #g nommé sigma (ou gigma pour les intimes)
        #on créer sigma prime
        g_prime = list(X)
        k = np.random.randint(nbr_villes)
        l = np.random.randint(nbr_villes)
        
        while k == l :
            k = np.random.randint(nbr_villes)
            
        
        
        intermediaire = g_prime[k]
        g_prime[k] = g_prime[l]
        g_prime[l] = intermediaire
        
        #distance de g et distance de g_prime
        h_g = 0
        h_g_prime = 0
        d = 0
        i = 0
        while g[i] != g[-1]:
            h_g = h_g +  dist[g[i]][g[i+1]]
            h_g_prime = h_g_prime + dist[g_prime[i]][g_prime[i+1]]
            i = i+1
        
        h_g = h_g +  dist[g[-1]][g[0]] 
        h_g_prime = h_g_prime + dist[g_prime[-1]][g_prime[0]] 
        
        rau = math.exp((h_g - h_g_prime)/T)
        if(rau >= 1):
            X = g_prime
            d = h_g_prime
        else: 
            d = h_g
            U = random.uniform(0,1)
            if (U < rau): 
                X = g_prime
                d = h_g_prime
        
    print("chemin retenu:",X)
    print("Meilleure distance:", d)
    Representation(X, villes_utilisées)
    return X


Markov_Question2(100000, 30)
webbrowser.open('chemin2.html')
end = time.time()
print(end - start, "secondes d'exécution")
print(round((end - start)/60,2), "minutes d'exécution")

#print(villes)