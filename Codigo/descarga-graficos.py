# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:11:54 2018

@author: victor
"""


#importamos todas las librerías que se van a utilizar
from bs4 import BeautifulSoup
import requests
import csv
import urllib2
import datetime
import time
import urllib

url = 'https://www.eleconomista.es/indices-mundiales/'
response = urllib2.urlopen(url)
soup0 = response.read()
soup = BeautifulSoup(soup0, 'lxml')


#inicializamos las listas donde guardaremos las url de las imagenes y sus títulos

url_imagenes = []
titulos_imagenes = []

#capturamos todas las url de las imágenes y sus títulos
for imagen in soup.find_all('div', class_ = 'caja2'):
    url_imagenes.append('http:' + imagen.a.img['src'])
    titulos_imagenes.append(imagen.a.img['title'])

#obtenemos el timestamp y lo formateamos
    
fecha_actual = str(datetime.datetime.now())
fecha_actual = fecha_actual[8:10] + '-' + fecha_actual[5:7] + '-' + fecha_actual[0:4]


#descargamos y guardamos las imágenes
for i in range(0,len(url_imagenes)):
    resource = urllib.urlopen(url_imagenes[i])
    output = open(titulos_imagenes[i] + '(' + fecha_actual + ')' + '.jpg','wb')
    output.write(resource.read())
    output.close()    


