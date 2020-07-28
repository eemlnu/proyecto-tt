#!/usr/bin/env python
# coding: utf-8

# # Algoritmo ECLAT

# In[1]:


#Importar itemset
from data import *
import itertools
from collections import defaultdict


# In[18]:


#Parametros iniciales
support = 0.02
min_sup = int(support*len(dataset))
confidence = 30
lift = 1


# Clases

# In[3]:


#Crear el diccionario vacio
resultClass = defaultdict(list)


# In[8]:


#Construir la tabla de clases

#Recorrer cada factura del dataset
for autorization in dataset:
    invoice = dataset[autorization]
    #Recorrer cada articulo de la factura
    for item in invoice:
        
        resultClass[item].append(autorization)


# In[17]:


for k,v in resultClass.items():
    print(k, 'soporte = ',len(v))


# In[55]:


#num = numero de articulos agrupados
#items = lista de articulos 
def recursivity(num,data):
    result = []
    count = 0
    for pair in itertools.permutations(data, r=2):
        result.append(pair)
        count+=1
        if(count == 110):
            break
    return(result)


# In[56]:


rul = recursivity(2,resultClass)


# In[57]:


rulGen = []
for ant,con in rul:
    for key,value in resultClass.items():
        if (ant == key):
            rulGen.append((ant,con,len(value)/len(dataset)))


# # Generacion de reglas de asociacion

# In[59]:


for item in rulGen:
    print(item[0],' ->', item[1],'con confianza = ',item[2])

