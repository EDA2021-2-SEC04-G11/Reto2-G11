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
import datetime

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
    # 1944-06-06 and 1989-11-09
    try:
        di = datetime.date.fromisoformat(input('Fecha de Adquisicion Inicial?\n').strip())
        df = datetime.date.fromisoformat(input('Fecha de Adquisicion Final?\n').strip())
    except:
        print('Introduce el año en un formato valido (yyyy-mm-dd).')
        return
    start_time = time.process_time()
    collection = controller.req2(catalog,di,df)
    stop_time = time.process_time()
    timef = (stop_time - start_time)*1000
    lst = collection[0]
    count = collection[1]
    co = collection[2]
    print('============================ REQ #2 Answer ============================')
    print(f'Hay {count} adquiridas entre la fecha {di} y la fecha {df}.')
    print(f'El número de obras adquiridas por la forma Purchase son {co}')
    print('Las tres primeras y las tres ultimas obras dentro del rango son:...')
    for i in lt.iterator(lst):
        print('=======================================================================')
        print(f"Title: {i['Title']}\n") 
        print(f"Artist: {i['Artists']['elements']}\n")
        print(f"DateAcquired: {i['DateAcquired']} || Medium: {i['Medium']} || Dimensions: {i['Dimensions']}")
    print(f"\nTIME USED: {timef}")
    print('=======================================================================')


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

    collection = controller.req4(catalog)

    n = collection[0]
    top3 = collection[1]
    print('============================ REQ #3 Answer ============================')
    i = 0
    while i < 10:
      print('=======================================================================')
      print(f"Nacionalidad: {n['i']}\n") 
      i+=1

    print('=======================================================================')

    pass

def req5(catalog):
    # Drawings & Prints
    dep = input('Departamento a Transferir?\n')
    start_time = time.process_time()
    collection = controller.req5(catalog, dep)
    stop_time = time.process_time()
    timef = (stop_time - start_time)*1000
    total_cost = collection[0]
    weight = collection[1]
    count = collection[2]
    leaderboard = collection[3]
    oldest = collection[4]
    print('============================ REQ #5 Answer ============================')
    print(f'Hay {count} en el departamento {dep}.')
    print(f'El costo total del traslado es {round(total_cost,2)}')
    print(f'El peso aproximado de las obras a trasladar es {round(weight,2)} kg')
    print('Las cinco obras con el costo de translado más grande son (de menor a mayor):...\n')
    for i in lt.iterator(leaderboard):
        print(f"Title: {i['Title']} || Artist -->")
        for j in lt.iterator(i['Artists']):
            print(j)
        print(f"|| 'Classification': {i['Classification']} || Date: {i['Date']} || Medium: {i['Medium']} || Dimensions: {i['Dimensions']} || Price: {i['price']}\n")
    print('Las cinco obras más antiguas a transladar son:...\n')
    for i in lt.iterator(oldest):
        print(f"Title: {i['Title']} || Artist -->")
        for j in lt.iterator(i['Artists']):
            print(j)
        print(f"|| 'Classification': {i['Classification']} || Date: {i['Date']} || Medium: {i['Medium']} || Dimensions: {i['Dimensions']} || Price: {i['price']}\n")
    print(f"\nTIME USED: {timef}")
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
