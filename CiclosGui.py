import PySimpleGUI as sg
from Equipamentos import *
from CoolProp.CoolProp import PropsSI as Prop
from Ciclos import CicloCompressaoDeVaporComTemperaturas, CicloDuplaCompressaoComFlash,CicloCascata3Pressoes,CicloComFlashCaso1
from telas import *


#Tela inicial 
janela1,janela2= janela_Inicial(),None

#Cria um loop de leitura de eventos nas telas 
while True:
    window,event,values = sg.read_all_windows()
    if window == janela1   and event == sg.WIN_CLOSED:
        break
    #Gerando a tela do ciclo escolhido 
    if window == janela1 and event =='Continuar' and values['CicloSimples'] == True:        
        janela2 = janela_CicloSimples()
        janela1.hide()
        janela2.bring_to_front()
    if window == janela1 and event =='Continuar' and values['CicloCascataSimples'] == True:        
        janela2 = janela_CicloCascataSimples()
        janela1.hide()
        janela2.bring_to_front()
    if window == janela1 and event =='Continuar' and values['CicloCameraFlash'] == True:        
        janela2 = janela_CicloCameraFlash()
        janela1.hide()
        janela2.bring_to_front()
    if window == janela1 and event =='Continuar' and values['CicloCameraFlashCaso2'] == True:        
        janela2 = janela_CicloFlashCaso2()
        janela1.hide()
        janela2.bring_to_front()
    if window == janela2 and event == 'Voltar':
        janela2.hide()
        janela1.un_hide()
    if window == janela2   and event == sg.WIN_CLOSED:
        break
    #Tela Ciclo Simples
    if window == janela2 and event == 'Executar':
        TemperaturaEvaporador = float(values['Te']) + 273.15
        TemperaturaCondensador = float(values['Tc']) + 273.15
        Tsa = float(values['Tsa'])
        Tsub = float(values['Tsub'])
        Nis = values['Nis']
        Fluido = values['Combo']
        try:
            cicloSimples= CicloCompressaoDeVaporComTemperaturas(fluido=Fluido,t_cond=TemperaturaCondensador,t_evap=TemperaturaEvaporador,t_superA=Tsa,vazao_refrigerante=1,Nis=Nis,t_sub=Tsub)
            cicloSimples.CriaTabelas2('Simples')
            print(f' Tabela criada com sucesso! ')
        except ValueError:
           print('Valores de input inadequados') 
    #Tela Ciclo com Flash          
    if window == janela2 and event == 'Calcular ':
        Nis = values['Nis']
        Fluido = values['Refri']
        CF = float(values['CF'])
        PressaoEvaporador = float(values['Pe'])
        PressaoCondensador = float(values['Pc'])
        PressaoInt = float(values['Pint'])
        try:
            CicloDuplaCompressaoComFlash(fluido=Fluido, Pc=PressaoCondensador,Pe=PressaoEvaporador,Pint=PressaoInt,CF=CF,Nis=Nis)
        except ValueError:
            print('Valores de input inadequados') 
    #Tela Ciclo Cascata
    if window == janela2 and event == 'Calcular':
        RefrigerantePH = values['RefriHP']
        RefrigerantePL = values['RefriPL']
        NisHP = values['NisHP']
        NisLP = values['NisLP']
        TemperaturaCondPH= float(values['TcHP']) + 273.15 
        TemperaturaEvaPH= float(values['TeHP']) + 273.15
        TemperaturaSaPH= float(values['TsaHP'])
        TemperaturaCondPL= float(values['TcLP']) + 273.15
        TemperaturaEvaPL= float(values['TeLP']) + 273.15
        TemperaturaSaPL= float(values['TsaLP'])
        CF = float(values['CF'])
        try:
            CicloCascata3Pressoes(fluidoSup=RefrigerantePH,fluidoInf=RefrigerantePL,THcond=TemperaturaCondPH,THevap=TemperaturaEvaPH,TLcond=TemperaturaCondPL,TLeva=TemperaturaEvaPL,CapacidadeFrigorifica=CF,NisHP=NisHP,NisLP=NisLP,TsaHP=TemperaturaSaPH,TsaLP=TemperaturaSaPL)
        except ValueError:
            print('Valores de input inadequados') 
    if window == janela2 and event == 'Calcular  ':
        Nis = values['Nis']
        Fluido = values['Refri']
        CF = float(values['CF'])
        TemperaturaEvaporador = float(values['Te'])
        TemperaturaCondensador = float(values['Tc'])
        PressaoInt = float(values['Pint'])
        try:
            CicloComFlashCaso1(fluido=Fluido, Tc=TemperaturaCondensador,Te=TemperaturaEvaporador,Pint=PressaoInt,CF=CF,Nis=Nis)
        except ValueError:
            print('Valores de input inadequados') 
   
   
    



    
       
           
        
            
    
      
            
            
            
            
            
