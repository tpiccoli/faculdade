# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:43:57 2022

@author: Tiago Piccoli

Algoritmo para auxílio no cálculo de SETPOINT de temperaturas entre tanques - trocador de calor c/ reservatório intermediário

"""
'''
Modelo 1 - Tanque atua como reservatório intermediário, enviando água para arrefecer algum processo e também recebe água fria de um chiller.
O reserv. intermediário tem a função de reduzir o delta_T no chiller (não há ligação direta: e.g. chiller//processo) e atuar como um 'bolsão térmico'.

Fluxo 1: Chiller > Reservatório > Chiller
Fluxo 2: Processo > Reservatório > Processo

Melhorias futuras: Calcular perda/ganho de temperatura do reservatório e tuublação;

'''

#import numpy as np

cp_agua=4178 # J/Kg*K

m_chiller=(int(input('Por favor, digite o fluxo de água fria: (L/h) ')))/3600 #vem do chiller - kg/s
m_tank=int(input('Por favor, digite a capacidade do reservatório: (L) '))
m_processo=(int(input('Por favor, digite o fluxo de água quente: (L/h) ')))/3600

t_chiller=float(input('Por favor, digite a temperatura de retorno (setpoint) do fluxo de água fria: (°C) '))
t_processo=float(input('Por favor, digite a temperatura de retorno do fluxo de água quente: (°C) '))

t_tanque=[]
t_0 = float(input('Digite a temperatura do reservatório no momento inicial: (°C)'))
t_tanque.append(t_0)
#------------------------------------------------
def ciclo(): #ciclo de 1h (3600s)
    global e_ent
    global e_sai
    i=0
    t_tanque.clear()
    t_tanque.append(t_0)
    
    while i<3600:
        e_ent = m_processo * cp_agua * abs(t_tanque[i]-t_processo)
        e_sai = m_chiller * cp_agua * abs(t_tanque[i]-t_chiller)
        
        saldo_termico = e_ent-e_sai

        #variação temp. tanque
        t_tank = saldo_termico/(cp_agua*m_tank)
        t_tank = t_tanque[i] + t_tank
        t_tanque.append(t_tank)
        i=i+1
        

#----------------------------------------------
a0=int(input('Deseja apenas rodar uma simulação para 1 hora? Digite 1'))

if a0==1:
    ciclo()
    print(t_tanque[3600])
else:
    pass    
#----------------------------------------------
a1=int(input('Deseja estimar a capacidade ótima do sistema? Digite 1'))
if a1==1:
    ciclo()
    a00= int(input('Iterar variando: Vazão (1), Temperatura(2) ou ambos (3)?'))
    i0=0 #contador de iterações
    imax=int(input("Digite o número máximo de iterações:"))
    
    if a00==1: #iteração de vazão
        while i0<imax:
            ciclo()
            if t_tanque[3600]>t_0: #caso subdimensionado - i.e., a água do reservatório vai aquecendo
                m_chiller = m_chiller + 0.001 #aumentar o fluxo em 10 L/h 
                i0=i0+1

            elif t_tanque[3600]<t_0: #caso superdimensionado i.e., a água do reservatório vai resfriando
                m_chiller = m_chiller - 10/3600 #diminuir o fluxo em 10 L/h
                i0=i0+1

            else:
                print('Vazão necessária de água gelada (L):',m_chiller*3600)
                print('Iterações:',i0)
                break
        print('Vazão necessária de água gelada (L):',m_chiller*3600)
        print('Iterações:',i0)
         
    if a00==2: #iteração de temperatura
        while i0<imax:
            ciclo()
            if t_tanque[3600]>t_0:
                t_chiller = t_chiller - 0.05 #diminui a temperatura em 0.05°C
                i0=i0+1

            elif t_tanque[3600]<t_0:
                t_chiller = t_chiller + 0.05 #aumenta a temperatura em 0.05°C
                i0=i0+1

            else:
                print('Temperatura setpoint máxima do chiller:(°C)' ,t_chiller)
                print('Iterações:',i0)
                break
        print('Temperatura setpoint máxima do chiller:(°C)' ,t_chiller)
        print('Iterações:',i0)
        
    if a00==3:
        m_chiller_max=(int(input('Por favor, digite a capacidade de vazão máxima suportada pelo chiller: (L/h)')))/3600
        t_chiller_min=7
        otimizacao=True
        while t_tanque[3600]>t_0:
            if m_chiller<m_chiller_max and t_chiller>t_chiller_min: #se a temperatura do tanque estiver aumentando após 1h de ciclo.
                m_chiller = m_chiller + 0.001 #aumentar o fluxo em 10 L/h
                t_chiller = t_chiller - 0.05 #diminuir temperatura em 0.05°C.
                ciclo()
                i0=i0+1
            
            else:
                otimizacao=False
                print("Sistema subdimensionado, váriaveis máximas disponíveis abaixo:")
                print('Vazão necessária de água gelada (L):',m_chiller*3600)
                print('Temperatura setpoint máxima do chiller:(°C)' ,t_chiller)
                break
                
        if otimizacao==True:
            print("Otimização bem sucedida, váriaveis máximas disponíveis abaixo:")
            print('Vazão necessária de água gelada (L/h):',m_chiller*3600)
            print('Temperatura setpoint máxima do chiller:(°C)' ,t_chiller)

#adicionar temperatura admissível para processo
#adicionar resfriament ode água e quanto tempo o reservatório mantém uma temp admissível.
#melhorar calculo para temperatura
#adicionar perda de temperatura do reserv. para ambiente
    
'''
    Anotações:
       e_ent =  m_processo * cp_agua * abs(t_0-t_processo) #energia total que entra #ERRO
                x=np.linspace(0,m_chiller_max,10000) #equiv vazão
                y=np.linspace(7,t_chiller_max,10000) #equiv. t_chiller
                            
                for x1,y1 in zip(x,y):
                    energia=x1*cp_agua*(t_0-y1) #saldo térmico por instante

                    if ((energia>e_ent) and (energia<1.1*e_ent)):
                        energia_list.append(energia)
                        vazao=round(x1*3600,2)
                        valores_vazao.append(vazao)
                        valores_temp.append((round(y1,2)))
                   
                        
                #indice_maiores = np.argsort(valores_energia)[-10:]
                #maiores_valores = [valores_energia[i] for i in indice_maiores]    
                
                #print(indice_maiores,maiores_valores)
        result=list(zip(valores_temp,valores_vazao))
            print(*result, sep="\n")
            print('Combinações em cada linha: TEMPERATURA SETPOINT(°C), VAZÃO (L/h)')
         
            #np.array(result) 
            
            
            #saldo_termico = e_ent-e_sai
'''