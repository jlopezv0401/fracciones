#Guadar diccionario en MySQL
# -*- coding: utf-8 -*-
import MySQLdb
import codecs
import os
import re
from BeautifulSoup import BeautifulSoup

texto = open('tigie.sql', 'w')
texto.writelines("CREATE DATABASE IF NOT EXISTS tarifa DEFAULT CHARACTER SET utf8; ")
texto.writelines("USE tarifa; ")
texto.writelines("DROP TABLE IF EXISTS tarifa; ")
texto.writelines("CREATE TABLE tarifa(seccion VARCHAR(6), seccion_desc TEXT, capitulo int(2), "+
                 "capitulo_desc TEXT,partida INT(4),partida_desc TEXT,partida_a INT(4),partida_a_desc TEXT," +
                 "subpartida INT(6),subpartida_desc TEXT,fraccion INT(8),fraccion_desc TEXT,unidad_medida VARCHAR(16),"+
                 "arancel_importacion_rt VARCHAR(10),iva_importacion_rt VARCHAR(10),arancel_importacionn_ff VARCHAR(10)," +
                 "iva_importacion_ff VARCHAR(10),arancel_importacion_rf VARCHAR(10),iva_importacion_rf VARCHAR(10)," +
                 "arancel_exportacion_rt VARCHAR(10),iva_exportacion_rt VARCHAR(10),arancel_exportacion_ff VARCHAR(10)," +
                 "iva_exportacion_ff VARCHAR(10),arancel_exportacion_rf VARCHAR(10),iva_exportacion_rf VARCHAR(10)," +
                 "restricciones_importacion TEXT,restricciones_exportacion TEXT," +
                 "anexos TEXT,cupos_importar_de TEXT,cupos_exportar_a TEXT,observaciones_generales TEXT," +
                 "observaciones_importacion TEXT,observaciones_exportacion TEXT,"+
                 "tlc_eua VARCHAR(20),tlc_canada VARCHAR(20),tlc_colombia VARCHAR(20),tlc_japon VARCHAR(20),"+
                 "tlc_bolivia VARCHAR(20),tlc_costa_rica VARCHAR(20),tlc_nicaragua VARCHAR(20),tlc_israel VARCHAR(20)," +
                 "tlc_comunidad_europea VARCHAR(20),tlc_guatemala VARCHAR(20),tlc_el_salvador VARCHAR(20)," +
                 "tlc_honduras VARCHAR(20),tlc_suiza VARCHAR(20),tlc_noruega VARCHAR(20),tlc_islandia VARCHAR(20)," +
                 "tlc_liechtenstein VARCHAR(20),tlc_chile VARCHAR(20),tlc_uruguay VARCHAR(20), PRIMARY KEY(fraccion))" +
                 "ENGINE=InnoDB DEFAULT CHARSET=utf8;\n")
texto.writelines("INSERT INTO tarifa VALUES \n")

base = MySQLdb.connect("192.168.40.240", "root", "moises", "fracciones")
cursor = base.cursor()
consulta = "SELECT fraccion,txt FROM fracciones where fraccion=\'03038101\'"
cursor.execute(consulta)
documentos = cursor.fetchall()

for documento in documentos:
    if len(documento[1]) > 0:
        soup =  BeautifulSoup('' .join(documento[1]))
        soup.prettify()
        #soup.__unicode__()
        #tabla = soup.find(name="table", attrs={"border" :"1"})
        noTablas = len(soup.findAll(name="table"))
        #print noTablas
        tabla = soup.find(name="table")
        
##########################################################################################################################################
#       TABLA FRACCION
##########################################################################################################################################
        tabla1 = tabla.find(name="table")
        if not tabla1:
            print documento[0] + ' Sin tabla1'
            for p in range (1,13):
                linea = linea + "\'NULL\'," 
        else:            
            filas = tabla1.findAll('tr')
            nofilas = len(filas)
            x=1
            linea="("
            for fila in filas:
                #nombre = fila.findAll(name="font", attrs={"color" : "#ff8100"}, text=True)
                celdas = fila.findAll(name="td")
                y=1
                for celda in celdas:
                    nombre = celda.findAll(name="font", attrs={"color" : "#ff8100"}, text=True)
                    if y==2:
                        if not nombre:
                            col2='NULL'
                        else:
                            col2=nombre[0]
                    elif y==3:
                        if not nombre:
                            col3='NULL'
                        else:
                            col3=nombre[0]
                    y+=1
                if x==5:
                    if nofilas==5:
                        linea = linea + "\'NULL\',\'NULL\',\'" + col2.encode('utf-8') + "\',\'" + col3.encode('utf-8') + "\',"
                else:    
                    linea = linea + "\'" + col2.encode('utf-8') + "\',\'" + col3.encode('utf-8') + "\',"
                    
                x+=1
        
