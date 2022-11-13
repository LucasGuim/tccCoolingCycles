import PySimpleGUI as sg
from Equip_metodos import *
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
        janela2 = telaCicloFlashCaso2()
        janela1.hide()
        janela2.bring_to_front()
    if window == janela1 and event =='Continuar' and values['CicloCameraFlashCaso2'] == True:        
        janela2 = telaCicloFlashCaso1()
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
    if window == janela2   and event == 'Error':
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
                sg.popup_error(cicloSimples.errorType,title='Error',modal=True)              
            if cicloSimples.COP != 0:
                cicloSimples.CriaTabelas1('Simples')
                sg.popup(f'O refrigerante mais eficiente nessas codições é o {cicloSimples.fluid} e sua tabela foi criada com sucesso !')
        except:
           sg.popup_error('Something went wrong...')  
           break
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
                sg.popup_error(cicloFlash1.errorType,title='Error',modal=True)
                
            if cicloFlash1.COP > 0:
                cicloFlash1.CriaTabelas1("Flash tipo-2")
                sg.popup(f'O refrigerante mais eficiente nessas codições é o {cicloFlash1.fluid} e sua tabela foi criada com sucesso !')
        except:
            sg.popup_error('Something went wrong...') 
            break
    #Tela Ciclo Cascata
    if window == janela2 and event == 'Calcular':
        RefrigerantePH = values['RefriHP']
        RefrigerantePL = values['RefriPL']
        NisHP = values['NisHP']
        NisLP = values['NisLP']
        TemperaturaCondPH= float(values['TcHP']) + 273.15 
        TemperaturaEvaPH= float(values['TeHP']) + 273.15
        TemperaturaSaPH= float(values['TsaHP'])
        SubResfriPH= float(values['TsubH'])
        TemperaturaCondPL= float(values['TcLP']) + 273.15
        TemperaturaEvaPL= float(values['TeLP']) + 273.15
        TemperaturaSaPL= float(values['TsaLP'])
        SubResfriPL= float(values['TsubL'])
        CF = float(values['CF'])
        cicloCascata= CicloCascata3Pressoes(fluidoSup=RefrigerantePH,fluidoInf=RefrigerantePL,THcond=TemperaturaCondPH,THevap=TemperaturaEvaPH,TLcond=TemperaturaCondPL,TLeva=TemperaturaEvaPL,CapacidadeFrigorifica=CF,NisHP=NisHP,NisLP=NisLP,TsaHP=TemperaturaSaPH,TsaLP=TemperaturaSaPL,TsubL=SubResfriPL,TsubH=SubResfriPH)
        if cicloCascata.erro == True:
                sg.popup_error(cicloCascata.errorType)
        sg.popup(f'COP do ciclo é: {cicloCascata.COP}. Tabela criada com sucesso !')
        


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
                sg.popup_error(cicloFlash2.errorType,title='Error',modal=True)
            if cicloFlash2.COP > 0:
                cicloFlash2.CriaTabelas1("Flash tipo-1")
                sg.popup(f'O refrigerante mais eficiente nessas codições é o {cicloFlash2.fluid} e sua tabela foi criada com sucesso !')           
            
        except:
            sg.popup_error('Something went wrong...') 
            break
    # Ciclo com trocador
    if window == janela2 and event == 'Executar ':
        TemperaturaEvaporador = float(values['Te']) + 273.15
        TemperaturaCondensador = float(values['Tc']) + 273.15
        Nis = values['Nis']
        CF = float(values['CF'])
        try:
            cicloSimples= RefrigeranteMaisEficienteCicloSimples(refrigerantes=refrigerantes,Function=CicloSimplesComTrocador,CF=CF,t_cond=TemperaturaCondensador,t_evap=TemperaturaEvaporador,t_superA=0,Nis=Nis,t_sub=0)
            if cicloSimples.erro == True:
                sg.popup_error(cicloSimples.errorType,title='Error',modal=True)
            if cicloSimples.COP > 0:
                cicloSimples.CriaTabelas1('Simples com Trocador de calor')
                sg.popup(f'O refrigerante mais eficiente nessas codições é o {cicloSimples.fluid} e sua tabela foi criada com sucesso !')
        except:
           sg.popup_error('Something went wrong...')
           break
   
    



    
       
           
        
            
    
      
            
            
            
            
            
