#!/usr/bin/env python
# coding: utf-8

# # Algoritmo FP-Growth

# Importar el dataset limpio

# In[1]:


from data import *


# In[2]:


from anytree import AnyNode, Node, RenderTree , AsciiStyle, Walker


# In[1]:


#Soporte de las reglas
support = 0.02
confiance = 30


# Construir el FP-Tree

# In[6]:


#Encontrar la frecuencia de cada articulo
frecuencia = {}

#Recorrer cada factura del dataset
for invoice in dataset.values():
    #Recorrer cada articulo de la factura
    for item in invoice:
        #Agregar el articulo a la tabla frecuencia si no existe
        #Si ya existe, incrementar el contador de la frecuencia
        frecuencia[item] = frecuencia.get(item, 0) + 1

print(frecuencia)


# In[7]:


#Ordenar la tabla de frecuencia de mayor a menor
sortFrequency = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)


# In[8]:


print(sortFrequency)


# In[10]:


#Asignar prioridad de acuerdo a la frecuencia
priority = {k[0]:v for v,k in enumerate(sortFrequency)}


# In[11]:


print(priority)


# In[13]:


#Dataset ordenado de acuerdo a la prioridad de los articulos

sortDataset = {}

for key in dataset:
    second = dataset[key]
    second.sort(key=priority.get)
    sortDataset[key] = second
    
print(sortDataset)


# In[14]:


#Crear el nodo raiz
root = Node(name = "root",cont = 1)


# In[16]:


# cont = 0
for invoice in sortDataset.values():
#     cont +=1
    prev = root
    for item in invoice:
        sub = next((c for c in prev.children if c.name == item),None)
        if sub is None:
            prev = Node(name = item, parent = prev,cont = 1)
        else:
            prev = sub
            prev.cont +=1
#     if(cont== 20):
#         break


# In[17]:


print(RenderTree(root))


# Graficar el arbol

# In[18]:


import anytree
from graphviz import render
from anytree import Node, RenderTree
from anytree.exporter import DotExporter


# In[59]:


another = root.children[0].children[0].children[3]


# In[60]:


DotExporter(another).to_picture("graph4.png")


# In[52]:


for line in DotExporter(root.children[0].children[0]):
    print(line)


# Generar reglas de asociacion

# In[ ]:


#Reglas generadas con Soporte dinamico
from anytree import findall
for minSup in range(support,101):
    rules = findall(root, filter_=lambda node: node.cont in ( 100,minSup))
    if len(rules) != 0:
        print(rules)

