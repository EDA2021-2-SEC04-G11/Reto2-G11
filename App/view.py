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
    print("5- Transportar obras de un departamento - REQ 5")
    print("6- Listar cronologicamente las adquisiciones - REQ 6")

def initcatalog():
    return controller.initcatalog()

def loaddata(catalog):
    controller.loaddata(catalog)

"""
Menu principal
"""

while True:
    print('\n\n SE PROCEDERA A CARGAR LOS DATOS \n\n')
    print("Cargando información de los archivos ....")
    catalog = initcatalog()
    loaddata(catalog)
    print('\n\n INFORMACION CARGADA COMPLETAMENTE \n\n')
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
    else:
        sys.exit(0)
#sys.exit(0)
