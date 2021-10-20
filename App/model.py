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
from DISClib.DataStructures.chaininghashtable import get
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
    # Number of nationalities found through artworks interactions in large file: 64570,best = American    ||| small file: American - 451
    catalog = {}
    catalog['artists list'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['artists map'] = mp.newMap(15224,maptype='PROBING',loadfactor=0.5)
    catalog['artworks list'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['artworks list 2'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['artworks map'] = mp.newMap(150681,maptype='PROBING',loadfactor=0.5)  
    catalog['artists with ids'] = mp.newMap(15224,maptype='CHAINING',loadfactor=4) 
    catalog['ids with artists'] = mp.newMap(15224,maptype='CHAINING',loadfactor=4) 
    catalog['Mediums'] = mp.newMap(21251,maptype='CHAINING',loadfactor=4)
    catalog['Mediums list'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['nationality'] = mp.newMap(64570,maptype='CHAINING',loadfactor=4) 

    """
    METHOD 1  -----  Currently using  -----  
    catalog['artists list'] : TAD LIST SORTED BY BeginDate( ConstituentID, DisplayName, BeginDate, ArtworkNumber, MediumNumber, Gender, TopMedium  )     |||||    REQ 6,3,1  
    catalog['artists map'] : TAD MAP( ConstituentID -> ConstituentID,DisplayName, Gender, BeginDate, ArtworkNumber, MediumNumber, EndDate, Nationality, Mediums : TAD MAP(), TopMedium
                                                     , TopMedium artworks : TAD LIST SORTED BY Date(ObjectID, Date), sorted : TAD LIST( Medium, count ) ) 
                                                         |||||    REQ 6,3,1
    catalog['artworks list'] : TAD LIST SORTED BY Date( ObjectID, Date, Title, Artists : TAD LIST(DisplayName), Classification, Medium,
                                                 Dimensions, Depth (cm), Diameter (cm), Height (cm), Length (cm), Width (cm), Weight (kg) )     |||||    REQ 5
    catalog['artworks list 2'] : TAD LIST SORTED BY DateAcquired( ObjectID, ConstituentID, DateAcquired, CreditLine, Title, Artists : TAD LIST(DisplayName),
                                                                 Classification, Medium, Dimensions, Date )     |||||    REQ 2
    catalog['artworks map'] : TAD MAP(ObjectID --> ConstituentID, DateAcquired, CreditLine, Title, Artists : TAD LIST(DisplayName),
                                                                 Classification, Medium, Dimensions, Date, Department)     |||||    REQ 6,3,1
    catalog['artists with ids'] : TAD MAP( ConstituentID : DisplayName )     |||||    REQ 5,2
    catalog['ids with artists'] : TAD MAP( DisplayName : ConstituentID )     |||||    REQ 5
    catalog['Mediums'] : TAD MAP(  Medium -> count, Artworks : TAD LIST SORTED BY Date(ObjectID, Date)  )
    catalog['Mediums list'] : TAD LIST(  Medium  )
    catalog['nationality'] : TAD MAP(  Nationality -> artworks : TAD LIST( ObjectID )  )
    """
    return catalog

# Funciones para agregar informacion al catalogo

def sortData(catalog):
    # Sort catalog['artists list'] by BeginDate (YYYY)
    cmp = cmpBeginDate
    lst = catalog['artists list']
    quicksorting(lst,cmp)
    # Sort the key   'TopMedium artworks'  : catalog['artists map'] ---> (key = 'TopMedium artworks)' ; by Date for each artist
    for i in lt.iterator(catalog['artists list']):
        cmp = cmpDate
        key = i['ConstituentID']
        person = me.getValue(mp.get(catalog['artists map'],key))
        lst = person['TopMedium artworks']
        quicksorting(lst,cmp)
        # EXTRA
        addArtist_sorted(catalog,key)
        cmp = cmpCount
        lst = person['sorted']
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
    # Sort catalog['artists mediums']
    # END

def addArtist_sorted(catalog,id):
    target = me.getValue(mp.get(catalog['artists map'],id))
    meds = target['sorted']
    keys = mp.keySet(target['Mediums'])
    for i in lt.iterator(keys):
        got = me.getValue(mp.get(target['Mediums'],i))
        lt.addLast(meds,got)

def addArtwork(catalog,artwork):
    # Create artwork model that will be added to the catalog
    new1 = infoartwork_list1(artwork)
    new2 = infoartwork_list2(artwork)
    # Add artists of artwork to the artwork models created´and add 'nationality'
    artid = artwork['ConstituentID'].strip('[]').replace(' ','').split(',')
    names = lt.newList(datastructure='ARRAY_LIST')
    for i in artid:
        addArtistMedium(catalog,i,artwork)
        addArtworkArtists(catalog,names,i)
        # nationality
        nation = me.getValue(mp.get(catalog['artists map'],i))['Nationality']
        if mp.contains(catalog['nationality'],nation):
            target = me.getValue(mp.get(catalog['nationality'],nation))
            lt.addLast(target['artworks'],artwork['ObjectID'])
        else:
            new = {}
            new['artworks'] = lt.newList(datastructure='ARRAY_LIST')
            mp.put(catalog['nationality'],nation,new)
    new1['Artists'] = names
    new2['Artists'] = names
    # Artworks Lists
    lt.addLast(catalog['artworks list'],new1)
    lt.addLast(catalog['artworks list 2'],new2)
    # Artworks map
    mp.put(catalog['artworks map'],artwork['ObjectID'],new2)
    # Mediums map
    if artwork['Medium'] != '' or artwork['Medium'] != ' ':
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
    # Nationality map
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
    # Nationality
    nation = artist['Nationality'].strip()
    new = {}
    new['artworks'] = lt.newList(datastructure='ARRAY_LIST')
    mp.put(catalog['nationality'],nation,new)
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
        current = me.getValue(mp.get(person['Mediums'],key))
        if key != '':
            current['count'] += 1
    else:
        if key != '':
            new = {'Medium':key,'count':1}
            mp.put(person['Mediums'],key,new)
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
            got = me.getValue(mp.get(mediums,j))
            val = got['count']
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
        new['Date'] = artwork['Date']
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
        if new[i] == '' or new[i] == ' ':
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
    new['Department'] = artwork['Department']
    keys = new.keys()
    for i in keys:
        if new[i] == '' or new[i] == ' ':
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
    new['ConstituentID'] = artist['ConstituentID']
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
    new['sorted'] = lt.newList(datastructure='ARRAY_LIST')
    keys = new.keys()
    for i in keys:
        if new[i] == '' or new[i] == ' ':
            new[i] = 'NOT IDENTIFIED'
    return new

# Funciones de consulta

def lab5(catalog,medium,n):
    target = me.getValue(mp.get(catalog['Mediums'],medium))
    lst = target['Artworks']
    count = target['count']
    if n > lt.size(lst):
        return lst,count
    artworks = lt.subList(lst,1,n)
    return artworks,count

def lab6(catalog,nation):
    try:
        target = me.getValue(mp.get(catalog['nationality'],nation))
        lst = target['artworks']
        return lt.size(lst)
    except:
        return None

def req1(catalog,yi:int,yf:int):
    count = 0
    last1 = None # [-1]
    last2 = None # [-2]
    last3 = None # [-3]
    size = 0
    lst = lt.newList(datastructure='SINGLE_LINKED')
    for i in lt.iterator(catalog['artists list']): # O(n)
        if i['BeginDate'] != 'NOT IDENTIFIED':
            y = int(i['BeginDate'].strip())
            if y >= yi and y <= yf:
                # ADD COUNT
                count += 1
                # ADD FIRST 3 -- O(1)
                if size < 3:
                    lt.addLast(lst,me.getValue(mp.get(catalog['artists map'],i['ConstituentID'])))
                    size += 1
                # CHECK IF EMPTY FOR THE LAST 3 -- THIS WILL CONTINUE LOOP -- O(1) FOR EACH
                if last3 == None:
                    last3 = me.getValue(mp.get(catalog['artists map'],i['ConstituentID']))
                    continue
                elif last2 == None:
                    last2 = me.getValue(mp.get(catalog['artists map'],i['ConstituentID']))
                    continue
                elif last1 == None:
                    last1 = me.getValue(mp.get(catalog['artists map'],i['ConstituentID']))
                    continue
                # CHECK FOR NEW LAST AND REPLACE CURRENT ONES -- O(1) FOR EACH
                if last1!=None and last2!=None and last1!=None:
                    last3 = last2
                    last2 = last1
                    last1 = me.getValue(mp.get(catalog['artists map'],i['ConstituentID']))
    # ADD LAST 3 -- O(1) FOR EACH
    if last3 != None:
        lt.addLast(lst,last3)
    if last2 != None:
        lt.addLast(lst,last2)
    if last1 != None:
        lt.addLast(lst,last1)
    return lst,count
    # END

def req2():
    pass

def req3(catalog, name):
    # GET DEFAULTS ---- O(1) FOR EACH
    id = me.getValue(mp.get(catalog['ids with artists'],name))
    target = me.getValue(mp.get(catalog['artists map'],id))
    new = lt.newList(datastructure='SINGLE_LINKED') # ADDING LAST IS O(1) FOR LINKED LIST
    lst = target['TopMedium artworks'] # ARRAY_LIST
    size = lt.size(lst)
    # GET ELEMENTS
    if size > 6:
        # O(1) FOR EACH
        last3  = me.getValue(mp.get(catalog['artworks map'], lt.getElement(lst,size-2)['ObjectID']))
        last2 = me.getValue(mp.get(catalog['artworks map'], lt.getElement(lst,size-1)['ObjectID']))
        last1 = me.getValue(mp.get(catalog['artworks map'], lt.getElement(lst,size)['ObjectID']))
        first = me.getValue(mp.get(catalog['artworks map'], lt.getElement(lst,1)['ObjectID']))
        second = me.getValue(mp.get(catalog['artworks map'], lt.getElement(lst,2)['ObjectID']))
        third = me.getValue(mp.get(catalog['artworks map'], lt.getElement(lst,3)['ObjectID']))
        # ADD ELEMENT -- O(1) FOR EACH
        lt.addLast(new,first)
        lt.addLast(new,second)
        lt.addLast(new,third)
        lt.addLast(new,last3)
        lt.addLast(new,last2)
        lt.addLast(new,last1)
    else:
        # LOOP OF <=6 ELEMENTS -- O(1)
        for i in lt.iterator(lst):
            got = me.getValue(mp.get(catalog['artworks map'], i['ObjectID']))
            lt.addLast(new,got)
    # GET MEDIUMS AND THEIR COUNTS -- O(1)
    meds = target['sorted']
    return target,id,new,meds

def req4():
    pass

def req5():
    pass

def req6(catalog,yi,yf,n):
    count = 0
    cmp = cmpArtworkNumber
    lst = lt.newList(datastructure='SINGLE_LINKED') # LAST ELEMENTS HAVE BIGGER NUMBERS
    # ========================= CRITERIA 1 ========================= #
    big = 0
    repeated = 0
    for i in lt.iterator(catalog['artists list']): # O(n)
        try:
            y = int(i['BeginDate'].strip())
        except:
            continue
        # CHECK IF BORN IN RANGE
        if y >= yi and y <= yf:
            score = i['ArtworkNumber']
            # CHECK IF WE FIND REPEATED MAX VALUE, THEN ADD
            if score == big and big != 0:
                # WE NEED TO ADD MORE ARTISTS TO REACH n ARTISTS
                if count != n:
                    got = me.getValue(mp.get(catalog['artists map'],i['ConstituentID']))
                    lt.addLast(lst,got) # O(1)
                    count += 1
                    repeated += 1
                # WE ALREADY FOUND n ARTISTS
                else:
                    lt.removeFirst(lst) # O(1)
                    got = me.getValue(mp.get(catalog['artists map'],i['ConstituentID']))
                    lt.addLast(lst,got) # O(1)
                    count += 1
                    repeated += 1
            # CHECK IF IT'S BIGGER AND THEN REPEATED WILL BE 0 
            elif score > big:
                # WE NEED TO ADD MORE ARTISTS TO REACH n ARTISTS
                if count != n:
                    big = score
                    repeated = 0
                    got = me.getValue(mp.get(catalog['artists map'],i['ConstituentID']))
                    lt.addLast(lst,got) # O(1)
                    count += 1
                # WE ALREADY FOUND n ARTISTS
                else:
                    lt.removeFirst(lst) # O(1)
                    got = me.getValue(mp.get(catalog['artists map'],i['ConstituentID']))
                    lt.addLast(lst,got) # O(1)
                    count += 1
                    repeated = 0
    if repeated == 0: # NONE TIE
        best = lt.lastElement(lst) # O(1)
        artworks = helperREQ6(catalog,best) # O(1) IN GENERAL, BECAUSE n ISN'T TOO BIG
        quicksorting(lst,cmp)
        return lst,best,artworks
    # ____ELSE____ #
    # ========================= CRITERIA 2 ========================= #
    # WE ALREADY HAVE A RANKING, SO WE'LL USE IT TO FIND THE BEST BY MediumNumber
    big = 0
    best = None
    repeated = 0
    for j in lt.iterator(lst): # O(n from input) = O(1) in general
        score = j['MediumNumber']
        if score == big and big != 0:
            repeated += 1
        elif score > big:
            best = j
            repeated = 0
            big = score
    if repeated == 0: # NO TIE
        artworks = helperREQ6(catalog,best) # O(1) IN GENERAL, BECAUSE n ISN'T TOO BIG
        cmp = cmpMediumNumber
        quicksorting(lst,cmp)
        return lst,best,artworks
    # ____ELSE____ #
    # ========================= CRITERIA 3 ========================= #
    best = lt.lastElement(lst) # O(1)
    artworks = helperREQ6(catalog,best) # O(1) IN GENERAL, BECAUSE n ISN'T TOO BIG
    quicksorting(lst,cmp)
    return lst,best,artworks

def helperREQ6(catalog,best):
    artworks = lt.newList(datastructure='SINGLE_LINKED')
    id = best['ConstituentID']
    arts = me.getValue(mp.get(catalog['artists map'],id))['TopMedium artworks'] # O(1)
    count = 0
    for k in lt.iterator(arts): #O(artworks with TopMedium) = O(1) in general
        if count == 5:
            return artworks
        artid = k['ObjectID']
        got = me.getValue(mp.get(catalog['artworks map'],artid)) # O(1)
        lt.addLast(artworks,got) # O(1)
        count += 1
    # END

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
    if di < dj:
        return True
    elif di == dj:
        return 0
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
    if di < dj:
        return True
    elif di == dj:
        return 0
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
    elif date1 == date2:
        return 0
    return False

def cmpCount(mediumI,mediumJ):
    ci = mediumI['count']
    cj = mediumJ['count']
    if ci > cj:
        return True
    elif ci == cj:
        return 0
    return False

def cmpArtworkNumber(numberI,numberJ):
    ci = numberI['ArtworkNumber']
    cj = numberJ['ArtworkNumber']
    if ci > cj:
        return True
    elif ci == cj:
        return 0
    return False

def cmpMediumNumber(numberI,numberJ):
    ci = numberI['MediumNumber']
    cj = numberJ['MediumNumber']
    if ci > cj:
        return True
    elif ci == cj:
        return 0
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
