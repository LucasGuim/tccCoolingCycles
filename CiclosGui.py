import PySimpleGUI as sg
from numpy import size 
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot
from CoolProp.Plots import SimpleCompressionCycle
from Equipamentos import *
from CoolProp.CoolProp import PropsSI as Prop
from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference, 
    Series
)
import os
from Ciclos import CicloCompressaoDeVaporComTemperaturas, CicloDuplaCompressaoComFlash
from Ciclos import CicloCascata3Pressoes

def janela_Inicial():
    
    layout = [  [sg.Text('Olá, meu mestre ')],
                [sg.Text('Qual tipo de ciclo quer calcular ?')],
                [sg.Radio('Ciclo Simples','Ciclo',key='CicloSimples'),sg.Radio('Ciclo Cascata','Ciclo',key='CicloCascataSimples'),sg.Radio('Ciclo com camera Flash','Ciclo',key='CicloCameraFlash')],
                [sg.Button('Continuar')]
            ]
    return sg.Window('Login',layout=layout,finalize=True)

def janela_CicloSimples():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Calcule a eficiência do seu ciclo de refrigeração  ')],
            [sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a'),key='Combo')],           
            [sg.Text('Temperatura do refrigerante no condensador em °C:'),sg.Input(key='Tc',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador em °C:'),sg.Input(key='Te',size=(5,5))],
            [sg.Button('Voltar'),sg.Button('Executar')],
            [sg.Output(size=(40,15))]           ]
    return sg.Window('Ciclo de compreesão simples',layout=layout,finalize=True)
def janela_CicloCascataSimples():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Capacidade Frigorífica em KW'),sg.Input(key='CF',size=(5,5))],
            [sg.Text('Fluido refrigerante ciclo de pressão alta'),sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a','R22'),key='RefriHP')],
            [sg.Text('Fluido refrigerante ciclo de pressão baixa'),sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a','R22'),key='RefriPL')],            
            [sg.Text('Temperatura do refrigerante no condensador de alta pressão em °C:'),sg.Input(key='TcHP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador de alta pressão em °C:'),sg.Input(key='TeHP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no condensador de baixa pressão em °C:'),sg.Input(key='TcLP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador de baixa pressão em °C:'),sg.Input(key='TeLP',size=(5,5))],
            [sg.Button('Voltar'),sg.Button('Calcular')],
            [sg.Output(size=(50,30))]  
            ]
    return sg.Window('Ciclo Cascata',layout=layout,finalize=True)
def janela_CicloCameraFlash():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Capacidade Frigorífica em KW'),sg.Input(key='CF',size=(5,5))],
            [sg.Text('Fluido refrigerante'),sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a','R22'),key='Refri')],
                    
            [sg.Text('Pressão no condensador em kPa:'),sg.Input(key='Pc',size=(5,5))],
            [sg.Text('Pressão no evaporador  em kPa:'),sg.Input(key='Pe',size=(5,5))],
            [sg.Text('Pressão Intermediaria'),sg.Input(key='Pint',size=(5,5))],
            
            [sg.Button('Voltar'),sg.Button('Calcular ')],
            [sg.Output(size=(40,15))]  
            ]
    return sg.Window('Ciclo com Camera Flash',layout=layout,finalize=True)


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
    if window == janela2 and event == 'Voltar':
        janela2.hide()
        janela1.un_hide()
    if window == janela2   and event == sg.WIN_CLOSED:
        break
    #Tela Ciclo Simples
    if window == janela2 and event == 'Executar':
        TemperaturaEvaporador = int(values['Te']) + 273
        TemperaturaCondensador = int(values['Tc']) + 273
        Fluido = values['Combo']
        CicloCompressaoDeVaporComTemperaturas(fluido=Fluido,t_cond=TemperaturaCondensador,t_evap=TemperaturaEvaporador,t_superA=0,vazao_refrigerante=1) 
    #Tela Ciclo com Flash          
    if window == janela2 and event == 'Calcular ':
        Fluido = values['Refri']
        CF = float(values['CF'])
        PressaoEvaporador = float(values['Pe'])
        PressaoCondensador = float(values['Pc'])
        PressaoInt = float(values['Pint'])
        CicloDuplaCompressaoComFlash(fluido=Fluido, Pc=PressaoCondensador,Pe=PressaoEvaporador,Pint=PressaoInt,CF=CF)
    #Tela Ciclo Cascata
    if window == janela2 and event == 'Calcular':
        RefrigerantePH = values['RefriHP']
        RefrigerantePL = values['RefriPL']
        TemperaturaCondPH= float(values['TcHP']) + 273 
        TemperaturaEvaPH= float(values['TeHP']) + 273
        TemperaturaCondPL= float(values['TcLP']) + 273
        TemperaturaEvaPL= float(values['TeLP']) + 273
        CF = float(values['CF'])       
        CicloCascata3Pressoes(fluidoSup=RefrigerantePH,fluidoInf=RefrigerantePL,THcond=TemperaturaCondPH,THevap=TemperaturaEvaPH,TLcond=TemperaturaCondPL,TLeva=TemperaturaEvaPL,CapacidadeFrigorifica=CF)
        
   
   
    



    
       
           
        
            
    
      
            
            
            
            
            
