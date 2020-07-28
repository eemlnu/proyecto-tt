#!/usr/bin/env python
# coding: utf-8

# # Preprocesamiento de Facturas

# Instalar la libreria xmljson

# In[33]:


import json,xmljson
from xml.dom import minidom
import xml.etree.ElementTree as ET
import os


# In[34]:


from lxml.etree import fromstring, tostring


# In[35]:


#Recorrer todos los comprobantes de esta carpeta
folder= 'resources'

#Los combrobantes tienen que estar en formato XML
invoicesList = {}

for fileName in os.listdir(folder):
    
    #Ruta relativa de cada comprobante
    content = open(os.path.join(folder, fileName), 'r')
    
    #Recorrer cada linea del contenido de un comprobante
    for x in content:
        
        idAutorizacion='0'
        
        #Extraer el numero de autorizacion
        #(identificador de la factura, para luego eliminar los duplicados)
        if(x.find('<numeroAutorizacion>')==0):
            
            #Crear arbol de elementos de la linea
            autorization = ET.fromstring(x)
            print('\"',autorization.text,end='')
            
            idAutorizacion = str(autorization.text)
            
        #Extraer los datos de la transaccion
        if(x.find('<detalles')!=-1):
            
            #Delimitar el texto requerido
            invoiceText=invoiceText = x
            if(x.find('<infoAdic')!=-1):   
                invoiceText = x[x.find('<detalles'):x.find('<infoAdic')]
            elif(x.find('<ds:Signature')!=-1):
                invoiceText = x[x.find('<detalles'):x.find('<ds:Signature')]
            
            #Crear arbol de elementos del contenido de la factura
            invoice = ET.fromstring(invoiceText)
            
            #Lista para agregar los articulos de la misma factura
            itemList = []
            
            #Se recorre todas las coincidencias de articulos 'detalle'
            for detail in invoice.findall('detalle'):
                #description = detail.find('descripcion').text
                _id = detail.find('codigoPrincipal').text
                num = detail.find('cantidad').text
                
                #Se agrega el articulo a la lista
                itemList.append(_id+'-'+str(num).replace(".", ""))
                
                #print (_id,num)
            
            #Se agrega la factura a la lista de facturas
            #Si la factura ya existe, la reemplaza o sobreescribe
            invoicesList[str(idAutorizacion)] = itemList
            
            #Se muestra la factura con sus respectivos articulos
            print('\":',invoicesList[str(idAutorizacion)],',')
            #Cierra la lectura del archivo
            #(no se necesita el resto de datos)
            content.close()
            
            #Pasa al siguiente archivo
            break

print(invoicesList)

