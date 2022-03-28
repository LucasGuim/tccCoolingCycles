import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot
from CoolProp.Plots import SimpleCompressionCycle
from Equipamentos_MkII import *
from CoolProp.CoolProp import PropsSI as Prop



def CicloCascata3Pressoes(fluidoSup,fluidoInf,THcond,THevap,TLcond,TLeva,CapacidadeFrigorifica,t_superA='sat'):
    #Ciclo High Pressure
    cicloHigh = Ciclo(4,fluidoSup)
    cicloHigh.Evapout(1,Pl='sat',Tsa=0,T=THevap)
    PHcond = Prop('P','T',THcond,'Q',0,fluidoSup)/1e3
    cicloHigh.Compress(2,PHcond,1,1)
    cicloHigh.Condout(3,2,PHcond,'sat')
    cicloHigh.VE(4,cicloHigh.p[1],3)
    
    CfCicloHigh = cicloHigh.ResultadosCf()
    #Ciclo Low Pressure
    cicloLow = Ciclo(4,fluidoInf)
    cicloLow.Evapout(1,Pl='sat',Tsa=10,T=TLeva)
    PLcond = Prop('P','T',TLcond,'Q',0,fluidoInf)/1e3
    cicloLow.Compress(2,PLcond,1,1)
    cicloLow.Condout(3,2,PLcond,'sat')
    cicloLow.VE(4,cicloLow.p[1],3)

    #Descobrindo as vazões de refrigerante 
    #     
    vazao_refrigeranteLow = CapacidadeFrigorifica/cicloLow.ResultadosCf()
    CalorExpelidoCondensadorLow = cicloLow.h[2] - cicloLow.h[3]
    vazao_refrigeranteHigh= (vazao_refrigeranteLow*CalorExpelidoCondensadorLow)/CfCicloHigh 
    #Calculando os trabalhos dos compressores

    WbLow = cicloLow.ResultadosWc()
    WbHigh = cicloHigh.ResultadosWc()

    TrabalhoNoCompressorLow = (cicloLow.ResultadosWc())*vazao_refrigeranteLow    
    TrabaloCompressorHigh = vazao_refrigeranteHigh*WbHigh

    cicloLow.SetMass(1,vazao_refrigeranteLow)
    cicloLow.Tub(1,2,3,4)
    cicloHigh.Exibir('h','p','s','T','x')
    print('ciclo inferior')
    WbTotal= TrabaloCompressorHigh + TrabalhoNoCompressorLow
    
    COP = CapacidadeFrigorifica/WbTotal

    cicloLow.Exibir('h','p','s','T','x')
    print(f'COP do ciclo é: {COP}',f'WTh:{TrabaloCompressorHigh} e WTl: {TrabalhoNoCompressorLow} , vazão Ciclo de baixa: {vazao_refrigeranteLow} ' )
    

CicloCascata3Pressoes('R22','R22',THcond=313,THevap=273,TLcond=273,TLeva=233,CapacidadeFrigorifica=100)

