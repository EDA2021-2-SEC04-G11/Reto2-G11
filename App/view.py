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
    print("7- las n obras más antiguas para un medio específico - LAB 5")
    print("8- Número total de obras de una nacionalidad  - LAB 6")
    print("1- Listar cronologicamente los artistas - REQ 1")
    print("2- Listar cronologicamente las adquisiciones - REQ 2")
    print("3- Clasificar las obras de un artista por tecnica - REQ 3")
    print("5- Transportar obras de un departamento - REQ 5")
    print("6- Listar cronologicamente las adquisiciones - REQ 6")

def initcatalog():
    return controller.initcatalog()

def loaddata(catalog):
    controller.loaddata(catalog)

def lab5(catalog):
    start_time = time.process_time()
    medium = input('Medio?\n').strip()
    n = int(input('Cuantas obras?\n').strip())
    collection = controller.lab5(catalog,medium,n)   # Returns (TAD LIST,int)
    artworks = collection[0]
    count = collection[1] 
    print(f'\nSe encontraron {count} obras en el medio {medium}.')
    for i in lt.iterator(artworks):
        print(f"ObjectID = {i['ObjectID']} || Date = {i['Date']}")
    print('\n')
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print(f"TIME : {elapsed_time_mseg}")
    # END

def lab6(catalog):
    start_time = time.process_time()
    nation = input('Nacionalidad?\n').strip()
    count = controller.lab6(catalog,nation)
    if count == None:
        print('\nDesafortunadamente no se encontro esa nacionalidad.\n')
        return
    print(f'\nSe encontraron {count} obras con la nacionalidad dada.\n')
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print(f"TIME : {elapsed_time_mseg}")

"""
Menu principal
"""
charged = False
while True:
    if not charged:
        start_time = time.process_time()
        print('\n\n SE PROCEDERA A CARGAR LOS DATOS \n\n')
        print("Cargando información de los archivos ....")
        catalog = initcatalog()
        loaddata(catalog)
        charged = True
        print('\n\n INFORMACION CARGADA COMPLETAMENTE \n\n')
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(f"TIME : {elapsed_time_mseg}")
    printMenu()
    inputs = input('Seleccione EL REQUISITO para continuar\n')
    if int(inputs[0]) == 1:
        pass
    elif int(inputs[0]) == 2:
        pass
    elif int(inputs[0]) == 3:
        pass
    elif int(inputs[0]) == 5:
        pass
    elif int(inputs[0]) == 6:
        pass
    elif int(inputs[0]) == 7:
        lab5(catalog)
    elif int(inputs[0]) == 8:
        lab6(catalog)
    else:
        sys.exit(0)
#sys.exit(0)