##########################################################################################################################################
#       TABLA ARANCELES
##########################################################################################################################################
        tabla2 = tabla1.findNext(name="table")
        if not tabla2:
            print documento[0] + ' Sin tabla2'
            for p in range (1,14):
                linea = linea + "\'NULL\',"  
        else:
            filas = []
            filas = tabla2.findAll(name="tr")
            x=1
            for fila in filas:
                if x==3:
                    celdas=fila.findAll(name="td")
                    textos=celdas[0].findAll(name="font", text=True)
                    linea = linea + "\'" + textos[1].encode('utf-8') + "\',"
                if x==4:
                    celdas=fila.findAll(name="td")
                    y=1
                    for celda in celdas:
                        textos=celda.findAll(name="font", text=True)
                        if y>1 and y<8:
                            if not textos:
                                linea = linea + "\'NULL\',"
                            else:
                                linea = linea + "\'" + textos[0].encode('utf-8') + "\',"
                        y+=1
                if x==5:
                    celdas=fila.findAll(name="td")
                    y=1
                    for celda in celdas:
                        textos=celda.findAll(name="font", text=True)
                        if y>1 and y<8:
                            if not textos:
                                linea = linea + "\'NULL\',"
                            else:
                                linea = linea + "\'" + textos[0].encode('utf-8') + "\',"
                        y+=1
                x+=1
        
        uno = tabla.find(name="font", text="RESTRICCIONES:")
        dos = uno.findNext(["b","u","a","p","ui","font","table"])
        
##########################################################################################################################################
#       RESTRICCIONES A LA IMPORTACION
##########################################################################################################################################
        r_importa = ""
        a = "A la  Importación:"
        if dos.contents:
            if a in str(dos.contents[0]):
                while(1):
                    #uno= uno.findNext(["b","u","a","p","ui","font","table"])
                    uno= uno.findNext("font")
                    if not uno:
                        break
                    else:
                        if  uno.contents:
                            a = "A la Exportación:"
                            if a in str(uno.contents[0]):
                                break
                            else:
                                r_importa += " " + uno.contents[0]
                                #print uno.contents[0]
        
##########################################################################################################################################
#       RESTRICCIONES A LA EXPORTACION
##########################################################################################################################################
        r_exporta = ""
        a = "A la Exportación:"
        #print a
        if a in str(uno.contents[0]):
            while(1):
                #uno= uno.findNext(["b","u","a","p","ui","font","table"])
                uno= uno.findNext("font")
                if not uno:
                    break
                else:        
                    if  uno.contents:
                        a = "ANEXOS:"
                        if a in str(uno.contents[0]):
                            break
                        else:
                            #print uno.contents[0]
                            r_exporta += " " +  no.contents[0]
        
##########################################################################################################################################
#       ANEXOS
##########################################################################################################################################        
        anexos = ""
        a = "ANEXOS:"
        #print a
        if a in str(uno.contents[0]):
            while(1):
                #uno= uno.findNext(["b","u","a","p","ui","font","table"])
                uno= uno.findNext("font")
                if not uno:
                    break
                else:        
                    if  uno.contents:
                        a = "CUPOS:"
                        if a in str(uno.contents[0]):
                            break
                        else:
                            #print uno.contents[0]
                            anexos += " " +  no.contents[0]
                            
        uno = tabla.find(name="font", text="CUPOS:")
        #print uno
        dos = uno.findNext(["b","u","a","p","ui","font","table"])
        
###########################################################################################################################################
##       CUPOS PARA IMPORTAR DE
###########################################################################################################################################
        cupos_importa = ""
        a = "Para Importar de:"
        if dos.contents:
            if a in str(dos.contents[0]):
                while(1):
                    #uno= uno.findNext(["b","u","a","p","ui","font","table"])
                    uno= uno.findNext("font")
                    if not uno:
                        break
                    else:
                        if  uno.contents:
                            a = "Para Exportar a:"
                            if a in str(uno.contents[0]):
                                break
                            else:
                                #print uno.contents[0]
                                cupos_importa += " " +  uno.contents[0]
                                
