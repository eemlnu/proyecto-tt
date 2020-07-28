#!/usr/bin/env python
# coding: utf-8

# # Algoritmo Apriori

# In[171]:


#Importar itemset
from data import *
import itertools


# In[173]:


print(dataset)


# In[174]:


#Parametros iniciales
min_supp_percent = 0.02
min_support = int(min_supp_percent*len(dataset))
min_confidence = 30
lift = 1
print(min_support)


# Conjunto de candidatos C1

# In[175]:


#Construir la tabla de soporte

#Encontrar la frecuencia de cada articulo
frecuencia = {}

#Recorrer cada factura del dataset
for invoice in dataset.values():
    #Recorrer cada articulo de la factura
    for item in invoice:
        #Agregar el articulo a la tabla frecuencia si no existe
        #Si ya existe, incrementar el contador de la frecuencia
        frecuencia[item] = frecuencia.get(item, 0) + 1
sortFrequency = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)
print(sortFrequency)


# Remover los conjuntos de articulos que esten por debajo del soporte minimo.

# In[176]:


itemsetL1 = []
for candidate in sortFrequency:
    if(candidate[1]>=min_support):
        itemsetL1.append(candidate)
#print(itemsetL1)  


# Generar candidatos C2 usando el itemsetL1, luego verificar si todos los subconjuntos son frecuentes y finalmente buscar el soporte en el dataset

# In[177]:


candidatesC2 = []

#Generar candidatos C2 usando el itemsetL1
for candidates in itertools.combinations(itemsetL1, r=2):
    _itemCan = [x[0] for x in candidates]
    #print(_itemCan)
    _itemL1 = [x[0] for x in itemsetL1]
    
    match = all(item in _itemL1 for item in _itemCan)
    if not match:
        break
        #Verificar si cada subconjunto se encuentra en itemsetL1
        #if candidate not in _itemL1:
            #Si no existe algun subconjunto, entonces hay que descartarlo y pasar
            #break
    else:
        itemCan = [x[0] for x in candidates]
        #print(itemCan)
        #Buscar el soporte de los articulos en el dataset
        supp = 0
        for invoice in dataset.values():
            check = all(item in invoice for item in itemCan)
            if(check):
                supp+=1
        candidatesC2.append((itemCan,supp))
        continue
        
print(candidatesC2)


# In[178]:


#print(candidatesC2)


# Conservar los conjuntos que cumplan con el soporte minimo

# In[179]:


itemsetL2 = []
for candidate in candidatesC2:
    #print(candidate[1])
    if(candidate[1]>=min_support):
        itemsetL2.append(candidate)
print(itemsetL2)


# Paso 3

# In[180]:


onlyItems2 = [x[0] for x in itemsetL2]
candidatesC3 = []
for x in onlyItems2:
    for y in onlyItems2:
        if(x[-1] == y[0]):
            #print('yeah')
            match = x[:-1]+y[0:]
            
            #Buscar el soporte de los articulos en el dataset
            supp = 0
            for invoice in dataset.values():
                check = all(item in invoice for item in match)
                if(check):
                    supp+=1
            candidatesC3.append((match,supp))


# In[181]:


print(candidatesC3)


# Conservar los conjuntos que cumplan con el soporte minimo

# In[182]:


itemsetL3 = []
for candidate in candidatesC3:
    #print(candidate[1])
    if(candidate[1]>=min_support):
        itemsetL3.append(candidate)
print(itemsetL3)


# C4

# In[183]:


onlyItems = [x[0] for x in itemsetL3]
candidatesC4 = []
for x in onlyItems:
    for y in onlyItems:
        if(x[-1] == y[0]):
            #print('yeah')
            match = x[:-1]+y[0:]
            
            #Buscar el soporte de los articulos en el dataset
            supp = 0
            for invoice in dataset.values():
                #print('entro')
                check = all(item in invoice for item in match)
                if(check):
                    supp+=1
            candidatesC4.append((match,supp))
#print(candidatesC4)


# # Generar reglas de asociacion

# In[184]:



onlyItems3 = [x[0] for x in itemsetL3]
#print(onlyItems3)


# In[185]:


elements = []
for items in onlyItems3:
    
    for ind,item in enumerate(items):
        value = items.copy()
        value.pop(ind)
        elements.append((item,value))
        elements.append((value,item))
#print('My list:', *elements, sep='\n- ')


# In[186]:


elements2 = []
for items in onlyItems2:
    
    for ind,item in enumerate(items):
        value = items.copy()
        value.pop(ind)
        elements2.append((item,value))
        elements2.append((value,item))
#print('My list:', *elements2, sep='\n> ')


# In[187]:


allItemSets = itemsetL1+itemsetL2+itemsetL3


# In[188]:


#print(allItemSets)


# In[189]:


reglasGeneradas = []
for key, value in elements+elements2:
    print('Regla: ',key,' -> ', value)
    
    _all = []
    if(type(key) == str):
        _all.append(key)
        #print('jj')
    else:
        _all+=key
    if(type(value) == str):
        _all.append(value)
        #print('kk')
    else:
        _all+=value
    
    print(_all)
    num = 0
    den = 1
    
    for _item,supp in allItemSets:
        check = all(item in _item for item in _all)
        if check:
            print(_item,supp,' ------')
            num = supp
        if key == _item:
            print(_item,supp,' ------')
            den = supp
            #print('ok',key,' = ',supp)
    confianza = (num/den)*100
    #print(num,'/',den,'* 100')
    #print(confianza,'%')
    #print('------')
    if(confianza<=100):
        reglasGeneradas.append((key,value,confianza))
    
        #print(item,' -> ',supp)


# In[190]:


reglasOrdenadas = sorted(reglasGeneradas, key=lambda x: x[2], reverse=True)
print('Reglas generadas:', *reglasOrdenadas, sep='\n> ')


# In[191]:


print(len(reglasOrdenadas))


# In[194]:


#reglasAltaConfianza = []
print('Reglas de asociacion que cumplen con la frecuencia minima:\n')
for x,y,z in reglasOrdenadas:
    if(z>=min_confidence):
        reglasAltaConfianza.append((x,y,z))
        print(x,' -> ',y, ', confianza = ',z,'%')


# In[195]:


print(len(reglasAltaConfianza))

