from tkinter import *
import CoolProp
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
def CicloCompressaoDeVaporComTemperaturas (fluido,t_evap,t_cond, vazao_refrigerante=0,t_superA='sat'):
    '''
        Descricao:
            

        Parametros:
            fluido: Fluido refrigerante
            eficiencia_is: Eficiencia isentropica do compressor
            Pc: Pressão no condenssador kPa
            Pe: Pressão no evaporador kPa
            vazao_refrigerante: fluxo do refrigerante kg/s 
            t_superA: Temperatura de superaquecimento K 

        
    '''
    # t_evap = int(input("Entre com a temperatura do refrigerante no evaporador em K :"))
    # t_cond=int(input("Entre com a temperatura do refrigerante no condensador em K :"))

    
    
    ciclo = Ciclo(4,fluido)
    ciclo.T[1]=t_evap
    ciclo.Evapout(1,'sat',t_superA,t_evap)
    P_alta = (Prop('P','T',t_cond,'Q',0,fluido))/1e3
    ciclo.Compress(2,P_alta,1,1)
    ciclo.Condout(3,2,P_alta,'sat')
    P_baixa = ciclo.p[1]/1e3
    ciclo.VE(4,ciclo.p[1],3)
    m = vazao_refrigerante
    ciclo.SetMass(1,m)
    ciclo.Tub(1,2,3,4)
    Cop = ciclo.ResultadosCop()
    Wb = ciclo.ResultadosWc()*m
    Cf = ciclo.ResultadosCf()*m
    print(f'Wb:{Wb} kW, CF:{Cf} kW, COP: {Cop} ')
    ciclo.Exibir('h','p','s','T','x')
    print(ciclo.T[1])
    
    
CicloCompressaoDeVaporComTemperaturas('R12',258,318,1) 



# janela = Tk()





# janela.title("Cotações em tempo real: ")
# titulo = Label(janela,text='Clique no botão para atualizar as cotações das moedas. ',padx=10)
# titulo.grid(column=0,row=0,pady=10)
# botão = Button(janela,text='Executar',command=pegar_cotacoes,pady=5,padx=5)
# botão.grid(column=0,row=1)
# cotacoes = Label(janela,text='',pady=10)
# cotacoes.grid(column=0,row=2,)

# janela.mainloop()
  


