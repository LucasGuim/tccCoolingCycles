import CoolProp
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
def CicloCompressaoDeVaporComPePc (fluido, vazao_refrigerante,Pe,Pc):
    ''' 
        Parametros:
            fluido: Fluido refrigerante
            eficiencia_is: Eficiencia isentropica do compressor
            Pc: Pressão no condenssador O
            Pe: Pressão no evaporador [K]
            vazao_refrigerante: fluxo do refrigerante 
    '''
    

    cycle = SimpleCompressionCycle('HEOS::R134a', 'PH', unit_system='EUR')
    T0 = Prop('T','P',Pe*1e3,'Q',1,fluido)
    T2 = Prop('T','P',Pc*1e3,'Q',0,fluido)
    cycle.simple_solve(T0, Pe, T2, Pc, 1, SI=True)
    cycle.steps = 50
    sc = cycle.get_state_changes()
    Cop=cycle.COP_cooling()
    print(cycle._cycle_states)
    print(Cop) 
    # ciclo = Ciclo(4,fluido)
    # ciclo.Evapout(i=1,Pl=Pe*1e3,Tsa='sat')
    # P_alta = (Prop('P','T',t_cond,'Q',0,fluido))/1e3
    # ciclo.Compress()
    # ciclo.Condout(3,2,P_alta,'sat')
    # P_baixa = ciclo.p[1]/1e3
    # ciclo.VE(4,ciclo.p[1],3)
    # m = vazao_refrigerante
    # ciclo.SetMass(1,m)
    # ciclo.Tub(1,2,3,4)
    # Cop = ciclo.Resultados()
    # print('COP',Cop)
    # ciclo.Exibir('h','p','s')
    # print(ciclo.T[1])



CicloCompressaoDeVaporComPePc('R134a',1,131.87692,1200)