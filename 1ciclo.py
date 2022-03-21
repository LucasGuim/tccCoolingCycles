
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
def CicloCompressaoDeVaporComTemperaturas (fluido, vazao_refrigerante,t_superA='sat'):
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
    t_evap = int(input("Entre com a temperatura do refrigerante no evaporador em K :"))
    t_cond=int(input("Entre com a temperatura do refrigerante no condensador em K :"))

    
    
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
    
    # pp = PropertyPlot('HEOS::R134a', 'PH', unit_system='EUR')
    # pp.calc_isolines(CoolProp.iQ, num=11)
    # cycle = SimpleCompressionCycle('HEOS::R134a', 'PH', unit_system='EUR')
    # T0 = t_evap 
    # pp.state.update(CoolProp.QT_INPUTS,0.0,T0-10)
    # p0 = pp.state.keyed_output(CoolProp.iP)
    # T2 = t_cond  
    # pp.state.update(CoolProp.QT_INPUTS,1.0,T2+15)
    # p2 = pp.state.keyed_output(CoolProp.iP)
    # pp.calc_isolines(CoolProp.iT, [T0-273.15,T2-273.15], num=2)
    # cycle.simple_solve(T0, p0, T2, p2, 0.7,'HEOS::R134a', SI=True)
    # cycle.steps = 50
    # sc = cycle.get_state_changes()
    # pp.draw_process(sc)    
    # plt.close(cycle.figure)
    # pp.show()
    

CicloCompressaoDeVaporComTemperaturas('R134a',0.03)


  


