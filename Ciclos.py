import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot
from CoolProp.Plots import SimpleCompressionCycle
from Equipamentos import *
from CoolProp.CoolProp import PropsSI as Prop

def CicloCompressaoDeVaporComTemperaturas (fluido,t_evap,t_cond, vazao_refrigerante,t_superA='sat',Nis=1.0,t_sub='sat'):
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
    P_baixa = (Prop('P','T',t_evap,'Q',1,fluido))/1e3
    ciclo.Evapout(1,Pl=P_baixa,Tsa=t_superA,T=t_evap)
    P_alta = (Prop('P','T',t_cond,'Q',0,fluido))/1e3
    ciclo.Compress(2,P_alta,1,Nis=Nis)
    ciclo.CondRef(3,P_alta,t_sub)
    ciclo.VE(4,ciclo.p[1],3)
    m = vazao_refrigerante
    ciclo.SetMass(1,m)
    ciclo.Tub(1,2,3,4)
    ciclo.COP = round(ciclo.ResultadosCop(),2)
    print('COP',ciclo.COP)
    ciclo.CriaTabelas2()
    
def CicloCascata3Pressoes(fluidoSup,fluidoInf,THcond,THevap,TLcond,TLeva,CapacidadeFrigorifica,TsaHP='sat',TsaLP='sat',NisHP=1.0,NisLP=1.0):
    #Ciclo High Pressure
    cicloHigh = Ciclo(4,fluidoSup)
    PHevap = (Prop('P','T',THevap,'Q',1,fluidoSup))/1e3
    cicloHigh.Evapout(1,Pl=PHevap,Tsa=TsaHP,T=THevap)
    PHcond = Prop('P','T',THcond,'Q',0,fluidoSup)/1e3
    cicloHigh.Compress(2,PHcond,1,Nis=NisHP)
    cicloHigh.Condout(3,2,PHcond,'sat')
    cicloHigh.VE(4,cicloHigh.p[1],3)
    
    CfCicloHigh = cicloHigh.ResultadosCf()
    #Ciclo Low Pressure
    cicloLow = Ciclo(4,fluidoInf)
    PLevap = (Prop('P','T',TLeva,'Q',1,fluidoInf))/1e3
    cicloLow.Evapout(1,Pl=PLevap,Tsa=TsaLP,T=TLeva)
    PLcond = Prop('P','T',TLcond,'Q',0,fluidoInf)/1e3
    cicloLow.Compress(2,PLcond,1,Nis=NisLP)
    cicloLow.Condout(3,2,PLcond,'sat')
    cicloLow.VE(4,cicloLow.p[1],3)

    #Descobrindo as vazões de refrigerante 
    #     
    vazao_refrigeranteLow = round(CapacidadeFrigorifica/cicloLow.ResultadosCf(),2)
    CalorExpelidoCondensadorLow = cicloLow.h[2] - cicloLow.h[3]
    vazao_refrigeranteHigh= (vazao_refrigeranteLow*CalorExpelidoCondensadorLow)/CfCicloHigh 
    #Calculando os trabalhos dos compressores

    WbLow = cicloLow.ResultadosWc()
    WbHigh = cicloHigh.ResultadosWc()

    TrabalhoNoCompressorLow = round((cicloLow.ResultadosWc())*vazao_refrigeranteLow,2)    
    TrabaloCompressorHigh = round(vazao_refrigeranteHigh*WbHigh,2)

    cicloLow.SetMass(1,vazao_refrigeranteLow)
    cicloLow.Tub(1,2,3,4)
    cicloHigh.Exibir('h','p','s','T','x')
    print('ciclo inferior')
    WbTotal= TrabaloCompressorHigh + TrabalhoNoCompressorLow
    
    COP = round(CapacidadeFrigorifica/WbTotal,2)
    cicloLow.COP,cicloHigh.COP=COP

    cicloLow.Exibir('h','p','s','T','x')
    print(f'COP do ciclo é: {COP}',f'WTh:{TrabaloCompressorHigh} e WTl: {TrabalhoNoCompressorLow} , vazão Ciclo de baixa: {vazao_refrigeranteLow} ' )
    
def CicloDuplaCompressaoComFlash(fluido,Pc,Pe,Pint,CF,Nis=1.0):

    ciclo = Ciclo(9,fluido)
    #Definindo pontos 1 e 2 
    ciclo.Evapout(1,Pe,'sat')
    ciclo.Compress(2,Pint,1,Nis=Nis)
    # Defindo saida do condensador
    ciclo.Condout(5,4,Pc,'sat')
    #Primeira valvula de expansão 
    ciclo.VE(6,Pint,5)
    #Camera Flash 
    ciclo.Tflash(7,9,6,P=Pint)
    ciclo.VE(8,Pe,7)
    #Camera de Mistura
    ciclo.CameraMistura(3,2,9)
    #Segundo compressor
    ciclo.Compress(4,Pc,1,Nis=Nis)
    #Taxa de calor absorvido no compressor por kg de refrigerante
    qh = ciclo.h[1] - ciclo.h[8]
    #Descobrindo as vazões de refrigerante

    VazaoEvap = round(CF/qh,3)
    VazaoCond = round(VazaoEvap/(1-ciclo.x[6]),3)
    #Trabalho dos compressores

    WbCompressorBaixa = VazaoEvap*(ciclo.h[2]-ciclo.h[1])
    WbCompressorAlta = VazaoCond*(ciclo.h[4]-ciclo.h[3])
    WbTotal = WbCompressorAlta + WbCompressorBaixa
    #Calculo do COP
    COP = round(CF/WbTotal,3)
    ciclo.COP = COP
    ciclo.CriaTabelas2()
    print(VazaoCond,VazaoEvap,WbCompressorAlta,WbCompressorBaixa,COP,sep=' , ')
    ciclo.Exibir('h','p','s','T','x')
    
#CicloDuplaCompressaoComFlash('R134a',1100,107.2,400,52.76)






