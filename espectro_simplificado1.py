# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 09:29:20 2022

@author: tpiccoli

Categorização da NPS do espectro sonoro de operação de prensagem a frio conforme NR 15;
Avaliação simplificada @ 44 kHz
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from scipy.stats import norm


df=pd.read_csv('Medicao_1.csv', sep=',',header=None)


espectro_nps=df[0].values.tolist()
peso_nps=np.repeat(0.2, len(espectro_nps)) #converte distribuição de 0,2s para 1s

dv_pad=np.std(espectro_nps)
media=np.median(espectro_nps)
print('Desvio padrão do espectro de:', dv_pad)
print('Mèdia da amostra do espectro de:' , media)
nps_impacto=[]
nps_ambiente=[]

#separação, ruidos e ambiente
for nps in espectro_nps:
    if nps > media+dv_pad:
        #é impacto
        nps_impacto.append(nps)
    else:
        nps_ambiente.append(nps)
  
peso_nps2=np.repeat(0.2, len(nps_impacto))
      
print('----')        
print('tempo em ruído de impacto: (s) ', len(nps_impacto)*0.2)
print('Ruído médio e desvio (dB): ', np.median(nps_impacto),' |' , np.std(nps_impacto))
print('-----')
print('tempo em ruído ambiente: (s) ', len(nps_ambiente)*0.2)
print('Ruído médio e desvio (dB): ', np.median(nps_ambiente),' |' , np.std(nps_ambiente))

#Histograma geral de ruídos da gravação
plt.hist(espectro_nps,bins=21,weights=peso_nps)
plt.xlabel('Faixas de Nível de Pressão Sonora (dB)')
plt.ylabel('Duração (s)')
plt.title('Histograma de Ruídos')
plt.xlim(min(espectro_nps), max(espectro_nps)) #dim. x do gráfico
plt.ylim(0,6) #Dim. y. do gráfico
plt.grid(True)
plt.show()

#histograma para ruído > mediana+margem

plt.hist(nps_impacto,bins=21,weights=peso_nps2,color='r')
plt.xlabel('Faixas de Nível de Pressão Sonora (dB)')
plt.ylabel('Duração (s)')
plt.title('Histograma de Ruído de Impacto')
plt.xlim(min(nps_impacto), max(nps_impacto)) #dim. x do gráfico
plt.ylim(0,3) #Dim. y. do gráfico
plt.grid(True)
plt.show()

plt.plot(espectro_nps,color='g') #gráfico de ruído geral captado

plt.ylabel('Nível de Pressão Sonora (dB(A))')
plt.xlabel('Duração (0,2s)')
plt.title('Gráfico de Amplitude Sonora - NPS x Tempo ')
plt.show()
