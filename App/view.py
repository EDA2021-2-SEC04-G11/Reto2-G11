"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf
import time

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
  print("Bienvenido")
  print("1- Listar cronologicamente los artistas - REQ 1")
  print("2- Listar cronologicamente las adquisiciones - REQ 2")
  print("3- Clasificar las obras de un artista por tecnica - REQ 3")
  print("4- Clasificar las obras por la nacionalidad de sus creadores - REQ 4")
  print("5- Transportar obras de un departamento - REQ 5")
  print("6- Listar cronologicamente las adquisiciones - REQ 6")
  print("7- Las n obras más antiguas para un medio específico - LAB 5")
  print("8- Número total de obras de una nacionalidad  - LAB 6")
  print("9- EXIT")

def charge():
  start_time = time.process_time()
  print('\n\n SE PROCEDERA A CARGAR LOS DATOS \n\n')
  print("Cargando información de los archivos ....")
  catalog = initcatalog()
  loaddata(catalog)
  print('\n\n INFORMACION CARGADA COMPLETAMENTE \n\n')
  stop_time = time.process_time()
  elapsed_time_mseg = (stop_time - start_time)*1000
  print(f"TIME : {elapsed_time_mseg}")
  return catalog

def initcatalog():
  return controller.initcatalog()

def loaddata(catalog):
  controller.loaddata(catalog)

def req1(catalog):
    # 1920 - 1985
    try:
        yi = int(input('Año inicial?\n').strip())
        yf = int(input('Año final?\n').strip())
    except:
        print('Introduce el año en un formato valido (yyyy).')
        return
    start_time = time.process_time()
    collection = controller.req1(catalog,yi,yf)
    stop_time = time.process_time()
    timef = (stop_time - start_time)*1000
    count = collection[1]
    lst = collection[0]
    print('============================ REQ #1 Answer ============================')
    print(f'There are {count} artists born between {yi} and {yf}.')
    print('The first and last 3 born in range are...\n')
    for i in lt.iterator(lst):
        print(f"DisplayName: {i['DisplayName']} || BeginDate: {i['BeginDate']} || EndDate: {i['EndDate']} || Nationality: {i['Nationality']} || Gender: {i['Gender']}\n")
    print(f"\nTIME USED: {timef}")
    print('=======================================================================')

def req2(catalog):
    pass

def req3(catalog):
    # Louise Bourgeois
    artist = input('Name of the artist?\n').strip()
    start_time = time.process_time()
    collection = controller.req3(catalog,artist)
    stop_time = time.process_time()
    timef = (stop_time - start_time)*1000
    if collection == None:
        print('Ese artista existe en otra dimension.')
        return
    target = collection[0]
    id = collection[1]
    lst = collection[2]
    meds = collection[3]
    print('============================ REQ #3 Answer ============================')
    print(f"{artist} with MoMA ID {id} has {target['ArtworkNumber']} artworks.")
    print(f"TOP {lt.size(meds)} Mediums ->\n")
    count = 1
    for i in lt.iterator(meds):
        print(f"{count}. Medium: {i['Medium'].strip()} || Count: {i['count']}\n")
        count += 1
    print('Artworks of best medium ->\n')
    for j in lt.iterator(lst):
        print(f"Title: {j['Title']} || Date: {j['Date']} || Medium: {j['Medium'].strip()} || Dimensions: {j['Dimensions']}\n")
    print(f"\nTIME USED: {timef}")
    print('=======================================================================')

def req4(catalog):
    pass

def req5(catalog):
    # Drawings & Prints
    dep = str(input('Departamento a Transferir:?\n'))
    collection = controller.req5(catalog, dep)
    #list.size(), total, pesot, top5A1, top5A2, top5C1, top5C2
    nObras = collection[0]
    costo = collection[1]
    peso = collection[2]
    T5A1 = collection[3]
    t5A2 = collection[4]
    T5C1 = collection[5]
    t5C2 = collection[6]
    print('============================ REQ #5 Answer ============================')
    print(f'Hay {nObras} en el departamento {dep}.')
    print(f'El costo total del traslado es{costo}')
    print(f'El peso aproximado de las obras a trasladar es{peso}')
    print('Las cinco obras con el costo de translado más grande son:...\n')
    f = 0
    for i in lt.iterator(T5C1):
        print(f"Title: {i['Title']} || Artist:  || 'Classification': {i['Classification']} || Date: {i['Date']} || Medium: {i['Medium']} || Dimensions: {i['Dimensions']} || Price: {t5C2[f]} ||\n")
        print('Las cinco obras más antiguas a transladar son:...\n')
    for i in lt.iterator(T5A1):
        print(f"Title: {i['Title']} || Artist:  || 'Classification': {i['Classification']} || Date: {i['Date']} || Medium: {i['Medium']} || Dimensions: {i['Dimensions']} || Price: {t5C2[f]} ||\n")
        f+=1
    print('=======================================================================')

def req6(catalog):
    # n = 7
    # 1914 - 1939
    try:
        n = int(input('Numero de artistas que desea ver?\n').strip())
        yi = int(input('Año inicial?\n').strip())
        yf = int(input('Año final?\n').strip())
    except:
        print('Introduce el año en un formato valido (yyyy).')
        return
    start_time = time.process_time()
    collection = controller.req6(catalog,yi,yf,n) # return lst,best,artworks
    stop_time = time.process_time()
    timef = (stop_time - start_time)*1000
    lst = collection[0]
    best = collection[1]
    artworks = collection[2]
    print('============================ REQ #6 Answer ============================')
    print(f"TOP {n} artistas mas prolificos ->\n")
    for i in lt.iterator(lst):
        print(f"DisplayName: {i['DisplayName']} || BeginDate: {i['BeginDate']} || Gender: {i['Gender']} ||")
        print(f"|| Artworks total: {i['ArtworkNumber']} || Mediums total: {i['MediumNumber']} || Best Medium: {i['TopMedium'].strip()}\n")
    print(f"TOP 5 artworks from the best medium of the artist {best['DisplayName']}->\n")
    for j in lt.iterator(artworks):
        print(f"Title: {j['Title']} || Date: {j['Date']} || DateAcquired: {j['DateAcquired']} || Medium: {j['Medium'].strip()} ||") 
        print(f"|| Departmment: {j['Department']} || Classification: {j['Classification']} || Dimensions: {j['Dimensions']}\n")
    print(f"\nTIME USED: {timef}")
    print('=======================================================================')

"""
Menu principal
"""
charged = False
while True:
    if not charged:
        catalog = charge()
        charged = True
    printMenu()
    inputs = input('\nSeleccione EL REQUISITO para continuar\n')
    option = int(inputs.strip()[0])
    if option == 1:
        req1(catalog)
    elif option == 2:
        req2(catalog)
    elif option == 3:
        req3(catalog)
    elif option == 4:
        req4(catalog)
    elif option == 5:
        req5(catalog)
    elif option == 6:
        req6(catalog)
    else:
        sys.exit(0)
    input('Introduce cualquier tecla para continuar...')
#sys.exit(0)
