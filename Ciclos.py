

from Equipamentos import *
from CoolProp.CoolProp import PropsSI as Prop

def CicloCompressaoDeVaporComTemperaturas (fluido,t_evap,t_cond, vazao_refrigerante=0,t_superA=0,Nis=1.0,t_sub=0,CF=0):
    
    ciclo = Ciclo(4,fluido)
    try:
        if t_cond<=t_evap or t_cond==t_evap:
            ciclo.erro=True 
            ciclo.errorType= "A temperatura do refrigerante no condensador deve ser superior a temperatura no evaporador" 
            return ciclo         
            
        P_baixa = (Prop('P','T',t_evap,'Q',1,fluido))/1e3
        ciclo.Evapout(1,Pl=P_baixa,Tsa=t_superA,T=t_evap)
        P_alta = (Prop('P','T',t_cond,'Q',0,fluido))/1e3
        ciclo.Compress(2,P_alta,1,Nis=Nis)
        ciclo.CondRef(3,P_alta,'sat')
        ciclo.subResfri(3,t_sub)
        ciclo.VE(4,ciclo.p[1],3)
        mVasao=round(CF/ciclo.ResultadosCf(),2)
        ciclo.SetMass(1,mVasao)
        ciclo.Tub(1,2,3,4)
        ciclo.COP = round(ciclo.ResultadosCop(),2)
        ciclo.FracaoMass(4)
        ciclo.COPcarnot=ciclo.ResultadosCarnot(Te=t_evap,Tc=t_cond)
    except ValueError:
             ciclo.COP=0
    return ciclo

def CicloSimplesComTrocador(fluido,t_evap,t_cond,Nis=1.0,CF=0,t_sub=0,t_superA=0):
    ciclo = Ciclo(4,fluido)
    try:
        if t_cond<=t_evap or t_cond==t_evap:
            ciclo.erro=True 
            ciclo.errorType= "A temperatura do refrigerante no condensador deve ser superior a temperatura no evaporador" 
            return ciclo        
        P_alta = (Prop('P','T',t_cond,'Q',0,fluido))/1e3 
        P_baixa = (Prop('P','T',t_evap,'Q',1,fluido))/1e3
        ciclo.Evapout(1,Pl=P_baixa,Tsa=0,T=t_evap)
        ciclo.superAqueci(1,(t_cond*0.03))
        ciclo.Compress(2,P_alta,1,Nis=Nis)
        ciclo.CondRef(3,P_alta,'sat')
        ciclo.subResfri(3,(t_cond*0.03))
        ciclo.VE(4,ciclo.p[1],3)
        mVasao=round(CF/ciclo.ResultadosCf(),3)
        ciclo.SetMass(1,mVasao)
        ciclo.Tub(1,2,3,4)
        ciclo.COP = round(ciclo.ResultadosCop(),3)
        ciclo.COPcarnot=ciclo.ResultadosCarnot(Te=t_evap,Tc=t_cond)
        ciclo.FracaoMass(4)
    except ValueError:
        ciclo.COP=0
    return ciclo

    
def CicloCascata3Pressoes(fluidoSup,fluidoInf,THcond,THevap,TLcond,TLeva,CapacidadeFrigorifica,TsaHP='sat',TsaLP='sat',NisHP=1.0,NisLP=1.0,TsubH=0.0,TsubL=0.0):
    #Ciclo High Pressure
    cicloHigh = Ciclo(4,fluidoSup)
    if THcond<=THevap or THcond==THevap:
        cicloHigh.erro=True 
        cicloHigh.errorType= "A temperatura do refrigerante no condensador deve ser superior a temperatura no evaporador" 
        return cicloHigh   
    PHevap = (Prop('P','T',THevap,'Q',1,fluidoSup))/1e3
    cicloHigh.Evapout(1,Pl=PHevap,Tsa=TsaHP,T=THevap)
    PHcond = Prop('P','T',THcond,'Q',0,fluidoSup)/1e3
    cicloHigh.Compress(2,PHcond,1,Nis=NisHP)
    cicloHigh.Condout(3,2,PHcond,'sat')
    cicloHigh.subResfri(3,TsubH)
    cicloHigh.VE(4,cicloHigh.p[1],3)
    CfCicloHigh = cicloHigh.ResultadosCf()
    cicloHigh.COP=cicloHigh.ResultadosCop()
    print(cicloHigh.COP)
    #Ciclo Low Pressure
    cicloLow = Ciclo(4,fluidoInf)
    if TLcond<=TLeva or TLcond==TLeva:
        cicloHigh.erro=True 
        cicloHigh.errorType= "A temperatura do refrigerante no condensador deve ser superior a temperatura no evaporador" 
        return cicloHigh
    PLevap = (Prop('P','T',TLeva,'Q',1,fluidoInf))/1e3
    cicloLow.Evapout(1,Pl=PLevap,Tsa=TsaLP,T=TLeva)
    PLcond = Prop('P','T',TLcond,'Q',0,fluidoInf)/1e3
    cicloLow.Compress(2,PLcond,1,Nis=NisLP)
    cicloLow.Condout(3,2,PLcond,'sat')
    cicloLow.subResfri(3,TsubL)
    cicloLow.VE(4,cicloLow.p[1],3)
    cicloLow.COP=cicloLow.ResultadosCop()
    print(cicloLow.COP)

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
    WbTotal= TrabaloCompressorHigh + TrabalhoNoCompressorLow    
    COP = round(CapacidadeFrigorifica/WbTotal,2)
    cicloHigh.COP=COP
    cicloHigh.CriaTabelaCascata(cicloLow=cicloLow)
    return cicloHigh
    
    
