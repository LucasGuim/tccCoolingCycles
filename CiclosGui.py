import PySimpleGUI as sg
from Equipamentos import *
from CoolProp.CoolProp import PropsSI as Prop
from Ciclos import *
from Telas import *


#Tela inicial 
janela1,janela2= janela_Inicial(),None
refrigerantes=[]

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
        janela2 = telaCicloFlashCaso1()
        janela1.hide()
        janela2.bring_to_front()
    if window == janela1 and event =='Continuar' and values['CicloCameraFlashCaso2'] == True:        
        janela2 = telaCicloFlashCaso2()
        janela1.hide()
        janela2.bring_to_front()
    if window == janela1 and event =='Continuar' and values['CicloSimplesTrocador'] == True:        
        janela2 = janela_CicloSimplesComTrocador()
        janela1.hide()
        janela2.bring_to_front()
    if window == janela2 and event == 'Voltar':
        janela2.hide()
        janela1.un_hide()
    if window == janela2   and event == sg.WIN_CLOSED:
        break
    if window == janela2   and event == 'Adicionar':
        Fluido = values['Refri']
        refrigerantes.append(Fluido)
        print(refrigerantes)

    #Tela Ciclo Simples
    if window == janela2 and event == 'Executar':
        TemperaturaEvaporador = float(values['Te']) + 273.15
        TemperaturaCondensador = float(values['Tc']) + 273.15
        Tsa = float(values['Tsa'])
        Tsub = float(values['Tsub'])
        Nis = values['Nis']
        CF = float(values['CF'])
        try:
            cicloSimples= RefrigeranteMaisEficienteCicloSimples(refrigerantes=refrigerantes,Function=CicloCompressaoDeVaporComTemperaturas,CF=CF,t_cond=TemperaturaCondensador,t_evap=TemperaturaEvaporador,t_superA=Tsa,Nis=Nis,t_sub=Tsub)
            if cicloSimples.erro == True:
                sg.popup_error(cicloSimples.errorType,title='Error')
            cicloSimples.CriaTabelas2('Simples')
            sg.popup(f'O refrigerante mais eficiente nessas codições é o {cicloSimples.fluid} e sua tabela foi criada com sucesso !')
        except ValueError:
           print('Valores de input inadequados') 
    #Tela Ciclo com Flash 1         
    if window == janela2 and event == 'Calcular ':
        Nis = values['Nis']
        CF = float(values['CF'])
        TemperaturaEvaporador = float(values['Te'])
        TemperaturaCondensador = float(values['Tc'])
        Tsa = float(values['Tsa'])
        Tsub = float(values['Tsub'])
        PressaoInt = float(values['Pint'])
        try:
            cicloFlash1= RefrigeranteMaisEficienteCiclosFlash(refrigerantes=refrigerantes,Function=CicloDuplaCompressaoComFlash,Tc=TemperaturaCondensador,Te=TemperaturaEvaporador,Tsub=Tsub,Tsa=Tsa,Pint=PressaoInt,CF=CF,Nis=Nis)
            
            if cicloFlash1.erro == True:
                sg.popup_error(cicloFlash1.errorType)
            cicloFlash1.CriaTabelas2("Flash tipo-2")
            sg.popup(f'O refrigerante mais eficiente nessas codições é o {cicloFlash1.fluid} e sua tabela foi criada com sucesso !')
        except ValueError:
            sg.popup_error('Valores de input inadequados') 
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
           cicloCascata= CicloCascata3Pressoes(fluidoSup=RefrigerantePH,fluidoInf=RefrigerantePL,THcond=TemperaturaCondPH,THevap=TemperaturaEvaPH,TLcond=TemperaturaCondPL,TLeva=TemperaturaEvaPL,CapacidadeFrigorifica=CF,NisHP=NisHP,NisLP=NisLP,TsaHP=TemperaturaSaPH,TsaLP=TemperaturaSaPL)
           if cicloCascata.erro == True:
                sg.popup_error(cicloCascata.errorType)
           sg.popup(f'COP do ciclo é: {cicloCascata.COP}. Tabela criada com sucesso !')
        except ValueError:
            sg.popup_error('Valores de input inadequados') 
    #Tela Ciclo com Flash 2
    if window == janela2 and event == 'Calcular  ':
        Nis = values['Nis']
        CF = float(values['CF'])
        TemperaturaEvaporador = float(values['Te'])
        TemperaturaCondensador = float(values['Tc'])
        Tsa = float(values['Tsa'])
        Tsub = float(values['Tsub'])
        PressaoInt = float(values['Pint'])
        try:
            cicloFlash2= RefrigeranteMaisEficienteCiclosFlash(refrigerantes=refrigerantes,Function=CicloComFlashCaso2, Tc=TemperaturaCondensador,Te=TemperaturaEvaporador,Tsub=Tsub,Tsa=Tsa,Pint=PressaoInt,CF=CF,Nis=Nis)
            
            if cicloFlash2.erro == True:
                sg.popup_error(cicloFlash2.errorType)
            cicloFlash2.CriaTabelas2("Flash tipo-1")
            sg.popup(f'O refrigerante mais eficiente nessas codições é o {cicloFlash2.fluid} e sua tabela foi criada com sucesso !')
        except ValueError:
            sg.popup_error('Valores de input inadequados') 
    # Ciclo com trocador
    if window == janela2 and event == 'Executar ':
        TemperaturaEvaporador = float(values['Te']) + 273.15
        TemperaturaCondensador = float(values['Tc']) + 273.15
        Nis = values['Nis']
        CF = float(values['CF'])
        try:
            cicloSimples= RefrigeranteMaisEficienteCicloSimples(refrigerantes=refrigerantes,Function=CicloCompressaoDeVaporComTemperaturas,CF=CF,t_cond=TemperaturaCondensador,t_evap=TemperaturaEvaporador,t_superA=Tsa,Nis=Nis,t_sub=Tsub)
            if cicloSimples.erro == True:
                sg.popup_error(cicloSimples.errorType,title='Error')
            cicloSimples.CriaTabelas2('Simples')
            sg.popup(f'O refrigerante mais eficiente nessas codições é o {cicloSimples.fluid} e sua tabela foi criada com sucesso !')
        except ValueError:
           print('Valores de input inadequados') 
   
    



    
       
           
        
            
    
      
            
            
            
            
            
