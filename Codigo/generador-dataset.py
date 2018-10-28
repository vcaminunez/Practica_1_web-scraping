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


#función que guarda los datos en el dataset

def generar_dataset():
    
    cabecera = ['Continente', 'Nombre', 'Tendencia', 'Puntos', 'Variacion(%)', 'Variacion puntos', 'Puntos Anterior', 'Hora', 'Fecha', 'Fecha descarga'] 
    fecha_actual = str(datetime.datetime.now())
    fecha_actual = fecha_actual[8:10] + '-' + fecha_actual[5:7] + '-' + fecha_actual[0:4]
    
    csv_file = open('datos_indices(' + fecha_actual + ').csv','wb')    
    csv_writer = csv.writer(csv_file,delimiter =';')
    
    csv_writer.writerow(cabecera)
    
    for i in range(0,len(datos_final)):
         csv_writer.writerow(datos_final[i])
    csv_file.close()


#funcion que acabade realizar el formato antes de proceder a creaer el dataset

def formato_final(datos_fin):
        
    for i in range(0,len(datos_fin)):
        fecha_inicial = datos_fin[i][8]
        del(datos_fin[i][8])
                
        if ':' in datos_fin[i][7]:
            datos_fin[i].append(fecha_inicial[0:10])
        else:
            if datos_fin[i][7][1] == '/':
                fecha_temporal = '0' + datos_fin[i][7][0] + '-' + datos_fin[i][7][2:4] + '-' + '2018'
            else:                
                fecha_temporal = datos_fin[i][7][0:2] + '-' + datos_fin[i][7][3:5] + '-' + '2018'
                
            del(datos_fin[i][7])
            datos_fin[i].append(' ')
            datos_fin[i].append(fecha_temporal)
        datos_fin[i].append(fecha_inicial)
    return datos_fin


#función que hace el web scraping y formatea los datos

def scraping(datos_formatados):
    datos_formatados = []
    temporal = []
    temporal2 = []
    temporal3 = []        
     
    for caja in soup.find_all('div', class_='tabla'):
        continente = caja.find('table', class_='tablalista tabla-latam').thead.tr.td.text
        continente = continente.encode(encoding='UTF-8',errors='strict')
        for cuerpo in caja.find_all('tbody'):
            temporal = []
            for datos in cuerpo.find_all('tr'):   
                datos0 = datos.text
                datos0 = datos0.encode(encoding='UTF-8',errors='strict')       
                temporal.append(datos0.split('\n'))  
                temporal2 = []
                for i in range(0,len(temporal)):
                    if i % 2 == 0:
                        pass
                    else:
                        temporal2.append(temporal[i])   
                for i in range(0,len(temporal2)):
                    temporal2[i][0] = continente
        for i in range(0,len(temporal2)):
            temporal3.append(temporal2[i])
    
    for i in range(0,len(temporal3)):
        temporal3[i][3] = temporal3[i][3].replace('.','')
        temporal3[i][5] = temporal3[i][5].replace('.','')
        temporal3[i][6] = temporal3[i][6].replace('.','')
        
        temporal3[i][3] = temporal3[i][3].replace(',','.')
        temporal3[i][4] = temporal3[i][4].replace(',','.')
        temporal3[i][5] = temporal3[i][5].replace(',','.')
        temporal3[i][6] = temporal3[i][6].replace(',','.')
        
        del(temporal3[i][8])
        
    for i in range(0,len(temporal3)):
        if float(temporal3[i][5]) < 0:
            temporal3[i][2] = 'Baja'
        else:         
            temporal3[i][2] = 'Sube'         
              
    for i in range(0,len(temporal3)):
        temporal3[i][4] = temporal3[i][4].replace('%','')
        
    fecha_hora_inglesa = str(datetime.datetime.now())
    fecha_hora = fecha_hora_inglesa[8:10] + '-' + fecha_hora_inglesa[5:7] + '-' + fecha_hora_inglesa[0:4] + fecha_hora_inglesa[10:]        
                  
    for i in range(0,len(temporal3)):
        datos_formatados.append(temporal3[i])
        datos_formatados[i].append(fecha_hora)
            
    return datos_formatados
           

#estas son las dos variables que se pueden modificar

tanda = 11   # numero de veces que se capturarán datos
delay = 3600  # segundos entre cada toma de datos. 


#inicializamos la lista donde se guardarán los datos finales
datos_final = []   
datos_formatados = []
datos_acumulados = []


for contador in range(0,tanda):
    
    url = 'https://www.eleconomista.es/indices-mundiales/'
    response = urllib2.urlopen(url)
    soup0 = response.read()
    soup = BeautifulSoup(soup0, 'lxml')
    
    datos_formatados = scraping(datos_formatados)
    
    for i in range(0,len(datos_formatados)):
        datos_acumulados.append(datos_formatados[i])   
    
    if (tanda -1 ) != contador:
        time.sleep(delay)

    
datos_final = formato_final(datos_acumulados)       
generar_dataset()    
   

   