def CicloDuplaCompressaoComFlash(fluido,Tc,Te,Pint,CF,Nis=1.0,Tsub=0,Tsa=0):
    #Criando Ciclo
    ciclo = Ciclo(9,fluido)    
    Tev = Te +273.15
    Tcond = Tc + 273.15
    #Calculando Pe 
    Pe = Prop('P','T',Tev,'Q',1,fluido)/1e3
    #Calculando Pc
    Pc = Prop('P','T',Tcond,'Q',0,fluido)/1e3
    #Verificação
    if Tc<=Te or Tc==Te:
        ciclo.erro=True 
        ciclo.errorType= "A temperatura do refrigerante no condensador deve ser superior a temperatura no evaporador" 
        return ciclo
    if Pint<=Pe or Pint>=Pc:
        ciclo.COP=0
        ciclo.erro=True 
        ciclo.errorType= f"A pressão intermediária do fluido {ciclo.fluid} nessas condições deve ser superior a {Pe}kPa e inferior a {Pc}kPa" 
        return ciclo
    #Definindo pontos 1 e 2 
    ciclo.Evapout(1,Pe,Tsa=Tsa)
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
    ciclo.FracaoMass(8)
    return ciclo
    


def CicloComFlashCaso2(fluido,Tc,Te,Pint,CF,Nis=1.0,Tsub=0,Tsa=0):
    ciclo = Ciclo(8,fluid=fluido)
    
    Tev = Te +273.15
    Tcond = Tc + 273.15
    try:             
        #Calculando Pe 
        Pe = Prop('P','T',Tev,'Q',1,fluido)/1e3
        #Calculando Pc
        Pc = Prop('P','T',Tcond,'Q',0,fluido)/1e3
        
        if Tc<=Te or Tc==Te:
                ciclo.COP=0
                ciclo.erro=True 
                ciclo.errorType= "A temperatura do refrigerante no condensador deve ser superior a temperatura no evaporador" 
                return ciclo 
        if Pint<=Pe or Pint>=Pc:
                ciclo.COP=0
                ciclo.erro=True 
                ciclo.errorType= f"A pressão intermediária do fluido {ciclo.fluid} nessas condições deve ser superior a {round(Pe,2)}kPa e inferior a {round(Pc,2)}kPa" 
                return ciclo
        #Ponto 1 e 2 
        ciclo.Evapout(1,Pe,Tsa)
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
        Ql = ciclo.h[1]-ciclo.h[8]
        M1 =round(CF/Ql,3)
        ciclo.m[1]=M1
        BalancoEnergia = round((ciclo.h[2]-ciclo.h[7])/(ciclo.h[6]-ciclo.h[3]),2)
        M3 = round(M1*BalancoEnergia,2)*-1
        Wcb = round(M1*(ciclo.h[2]-ciclo.h[1]),2)
        Wca = round(M3*(ciclo.h[4]-ciclo.h[3]),2)
        Wtotal = Wca + Wcb
        COP = round(CF/Wtotal,2)
        ciclo.COP = COP
        ciclo.COPcarnot=ciclo.ResultadosCarnot(Te=Tev,Tc=Tcond)
        ciclo.FracaoMass(8)
    except ValueError:
        ciclo.COP = 0
    
    return ciclo
    
    
    

def RefrigeranteMaisEficienteCicloSimples(refrigerantes,t_evap,t_cond,Function=CicloCompressaoDeVaporComTemperaturas,CF=1,t_superA=0,Nis=1.0,t_sub=0):
    copCicloHighest = 0
    cicloHighest=Ciclo(4,refrigerantes[0])
    cicloHighest.COP=0
    for fluido in refrigerantes:
        try:
            ciclo = Function(fluido=fluido,t_evap=t_evap,t_cond=t_cond,t_sub=t_sub,t_superA=t_superA,Nis=Nis,CF=CF)
            print(f'Refrigerante: {ciclo.fluid} - COP: {ciclo.COP}')
        except :
            ciclo = Ciclo(4,refrigerantes[0])
            ciclo.COP=0                         
        if(ciclo.COP >= copCicloHighest):
            copCicloHighest=ciclo.COP
            cicloHighest=ciclo
        if(cicloHighest.COP ==0 and cicloHighest.erro !=True):
            cicloHighest.erro=True
            cicloHighest.errorType= 'Nenhum dos refrigerantes selecionados podem ser utilizados nessas condições'   
       
    return cicloHighest
    

def RefrigeranteMaisEficienteCiclosFlash(refrigerantes,Te,Tc,Pint,CF,Function=CicloComFlashCaso2,Tsa=0,Nis=1.0,Tsub=0):
    copCicloHighest = 0
    cicloHighest=Ciclo(4,refrigerantes[0])
    cicloHighest.COP=0
    for fluido in refrigerantes:
        try:
            ciclo = Function(fluido=fluido,Pint=Pint,Tc=Tc,Te=Te,CF=CF,Tsub=Tsub,Tsa=Tsa,Nis=Nis)
            print(f'Refrigerante: {ciclo.fluid} - COP: {ciclo.COP}')
        except :
            ciclo = Ciclo(4,refrigerantes[0])
            ciclo.COP=0
        if(ciclo.COP >= copCicloHighest):
            copCicloHighest=ciclo.COP
            cicloHighest=ciclo           
    if(cicloHighest.COP ==0 and cicloHighest.erro !=True):
        cicloHighest.erro=True
        cicloHighest.errorType= 'Nenhum dos refrigerantes selecionados podem ser utilizados nessas condições'    
    
    return cicloHighest
