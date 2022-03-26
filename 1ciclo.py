
from tkinter import Label
from tkinter.ttk import Button
import CoolProp
from kivy.app import App
from kivy.lang import Builder
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot
from CoolProp.Plots import SimpleCompressionCycle
from Equipamentos_MkII import *
from CoolProp.CoolProp import PropsSI as Prop
from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference, 
    Series
)
import os
def CicloCompressaoDeVaporComTemperaturas (fluido,t_evap,t_cond, vazao_refrigerante,t_superA='sat'):
    '''
        Descricao:
            

        Parametros:
            fluido: Fluido refrigerante
            eficiencia_is: Eficiencia isentropica do compressor
            t_cond: Temperatura do refrigerante no condenssador [K]
            t_evap: Temperatura do refrigerante no evaporador [K]
            vazao_refrigerante: fluxo do refrigerante 
            t_superA: Temperatura de superaquecimento K 

        
    '''
   

    
    
    ciclo = Ciclo(4,fluido)
    ciclo.Evapout(1,'sat',t_superA,t_evap)
    P_alta = (Prop('P','T',t_cond,'Q',0,fluido))/1e3
    ciclo.Compress(2,P_alta,1,1)
    ciclo.Condout(3,2,P_alta,'sat')
    P_baixa = ciclo.p[1]/1e3
    ciclo.VE(4,ciclo.p[1],3)
    m = vazao_refrigerante
    ciclo.SetMass(1,m)
    ciclo.Tub(1,2,3,4)
    Cop = ciclo.Resultados()
    print('COP',Cop)
    ciclo.Exibir('h','p','s')
    print(ciclo.T[1])
    
    
    

#CicloCompressaoDeVaporComTemperaturas('R134a',0.03)
import PySimpleGUI as sg


class TelaPython:
    def __init__(self):
        layout = [
            [sg.Text('Calcule a eficiência do seu ciclo de refrigeração  ')],
            [sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a'),key='Combo')],           
            [sg.Text('Temperatura do refrigerante no evaporador em °C:'),sg.Input(key='Te',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no condensador em °C:'),sg.Input(key='Tc',size=(5,5))],
            [sg.Text('É um ciclo Cascata ?')],
            [sg.Radio('Sim','Cascata',key='temPrIntermediaria'),sg.Radio('Não','Cascata',key='naoTemPintermediaria')],
            [sg.Text('Pressão intermediária'),sg.Input(key='Pint')],
            [sg.Button('Enviar')],
            [sg.Output(size=(40,15))]
        ]
        self.janela = sg.Window("Formulário da madrugada").layout(layout)

        
    def Iniciar (self):
        while True:
            self.button,self.values = self.janela.Read()
            TemperaturaEvaporador = int(self.values['Te']) + 273
            TemperaturaCondensador = int(self.values['Tc']) + 273
            Fluido = self.values['Combo']
            if self.values['temPrIntermediaria'] == True:
                tem_PrIntermediaria = 'Sim'
            else:
                tem_PrIntermediaria = 'Não'
            CicloCompressaoDeVaporComTemperaturas(fluido=Fluido,t_cond=TemperaturaCondensador,t_evap=TemperaturaEvaporador,t_superA=0,vazao_refrigerante=1)
            
            
            
tela = TelaPython()
tela.Iniciar()