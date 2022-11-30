# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 11:41:24 2022

@author: Mathieu
"""


import pandas as pd
import itertools as itt
import math
import folium
import webbrowser
import time
start = time.time()

#Fonction permettant de trouver la distance entre deux villes selon leur lattitudes et longitudes
def distance(lat1, lat2, lon1, lon2):
    R = 6372800  # Rayon de la Terre en mètre
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return round((2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a)))*10**(-3), 2)

                          
def distance_totale(permut, lat, long):
    distances=len(permut)*[0]
    parcours=len(permut)*[0]
    for i in range(len(permut)):
        #d est la distance pour chaque permut, donc remise à zéro quand on change de permut.
        d=0
        for j in range (1,len(permut[i])):
            #incrémentation de d avec la distance entre chaque point
            d= d+distance(lat[permut[i][j-1]], lat[permut[i][j]], long[permut[i][j-1]], long[permut[i][j]])
            distances[i]=d
        #Ligne permettant de relier le dernier point au point de départ pour boucler le chemin
        distances[i] = round(distances[i] + distance(lat[permut[i][j]], lat[permut[i][0]], long[permut[i][j]], long[permut[i][0]]),2)
        parcours[i] = permut[i]
    return distances, parcours

def min_distance(distance_totale):
    d_opti=distance_totale[0][0]
    p_opti=distance_totale[1][0]
    e=0
    for i in range(1,len(distance_totale[0])):
        #Comparaison de toutes les distances avec le minimum
        if (distance_totale[0][i]<d_opti):
            d_opti =distance_totale[0][i]
            p_opti = distance_totale[1][i]      
    return d_opti, p_opti

def Visualisation_carte( distance_totale, lat, long):
    mini = min_distance(distance_totale)
    fmap = folium.Map(location=[lat[mini[1][0]], long[mini[1][0]]])
    points=(len(mini[1])+1)*[0]
    for k in range(len(points)-1):
        points[k]= lat[mini[1][k]],long[mini[1][k]]
        folium.Marker(points[k]).add_to(fmap)
    points[-1]= lat[mini[1][0]], long[mini[1][0]]
    folium.PolyLine(points,  color='blue', weight=2.5, opacity=0.8).add_to(fmap)
    fmap.save('chemin.html')
    return 0




def chemin_opti(echant_villes):
    ville = pd.read_csv('C:/Users/Mathieu/Desktop/Villes_marchant.csv')

    villes = pd.DataFrame(columns=('Ville', 'Latitude', 'Longitude'))

    for i in ville.index:
        information = ville.iloc[i].str.split(';')
        data = pd.DataFrame({'Ville':information[0][0], 'Latitude':information[0][5], 'Longitude':information[0][6]}, index=(0, 1, 2))
        villes = pd.concat([villes, data[0:1]], ignore_index=True)

    villes['Latitude'] = villes['Latitude'].astype(float)
    villes['Longitude'] = villes['Longitude'].astype(float)
    
    lat=len(villes)*[0]
    long=len(villes)*[0]
    num_V =echant_villes*[0]
    for i in range(len(villes)):
        lat[i]=villes.iloc[i][1]
        long[i]=villes.iloc[i][2]
    for j in range(echant_villes):
        num_V[j]= j
    permut = list(itt.permutations(num_V))
    distances = (distance_totale(permut, lat, long))
    Visualisation_carte(distances, lat, long)
    print(min_distance(distances)[0], "km")
    print("meilleur parcours:", min_distance(distances)[1])
    return 0

chemin_opti(10)


webbrowser.open('chemin.html')
end = time.time()
print(end - start, "secondes d'exécution")
print(round((end - start)/60,2), "minutes d'exécution")
