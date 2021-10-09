"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import datetime
import time
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.Algorithms.Sorting import shellsort as shell
assert cf

# Construccion de modelos

def initcatalog():
    # Number of artists in large file: 15224
    # Number of artworks in large file: 150681
    # Number of mediums in large file: 21251
    catalog = {
        'artworks':None,
        'mediums':None,
        'artists with artworks':None
    }
    catalog['artworks'] = mp.newMap(150681,maptype='PROBING',loadfactor=0.5,comparefunction=comparedateadquisition)  
    catalog['mediums'] = mp.newMap(21251,comparefunction=comparemedium,maptype='PROBING',loadfactor=0.5)
    catalog['artists with artworks'] = mp.newMap(15224,maptype='PROBING',loadfactor=0.5,comparefunction=compareartistid)  
    """
    METHOD 1  -----  Currently using  -----  
    catalog['artists list'] : TAD LIST SORTED BY BeginDate( DisplayName, BeginDate, ArtworkNumber, MediumNumber  )     |||||    REQ 6,3,1
    catalog['artists map'] : TAD MAP( DisplayName -> Gender, BeginDate, ArtworkNumber, MediumNumber, EndDate, Nationality, TopMedium
                                                     , TopMedium artworks : TAD LIST SORTED BY DateAcquired(ObjectID, DateAcquired) )     |||||    REQ 6,3,1
    catalog['artworks list'] : TAD LIST SORTED BY Date( ObjectID, Date, Depth (cm), Diameter (cm), Height (cm), Length (cm), Width (cm), Weight (kg) )     |||||    REQ 5
    catalog['artworks list for req 2'] : TAD LIST SORTED BY DateAcquired( ObjectID, DateAcquired )     |||||    REQ 2
    catalog['artworks map'] : TAD MAP( ObjectID -> Title, ArtistsFromIDs, Classification, Medium, Dimensions )     |||||    REQ 5,2
    catalog['artists with ids'] : TAD MAP( ConstituentID : DisplayName )     |||||    REQ 5,2
    """
    return catalog

# Funciones para agregar informacion al catalogo

def addartist(catalog,artist):
    new = newartist()
    infoartist(new,artist)
    lt.addLast(catalog['artists'],new)

def addartwork(catalog,artwork):
    new = newartwork()
    infoartwork(new,artwork)
    lt.addLast(catalog['artworks'],new)
    ispresent = mp.contains(catalog['mediums'],artwork['Medium'])
    if not ispresent:
        addmedium(catalog,artwork)
    addartworkmedium(catalog,artwork)

def addmedium(catalog, artwork):
    newtag = newmedium(artwork['Medium'])
    mp.put(catalog['mediums'], artwork['Medium'], newtag)

def addartworkmedium(catalog, artwork):
    medium = artwork['Medium']
    entry = mp.get(catalog['mediums'], medium)
    if entry:
        artworkmedium = mp.get(catalog['mediums'], me.getValue(entry)['name'])
        artworkmedium['value']['total_artworks'] += 1
        lt.addLast(artworkmedium['value']['artworks'], artwork)

def infoartist(new,artist):
    new['DisplayName'] = artist['DisplayName']
    new['Nationality'] = artist['Nationality']
    new['Gender'] = artist['Gender']
    new['BeginDate'] = artist['BeginDate']
    new['ConstituentID'] = artist['ConstituentID']

def infoartwork(new,artwork):
    new['ObjectID'] = artwork['ObjectID']
    new['Title'] = artwork['Title']
    new['DateAcquired'] = artwork['DateAcquired']
    new['Medium'] = artwork['Medium']
    new['Dimensions'] = artwork['Dimensions']
    new['ConstituentID'] = artwork['ConstituentID']
    new['Weight (kg)'] = artwork['Weight (kg)']
    new['Height (cm)'] = artwork['Height (cm)']
    new['Length (cm)'] = artwork['Length (cm)']
    new['Width (cm)'] = artwork['Width (cm)']
    new['Diameter (cm)'] = artwork['Diameter (cm)']
    new['Department'] = artwork['Department']
    new['Classification'] = artwork['Classification']
    new['Date'] = artwork['Date']
    new['CreditLine'] = artwork['CreditLine']

# Funciones para creacion de datos

def newartist():
    new = {'name':None,'nationality':None,'gender':None,'birthday':None,'ID':None,'deathday':None,}
    return new
