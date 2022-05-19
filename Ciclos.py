

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
    ciclo.CondRef(3,P_alta,'sat')
    ciclo.subResfri(3,t_sub)
    ciclo.VE(4,ciclo.p[1],3)
    m = vazao_refrigerante
    ciclo.SetMass(1,m)
    ciclo.Tub(1,2,3,4)
    ciclo.COP = round(ciclo.ResultadosCop(),2)
    print('COP',ciclo.COP)
    return ciclo
    
    
    
def CicloCascata3Pressoes(fluidoSup,fluidoInf,THcond,THevap,TLcond,TLeva,CapacidadeFrigorifica,TsaHP='sat',TsaLP='sat',NisHP=1.0,NisLP=1.0,Tsub=0):
    #Ciclo High Pressure
    cicloHigh = Ciclo(4,fluidoSup)
    PHevap = (Prop('P','T',THevap,'Q',1,fluidoSup))/1e3
    cicloHigh.Evapout(1,Pl=PHevap,Tsa=TsaHP,T=THevap)
    PHcond = Prop('P','T',THcond,'Q',0,fluidoSup)/1e3
    cicloHigh.Compress(2,PHcond,1,Nis=NisHP)
    cicloHigh.Condout(3,2,PHcond,'sat')
    cicloHigh.subResfri(3,Tsub)
    cicloHigh.VE(4,cicloHigh.p[1],3)
    
    CfCicloHigh = cicloHigh.ResultadosCf()
    #Ciclo Low Pressure
    cicloLow = Ciclo(4,fluidoInf)
    PLevap = (Prop('P','T',TLeva,'Q',1,fluidoInf))/1e3
    cicloLow.Evapout(1,Pl=PLevap,Tsa=TsaLP,T=TLeva)
    PLcond = Prop('P','T',TLcond,'Q',0,fluidoInf)/1e3
    cicloLow.Compress(2,PLcond,1,Nis=NisLP)
    cicloLow.Condout(3,2,PLcond,'sat')
    cicloLow.subResfri(3,Tsub)
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
    cicloHigh.Exibir('h','p','s','T')
    print('---------------')
    print('Ciclo inferior')
    WbTotal= TrabaloCompressorHigh + TrabalhoNoCompressorLow
    
    COP = round(CapacidadeFrigorifica/WbTotal,2)
    cicloHigh.COP=COP
    cicloHigh.CriaTabelaCascata(cicloLow=cicloLow)

    cicloLow.Exibir('h','p','s','T')
    print(f'COP do ciclo é: {COP}. Tabela criada com sucesso.' )
    
def CicloDuplaCompressaoComFlash(fluido,Pc,Pe,Pint,CF,Nis=1.0,Tsub=0):

    ciclo = Ciclo(9,fluido)
    #Definindo pontos 1 e 2 
    ciclo.Evapout(1,Pe,Tsa=0)
    ciclo.Compress(2,Pint,1,Nis=Nis)
    # Defindo saida do condensador
    ciclo.Condout(5,4,Pc,'sat')
    ciclo.subResfri(5,Tsub)
    #Primeira valvula de expansão 
    ciclo.VE(6,Pint,5)
    #Camera Flash 
    ciclo.Tflash(7,9,[6],P=Pint)
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
    ciclo.CriaTabelas2("Flash Tipo-1")
    print(VazaoCond,VazaoEvap,WbCompressorAlta,WbCompressorBaixa,COP,sep=' , ')
    
    
#CicloDuplaCompressaoComFlash('R134a',1100,107.2,400,52.76)

def CicloComFlashCaso1(fluido,Tc,Te,Pint,CF,Nis=1.0,Tsub=0,Tsuper=0):
    ciclo = Ciclo(8,fluid=fluido)
    Tev = Te +273.15
    Tcond = Tc + 273.15
    #Calculando Pe 
    Pe = Prop('P','T',Tev,'Q',1,fluido)/1e3
    #Calculando Pc
    Pc = Prop('P','T',Tcond,'Q',0,fluido)/1e3
    #Ponto 1 e 2 
    ciclo.Evapout(1,Pe,Tsuper)
    ciclo.Compress(2,Pint,1,Nis)
    #Saida do condensador 
    ciclo.Condout(5,4,Pc,'sat')
    ciclo.subResfri(5,Tsub)
    ciclo.VE(6,Pint,5)
    X6 = round(ciclo.x[6],2)
    #Flash
    ciclo.Tflash(l=7,v=3,entrada=[2],P=Pint)
    ciclo.Compress(4,Pc,3,Nis)
    ciclo.VE(8,Pe,7)
    ciclo.T[3]= Prop('T','P',Pint*1e3,'Q',1,fluido)
    ciclo.T[7]= Prop('T','P',Pint*1e3,'Q',0,fluido)
    ciclo.Exibir('h','s','p','T')
    Ql = ciclo.h[1]-ciclo.h[8]
    M1 =round(CF/Ql,3)
    BalancoEnergia = round((ciclo.h[2]-ciclo.h[7])/(ciclo.h[6]-ciclo.h[3]),2)
    M3 = round(M1*BalancoEnergia,2)*-1
    Wcb = round(M1*(ciclo.h[2]-ciclo.h[1]),2)
    Wca = round(M3*(ciclo.h[4]-ciclo.h[3]),2)
    Wtotal = Wca + Wcb
    COP = round(CF/Wtotal,2)
    ciclo.COP = COP
    ciclo.CriaTabelas2("Flash tipo-2")
    
    print(M1,M3,X6,Wcb,Wca,COP)
    
#CicloComFlashCaso1(fluido='R717',Tc=24.9,Te=-20,Pint=500,CF=249.7,Tsuper=0,Tsub=0)

def RefrigeranteMaisEficienteCicloSimples(refrigerantes,t_evap,t_cond, vazao_refrigerante,t_superA=0,Nis=1.0,t_sub=0):
    copCicloHighest = 0
    for fluido in refrigerantes:
        ciclo = CicloCompressaoDeVaporComTemperaturas(fluido=fluido,t_evap=t_evap,t_cond=t_cond,t_sub=t_sub,t_superA=t_superA,Nis=Nis,vazao_refrigerante=1)
        if(ciclo.COP > copCicloHighest):
            copCicloHighest=ciclo.COP
            cicloHighest=ciclo
    print(cicloHighest.COP)


RefrigeranteMaisEficienteCicloSimples(refrigerantes=['R134a','Water','R717','R600a','R290','R1234yf', 'R1234ze(E)', 'R410a'],t_evap=274,t_cond=313,vazao_refrigerante=1)