###########################################################################################################################################
##       CUPOS PARA EXPORTAR DE
###########################################################################################################################################
        cupos_exporta = ""
        a = "Para Esportar de:"
        if dos.contents:
            if a in str(dos.contents[0]):
                while(1):
                    #uno= uno.findNext(["b","u","a","p","ui","font","table"])
                    uno= uno.findNext("font")
                    if not uno:
                        break
                    else:
                        if  uno.contents:
                            a = "OBSERVACIONES:"
                            if a in str(uno.contents[0]):
                                break
                            else:
                                print uno.contents[0]
                                cupos_exporta +=  " " + uno.contents[0]
                                
        uno = tabla.find(name="font", text="OBSERVACIONES:")
        #print uno
        dos = uno.findNext(["b","u","a","p","ui","font","table"])
###########################################################################################################################################
##       OBSERVACIONES GENERALES
###########################################################################################################################################
        observa_grales = ""
        a = "Generales:"
        if dos.contents:
            if a in str(dos.contents[0]):
                while(1):
                    #uno= uno.findNext(["b","u","a","p","ui","font","table"])
                    uno= uno.findNext("font")
                    if not uno:
                        break
                    else:
                        if  uno.contents:
                            a = "En Importación:"
                            if a in str(uno.contents[0]):
                                break
                            else:
                                #print uno.contents[0]
                                observa_grales +=  " " +  uno.contents[0]
                            
##########################################################################################################################################
#       OBSERVACIONES EN IMPORTACION
##########################################################################################################################################                              
        observa_importa = ""
        a = "En Importación:"
        #print a
        if a in str(uno.contents[0]):
            while(1):
                uno= uno.findNext("font")
                if not uno:
                    break
                else:        
                    if  uno.contents:
                        a = "En Exportación:"
                        if a in str(uno.contents[0]):
                            break
                        else:
                            #print uno.contents[0]
                            observa_importa +=  " " +  uno.contents[0]
                            
##########################################################################################################################################
#       OBSERVACIONES EN EXPORTACION
##########################################################################################################################################
        observa_exporta = ""
        a = "En Exportación:"
        #print a
        if a in str(uno.contents[0]):
            while(1):
                uno= uno.findNext("font")
                if not uno:
                    break
                else:        
                    if  uno.contents:
                        a = "Tratados de Libre Comercio"
                        if a in str(uno.contents[0]):
                            break
                        else:
                            #print uno.contents[0]
                            observa_exporta +=  " " + uno.contents[0]
                        
        linea = linea + "\'" + r_importa.encode('utf-8') + "\',\'" +  r_exporta.encode('utf-8')
        linea = linea + "\',\'"+ anexos.encode('utf-8') + "\',\'" + cupos_importa.encode('utf-8') 
        linea = linea + "\',\'" + cupos_exporta.encode('utf-8') + "\',\'" + observa_grales.encode('utf-8')
        linea = linea + "\',\'" + observa_importa.encode('utf-8') + "\'," + observa_exporta.encode('utf-8') + "\',"
        
##########################################################################################################################################
#       TABLA TRATADOS DE LIBRE COMERCIO
##########################################################################################################################################
        tabla3 = tabla2.findNext(name="table")
        while(1):
            uno= tabla3.findNext("font")
            if not uno:
                break
            else:        
                if  uno.contents:
                    a = "Tratados de Libre Comercio"
                    if a in str(uno.contents[0]):
                        break
                    else:
                        tabla3 = tabla3.findNext(name="table")

        filas = []       
        if not tabla3:
            print documento[0] + ' Sin tabla3'
            for p in range (1,19):
                linea = linea + "\'NULL\',"
            linea = linea + "\'NULL\'"
        else:
            filas = tabla3.findAll(name="tr")
            x=1
            for fila in filas:
                if x==3:
                    celdas=fila.findAll(name="td")
                    for celda in celdas:
                        textos=celda.findAll(name="font", text=True)
                        if not textos:
                            linea = linea + "\'NULL\',"
                        else:
                            linea = linea + "\'" + textos[0].encode('utf-8') + "\',"
                elif x==5:
                    celdas=fila.findAll(name="td")
                    for celda in celdas:
                        textos=celda.findAll(name="font", text=True)
                        if not textos:
                            linea = linea + "\'NULL\',"
                        else:
                            linea = linea + "\'" + textos[0].encode('utf-8') + "\',"
                elif x==7:
                    celdas=fila.findAll(name="td")
                    y=1
                    for celda in celdas:
                        textos=celda.findAll(name="font", text=True)
                        if not textos:
                            linea = linea + "\'NULL\',"
                            if y==6:
                                linea = linea + "\'NULL\'"   
                        else:
                            linea = linea + "\'" + textos[0].encode('utf-8') + "\',"
                            if y==6:
                                linea = linea + "\'" + textos[0].encode('utf-8') + "\'"                           
                        y+=1    
                x+=1

        linea = linea + "),\n"
        #print linea
        texto.writelines(linea)
    else:
        print documento[0]
texto.close()

