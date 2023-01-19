# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 17:34:47 2022

@author: tpiccoli

Categorização da NPS do espectro sonoro de operação de prensagem a frio conforme NR 15;
Avaliação fina  @ 44 kHz
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('NPS_ChapaGrossa_1.txt', sep=' ',header=None)

espectro_nps=df[0].values.tolist()
espec_nps_a=[]
'''
Medição simplificada
min(espectro_nps),max(espectro_nps)
Out[37]: (75.0, 94.8)
Diferença 19.799999999999997
'''
dif0=19.799999999999997
dif1=max(espectro_nps)-min(espectro_nps)

for i in espectro_nps:
    nps_a = i/dif1*dif0+75
    espec_nps_a.append(nps_a)
    

nps_impacto=[]
nps_ambiente=[]


dv_pad=np.std(espec_nps_a)
media=np.median(espec_nps_a)
print('Desvio padrão do espectro de:', dv_pad)
print('Mèdia da amostra do espectro de:' , media)

#separação, ruidos e ambiente
for nps in espec_nps_a:
    if nps > media+dv_pad:
        #é impacto
        nps_impacto.append(nps)
    else:
        nps_ambiente.append(nps)
    
print('----')        
print('tempo em ruído de impacto: (s) ', len(nps_impacto)/44100)
print('Ruído médio e desvio (dB): ', np.median(nps_impacto),' |' , np.std(nps_impacto))
print('-----')
print('tempo em ruído ambiente: (s) ', len(nps_ambiente)/44100)
print('Ruído médio e desvio (dB): ', np.median(nps_ambiente),' |' , np.std(nps_ambiente))


peso_nps=np.repeat(1/44100,len(espec_nps_a))
#Histograma geral de ruídos da gravação
plt.hist(espec_nps_a,bins=21,weights=peso_nps)
plt.xlabel('Faixas de Nível de Pressão Sonora (dB)')
plt.ylabel('Duração (s)')
plt.title('Histograma de Ruídos')
plt.xlim(70,100) #dim. x do gráfico
plt.ylim(0,20) #Dim. y. do gráfico
plt.grid(True)
plt.show()

#histograma para ruído > mediana+margem
peso_nps2=np.repeat(1/44100, len(nps_impacto))

plt.hist(nps_impacto,bins=21,weights=peso_nps2,color='r')
plt.xlabel('Faixas de Nível de Pressão Sonora (dB)')
plt.ylabel('Duração (s)')
plt.title('Histograma de Ruído de Impacto')
plt.xlim(82, 90) #dim. x do gráfico
plt.ylim(0,1.2) #Dim. y. do gráfico
plt.grid(True)
plt.show()

plt.plot(espec_nps_a,color='g') #gráfico de ruído geral captado

plt.ylabel('Nível de Pressão Sonora (dB(A))')
plt.xlabel('Duração (44100s ^(-1))')
plt.title('Gráfico de Amplitude Sonora - NPS x Tempo ')
plt.show()
