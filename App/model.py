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
import sys
import time
from DISClib.DataStructures.arraylist import iterator
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as shellsort
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.Algorithms.Sorting import shellsort as shell
assert cf

# Construccion de modelos

def initcatalog():
    # Number of artists in large file: 15224
    # Number of artworks in large file: 150681
    # Number of mediums in large file: 21251     ||| In small file: 383
    # Number of max mediums for an artist in large file: 352, id: 41829
    catalog = {
        'artists list':None,
        'artists map':None,
        'artworks list':None,
        'artworks list 2':None,
        'artworks map':None,
        'artists with ids':None,
        'ids with artists':None,
        'Mediums': None
    }
    catalog['artists list'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['artists map'] = mp.newMap(15224,maptype='PROBING',loadfactor=0.5)
    catalog['artworks list'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['artworks list 2'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['artworks map'] = mp.newMap(150681,maptype='PROBING',loadfactor=0.5)  
    catalog['artists with ids'] = mp.newMap(15224,maptype='PROBING',loadfactor=0.5) 
    catalog['ids with artists'] = mp.newMap(15224,maptype='PROBING',loadfactor=0.5) 
    catalog['Mediums'] = mp.newMap(21251,maptype='PROBING',loadfactor=0.5)
    catalog['Mediums list'] = lt.newList(datastructure='ARRAY_LIST')

    """
    METHOD 1  -----  Currently using  -----  
    catalog['artists list'] : TAD LIST SORTED BY BeginDate( ConstituentID, DisplayName, BeginDate, ArtworkNumber, MediumNumber  )     |||||    REQ 6,3,1  
    catalog['artists map'] : TAD MAP( ConstituentID -> DisplayName, Gender, BeginDate, ArtworkNumber, MediumNumber, EndDate, Nationality, Mediums : TAD MAP(), TopMedium
                                                     , TopMedium artworks : TAD LIST SORTED BY DateAcquired(ObjectID, DateAcquired) )     |||||    REQ 6,3,1
    catalog['artworks list'] : TAD LIST SORTED BY Date( ObjectID, Date, Title, Artists : TAD LIST(DisplayName), Classification, Medium,
                                                 Dimensions, Depth (cm), Diameter (cm), Height (cm), Length (cm), Width (cm), Weight (kg) )     |||||    REQ 5
    catalog['artworks list 2'] : TAD LIST SORTED BY DateAcquired( ObjectID, ConstituentID, DateAcquired, CreditLine, Title, Artists : TAD LIST(DisplayName),
                                                                 Classification, Medium, Dimensions, Date )     |||||    REQ 2
    catalog['artworks map'] : TAD MAP(ObjectID --> ConstituentID, DateAcquired, CreditLine, Title, Artists : TAD LIST(DisplayName),
                                                                 Classification, Medium, Dimensions, Date)     |||||    REQ 6,3,1
    catalog['artists with ids'] : TAD MAP( ConstituentID : DisplayName )     |||||    REQ 5,2
    catalog['ids with artists'] : TAD MAP( DisplayName : ConstituentID )     |||||    REQ 5
    catalog['Mediums'] : TAD MAP(  Medium -> count, Artworks : TAD LIST SORTED BY Date(ObjectID, Date)  )
    catalog['Mediums list'] : TAD LIST(  Medium: None  )
    """
    return catalog

# Funciones para agregar informacion al catalogo

def sortData(catalog):
    # Sort catalog['artists list'] by BeginDate (YYYY)
    cmp = cmpBeginDate
    lst = catalog['artists list']
    quicksorting(lst,cmp)
    # Sort the key   'TopMedium artworks'  : catalog['artists map'] ---> (key = 'TopMedium artworks)' ; by DateAcquired (YYYY-MM-DD) for each artist
    cmp = cmpDateAcquired
    for i in lt.iterator(catalog['artists list']):
        key = i['ConstituentID']
        person = me.getValue(mp.get(catalog['artists map'],key))
        lst = person['TopMedium artworks']
        quicksorting(lst,cmp)
    # Sort catalog['artworks list'] by Date
    cmp = cmpDate
    lst = catalog['artworks list']
    quicksorting(lst,cmp) 
    # Sort catalog['artworks list 2'] by DateAcquired
    cmp = cmpDateAcquired
    lst = catalog['artworks list 2']
    quicksorting(lst,cmp) 
    # Sort 'Artworks' key for each catalog['Mediums'] element in catalog
    cmp = cmpDate
    for i in lt.iterator(catalog['Mediums list']):
        target = me.getValue(mp.get(catalog['Mediums'],i))
        lst = target['Artworks']
        quicksorting(lst,cmp)
    for j in lt.iterator(catalog['Mediums list']):
        target = me.getValue(mp.get(catalog['Mediums'],j))
    # END

def addArtwork(catalog,artwork):
    # Create artwork model that will be added to the catalog
    new1 = infoartwork_list1(artwork)
    new2 = infoartwork_list2(artwork)
    # Add artists of artwork to the artwork models created
    artid = artwork['ConstituentID'].strip('[]').replace(' ','').split(',')
    names = lt.newList(datastructure='ARRAY_LIST')
    for i in artid:
        addArtistMedium(catalog,i,artwork)
        addArtworkArtists(catalog,names,i)
    new1['Artists'] = names
    new2['Artists'] = names
    # Artworks Lists
    lt.addLast(catalog['artworks list'],new1)
    lt.addLast(catalog['artworks list 2'],new2)
    # Artworks map
    mp.put(catalog['artworks map'],artwork['ObjectID'],new2)
    # Mediums map
    if artwork['Medium'] != '':
        if not mp.contains(catalog['Mediums'],artwork['Medium']):
            lt.addLast(catalog['Mediums list'],artwork['Medium'])
            new = infoMediums()
            mp.put(catalog['Mediums'],artwork['Medium'],new)
        target = me.getValue(mp.get(catalog['Mediums'],artwork['Medium']))
        target['count'] += 1
        new = {}
        new['ObjectID'] = artwork['ObjectID']
        new['Date'] = artwork['Date']
        keys = new.keys()
        for i in keys:
            if new[i] == '':
                new[i] = 'NOT IDENTIFIED'
        lt.addLast(target['Artworks'],new)
    # END

def addArtist(catalog,artist):
    # artists list
    new = infoartist_list(artist)
    lt.addLast(catalog['artists list'],new)
    # artists map
    new = infoartist_map(artist)
    artistid = artist['ConstituentID'].strip('[]').replace(' ','')
    mp.put(catalog['artists map'], artistid,new)
    addArtist_id(catalog,artist)
    # END

def addArtist_id(catalog,artist):
    mp.put(catalog['artists with ids'],artist['ConstituentID'],artist['DisplayName'])
    mp.put(catalog['ids with artists'],artist['DisplayName'],artist['ConstituentID'])

def addArtistMedium(catalog,artistid,artwork):
    # Add medium count
    en = mp.get(catalog['artists map'],artistid)
    person = me.getValue(en)
    key = artwork['Medium']
    if mp.contains(person['Mediums'],key):
        entry = mp.get(person['Mediums'],key)
        current = me.getValue(entry)
        if key != '':
            mp.put(person['Mediums'],key,current+1)
    else:
        if key != '':
            mp.put(person['Mediums'],key,1)
    # Add ArtworkNumber to artists map
    person['ArtworkNumber'] += 1   # MAP

def addTopMedium(catalog):
    # RUNS AFTER ALL FILES ARE LOADED AND AFTER addArtistMedium()
    for i in lt.iterator(catalog['artists list']):
        # Add MediumNumber to artists list and map
        personID = i['ConstituentID'].strip()
        person = me.getValue(mp.get(catalog['artists map'],personID))
        mediums = person['Mediums']
        person['MediumNumber'] = mp.size(mediums)     # MAP
        i['MediumNumber'] = mp.size(mediums)         # LIST
        # Add TopMedium to map
        keys = mp.keySet(mediums)
        big = 0
        best = None
        for j in lt.iterator(keys):
            val = me.getValue(mp.get(mediums,j))
            if val >= big:
                big = val
                best = j
        person['TopMedium'] = best
        # Add TopMedium artworks to map and add Medium to Mediums list
        for artwork in lt.iterator(catalog['artworks list 2']):
            addTopMediumArtworks(artwork,person,best,personID)
            #mp.put(catalog['Mediums map'],artwork['Medium'],None)
        # Add ArtworkNumber to list
        i['ArtworkNumber'] = person['ArtworkNumber']

def addTopMediumArtworks(artwork,person,best,artistID):
    artid = artwork['ConstituentID'].strip('[]').replace(' ','').split(',')
    if artwork['Medium'] == best and artistID in artid:
        new = {}
        new['ObjectID'] = artwork['ObjectID']
        new['DateAcquired'] = artwork['DateAcquired']
        keys = new.keys()
        for i in keys:
            if new[i] == '':
                new[i] = 'NOT IDENTIFIED'
        lt.addLast(person['TopMedium artworks'],new)

def addArtworkArtists(catalog,names,artid):
    name = me.getValue(mp.get(catalog['artists with ids'],artid))
    lt.addLast(names,name)

# Funciones para creacion de datos

def infoMediums():
    new = {}
    new['count'] = 0
    new['Artworks'] = lt.newList(datastructure='ARRAY_LIST')
    return new

def infoartwork_list1(artwork):
    new = {}
    new['ObjectID'] = artwork['ObjectID']
    new['Date'] = artwork['Date']
    new['Title'] = artwork['Title']
    new['Artists'] = lt.newList(datastructure='ARRAY_LIST')
    new['Classification'] = artwork['Classification']
    new['Medium'] = artwork['Medium']
    new['Dimensions'] = artwork['Dimensions']
    new['Depth (cm)'] = artwork['Depth (cm)']
    new['Weight (kg)'] = artwork['Weight (kg)']
    new['Height (cm)'] = artwork['Height (cm)']
    new['Length (cm)'] = artwork['Length (cm)']
    new['Width (cm)'] = artwork['Width (cm)']
    new['Diameter (cm)'] = artwork['Diameter (cm)']
    keys = new.keys()
    for i in keys:
        if new[i] == '':
            new[i] = 'NOT IDENTIFIED'
    return new
    
def infoartwork_list2(artwork):
    new = {}
    new['ObjectID'] = artwork['ObjectID']
    new['ConstituentID'] = artwork['ConstituentID']
    new['DateAcquired'] = artwork['DateAcquired']
    new['CreditLine'] = artwork['CreditLine']
    new['Title'] = artwork['Title']
    new['Artists'] = lt.newList(datastructure='ARRAY_LIST')
    new['Classification'] = artwork['Classification']
    new['Medium'] = artwork['Medium']
    new['Dimensions'] = artwork['Dimensions']
    new['Date'] = artwork['Date']
    keys = new.keys()
    for i in keys:
        if new[i] == '':
            new[i] = 'NOT IDENTIFIED'
    return new

def infoartist_list(artist):
    new = {}
    new['ConstituentID'] = artist['ConstituentID']
    new['DisplayName'] = artist['DisplayName']
    new['BeginDate'] = artist['BeginDate']
    new['ArtworkNumber'] = 0
    new['MediumNumber'] = 0
    keys = new.keys()
    for i in keys:
        if new[i] == '':
            new[i] = 'NOT IDENTIFIED'
    return new

def infoartist_map(artist):
    new = {}
    new['DisplayName'] = artist['DisplayName']
    new['Gender'] = artist['Gender']
    new['BeginDate'] = artist['BeginDate']
    new['ArtworkNumber'] = 0
    new['MediumNumber'] = 0
    new['EndDate'] = artist['EndDate']
    new['Nationality'] = artist['Nationality']
    new['TopMedium'] = None
    new['TopMedium artworks'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction= cmpDateAcquired)
    mediums = mp.newMap(3,maptype='PROBING',loadfactor=0.5)   #352
    new['Mediums'] = mediums
    keys = new.keys()
    for i in keys:
        if new[i] == '':
            new[i] = 'NOT IDENTIFIED'
    return new

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpDate(artworkI, artworkJ):
    # Compares the artwork['Date']; artworkI, artworkJ are artwork elements
    if artworkI['Date'] != '' and artworkI['Date'] != 'NOT IDENTIFIED':
        di = int(artworkI['Date'].strip())
    else:
        di = int(datetime.date.today().year)
    if artworkJ['Date'] != '' and artworkJ['Date'] != 'NOT IDENTIFIED':
        dj = int(artworkJ['Date'].strip())
    else:
        dj = int(datetime.date.today().year)
    if di <= dj:
        return True
    return False

def cmpBeginDate(artistI, artistJ):
    # Compares the artist['BeginDate']; artistI, artistJ are artist elements
    if artistI['BeginDate'] != '' and artistI['BeginDate'] != 'NOT IDENTIFIED':
        di = int(artistI['BeginDate'].strip())
    else:
        di = int(datetime.date.today().year)
    if artistJ['BeginDate'] != '' and artistJ['BeginDate'] != 'NOT IDENTIFIED':
        dj = int(artistJ['BeginDate'].strip())
    else:
        dj = int(datetime.date.today().year)
    if di > dj:
        return True
    return False
def cmpDateAcquired(artworkI,artworkJ):
    # year-month-day
    if artworkI['DateAcquired'] != '' and artworkI['DateAcquired'] != 'NOT IDENTIFIED':
        date1 = datetime.date.fromisoformat(artworkI['DateAcquired'])
    else:
        date1 = datetime.date.today()
    if artworkJ['DateAcquired'] != '' and artworkJ['DateAcquired'] != 'NOT IDENTIFIED':
        date2 = datetime.date.fromisoformat(artworkJ['DateAcquired'])
    else:
        date2 = datetime.date.today()
    #print(f"{date1} < {date2} = {date1 < date2}")
    if date1 < date2:
        return True
    return False

def isoformat(datei,datej):
    yi,mi,di = datei.year,datei.month,datei.day
    yj,mj,dj = datej.year,datej.month,datej.day
    if yi < yj:
        return True
    elif yi == yj:
        if mi < mj:
            return True
        elif mi == mj:
            if di <= dj:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


# Funciones de ordenamiento

def insertionsorting(lst, cmp):
    start_time = time.process_time()
    sortedL = insertion.sort(lst,cmp)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return (sortedL, f'time: {elapsed_time_mseg}')

def mergesorting(lst, cmp):
    start_time = time.process_time()
    sortedL = merge.sort(lst, cmp)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return (sortedL, f'time: {elapsed_time_mseg}')
     
def quicksorting(lst, cmp):
    start_time = time.process_time()
    sortedL = quick.sort(lst, cmp)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return (sortedL, f'time: {elapsed_time_mseg}')
    
def shellsorting(lst, cmp):
    start_time = time.process_time()
    sortedL = shell.sort(lst, cmp)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return (sortedL, f'time: {elapsed_time_mseg}')



"""
def test_one(catalog):
    # Tests catalog['artists map']
    j = 0
    for i in lt.iterator(catalog['artists list']):
        artistID = i['ConstituentID']
        person = mp.get(catalog['artists map'],artistID)['value']
        if j == 5: # Test for the #j artist (no order in special)
            print('------------------------------------------------------------------')
            print(f"\n\nTESTING FOR THE ARTIST: {artistID} - {i['DisplayName']}")
            print('__________________________________________________________________')
            print('\nMediums:')
            mkeys = mp.keySet(person['Mediums'])
            valsum = 0
            for j in lt.iterator(mkeys):
                mentry = mp.get(person['Mediums'],j)
                key = mentry['key']
                val = mentry['value']
                valsum += val
                print(f"ArtistID - {artistID}  :  {key}  :  {val}")
            print(f"SUM OF MEDIUMS VALUES = {valsum}")
            print('__________________________________________________________________')
            print('\nTopMedium:')
            print(f"TOP  :  {person['TopMedium']}")
            print('__________________________________________________________________')
            print('\nTopMedium artworks:')
            for k in lt.iterator(person['TopMedium artworks']):
                temp = mp.get(catalog['artworks map'],k['ObjectID'])['value']['ConstituentID']
                artid = temp.strip('[]').replace(' ','').split(',')
                print(f"ObjectID - {k['ObjectID']}  :  {k['DateAcquired']}  :  ARTISTS ARE SHOWN BELOW -->")
                for l in artid:
                    name = mp.get(catalog['artists with ids'],l)['value']
                    print(f'ARTIST: {name} --- {l}')
            print('__________________________________________________________________')
            print(f"\nMediumNumber = {person['MediumNumber']}")
            print(f"ArtworkNumber = {person['ArtworkNumber']}")
            print('------------------------------------------------------------------')
            break
        j += 1
    # END
"""
