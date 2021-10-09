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


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Las n obras mas antiguas para un medio especifico")

def initcatalog():
    return controller.initcatalog()

def loaddata(catalog):
    controller.loaddata(catalog)

def getartworksbymedium(catalog,m):
    return controller.getartworksbymedium(catalog,m)

def printartworksbymedium(artworksbymedium):
    # Lithograph
    for i in lt.iterator(artworksbymedium):
        print(f"TITLE: {i['Title']}  |  OBJECTID: {i['ObjectID']}  |  MEDIUM: {i['Medium']}")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initcatalog()
        loaddata(catalog)

    elif int(inputs[0]) == 2:
        m = input('Medio:\n')
        n = input('Valor de n:\n')
        n = int(n.strip())
        artworksbymedium = getartworksbymedium(catalog,m)
        printartworksbymedium(artworksbymedium)


    else:
        sys.exit(0)
sys.exit(0)

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
                For the first 5 artworks of that artist with the most used Medium -> (Title, DateAcquired, Medium, Dimensions))
"""