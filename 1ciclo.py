
from Equipamentos_MkII import *
from CoolProp.CoolProp import PropsSI as Prop
from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference, 
    Series
)
import os
def CicloCompressaoDeVaporComTemperaturas (fluido,t_evap ,t_cond, vazao_refrigerante,t_superA='sat'):
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
CicloCompressaoDeVaporComTemperaturas('R134a',253,313,0.03)


  