def newartwork():
    new = {'Title':None,'DateAcquired':None,'Medium':None,'Dimensions':None,'artistID':None,
    'Weight (kg)':None,'Height (cm)':None,'Length (cm)':None,'Width (cm)':None, 'Department':None,'costo transporte':None,
     'Classification':None, 'Date':None, 'CreditLine':None, 'ObjectID':None}
    return new
def newmedium(name):
    """
    Esta estructura crea una relación entre un tag y los libros que han sido
    marcados con dicho tag.  Se guarga el total de libros y una lista con
    dichos libros.
    """
    medium = {'name': '',
           'total_artworks': 0,
           'artworks': None}
    medium['name'] = name
    medium['artworks'] = lt.newList()
    return medium

# Funciones de consulta

def getartworksbymedium(catalog,medium):
    entry = mp.get(catalog['mediums'],medium)
    artworksbymedium = me.getValue(entry)['artworks']
    mergesorting(artworksbymedium,'artworks')
    return artworksbymedium

# Funciones utilizadas para comparar elementos dentro de una lista

def comparemedium(keymedium,medium):
    mediumentry = me.getKey(medium)
    if (keymedium == mediumentry):
        return 0
    elif (keymedium > mediumentry):
        return 1
    else:
        return -1
def compareartistid(id1,id2):
    year1 = id1['ConstituentID']
    year2 = id2['ConstituentID']
    d1 = datetime.date.fromisoformat(f'{year1}-01-01')
    d2 = datetime.date.fromisoformat(f'{year2}-01-01')
    ret = False
    if d1 < d2:
        ret = True
    return ret
def comparedateadquisition(artwork1,artwork2):
    ret = False
    if artwork1['DateAcquired'] != '' :
        date1 = datetime.date.fromisoformat(artwork1['DateAcquired'])
    else:
        date1 = datetime.date.today()
    if artwork2['DateAcquired'] != '':
        date2 = datetime.date.fromisoformat(artwork2['DateAcquired'])
    else:
        date2 = datetime.date.today()
    if date1 < date2:
        ret = True
    return ret

# Funciones de ordenamiento

def insertionsorting(lst, target):
    cmpfunction = comparedateadquisition
    if target == 'artists':
        cmpfunction = compareartistid
    start_time = time.process_time()
    ordenada = insertion.sort(lst,cmpfunction)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return (ordenada, f'time: {elapsed_time_mseg}')

def mergesorting(lst, target):
    cmpfunction = comparedateadquisition
    if target == 'artists':
        cmpfunction = compareartistid
    start_time = time.process_time()
    ordenada = merge.sort(lst, cmpfunction)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return (ordenada, f'time: {elapsed_time_mseg}')
     
def quicksorting(lst, target):
    cmpfunction = comparedateadquisition
    if target == 'artists':
        cmpfunction = compareartistid
    start_time = time.process_time()
    ordenada = quick.sort(lst, cmpfunction)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return (ordenada, f'time: {elapsed_time_mseg}')
    
def shellsorting(lst, target):
    cmpfunction = comparedateadquisition
    if target == 'artists':
        cmpfunction = compareartistid
    start_time = time.process_time()
    ordenada = shell.sort(lst, cmpfunction)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return (ordenada, f'time: {elapsed_time_mseg}')



"""
REQ 1: 
    Find artists born in a specific range of years
        PRINT:  Total artists born in range  
                |  for the initial 3 and last 3 -> (DisplayName, BeginDate, EndDate, Nationality, Gender)
REQ 2: 
    Find artworks adquired in a specific range of date
        PRINT:  Total artworks adquired in range  |  Total artworks such that ("pucharse" in artwork["CreditLine"])  
                |  for the 3 artists with the most artworks and 3 artists with the least artworks -> (Title, Artists transformed from ConstituentID's,
                DateAcquired, Medium, Dimensions)
REQ 3: 
    Artworks classification of an artists by medium
        PRINT:  Total artist's artworks  |  Total mediums used  |  Most used technique  
                |  for the initial 3 and last 3 -> (Title, DateAcquired, Medium, Dimensions)
REQ 5: 
    Transport artworks of a department
        PRINT: Total artworks to transport  |  Stimated price of service  |  Stimated weigh of service  
                |  for the most ancient 5 and most expensive 5 -> (Title, Artists transformed from ConstituentID's, Classification, DateAcquired, Medium, Dimensions,
                Cost of transportation)
REQ 6: 
    Find the best n (input) prolific artists in the classification in a range of years
        PRINT:  For each artist -> (Total artworks, Total mediums used, Most used Medium,
                For the first 5 artworks of that artist with the most used Medium -> (Title, DateAcquired, Medium, Dimensions)
"""