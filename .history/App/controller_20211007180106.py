﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initcatalog():
    return model.initcatalog()

# Funciones para la carga de datos

def loaddata(catalog):
    loadartists(catalog)
    loadartworks(catalog)
def loadartists(catalog):
    artistsfile = cf.data_dir + 'MoMA/Artists-utf8-large.csv'
    artistsFile = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in artistsFile:
        model.addartist(catalog,artist)
def loadartworks(catalog):
    artworksfile = cf.data_dir + 'MoMA/Artworks-utf8-large.csv'
    artworksFile = csv.DictReader(open(artworksfile, encoding='utf-8'))
    for artwork in artworksFile:
        model.addartwork(catalog,artwork)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getartworksbymedium(catalog,m):
    return model.getartworksbymedium(catalog,m)