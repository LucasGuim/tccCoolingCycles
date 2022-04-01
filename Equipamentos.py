

from CoolProp.CoolProp import PropsSI as Prop

'''
Funcao Prop usada para ter as propriedades do fluido
    Prop(PropriedadeRetornada, arg1, ValorArg1, arg2, ValorArg2, fluido)
    P = Pa
    H = J/kg
    
Codigos para argumentos
    P pressao (pode usar 'sat' para a pressao de saturacao)
    T temperatura (pode usar 'sat' para temperatura de saturacao)
    Q título 
    H entalpia por unidade de massa
    S entropia por unidade de massa
    D densidade massica
'''

from sympy import symbols, Eq, solve
class Ciclo:
    def __init__(self,n,fluid): # n = numeros de pontos de controle (ou de equipamentos)
        self.fluid=fluid
        self.n = n      # ? nao usado
        self.p=['Pressao (kPa):']+["-"]*n
        self.h=['Entalpia (kJ/kg):']+["-"]*n
        self.s=['Entropia (kJ/kgK):']+["-"]*n
        self.T=['Temperatura (K):']+["-"]*n
        self.x=['Titulo:']+["-"]*n
        self.y=['Fracao massica']+["-"]*n
        self.m=['Vazão mássica']+["-"]*n
        self.wc=['Trabalho do compressor']+["-"]*n
       
        
       
    # Evaporador
    def Evapout(self,i,Pl='sat',Tsa ='sat', T = 0):
        # Pl pressao low kPa | Tsa temperatura se super aquecimento
        if Pl == 'sat':
            self.p[i] = Prop('P','T',T,'Q',1,self.fluid)/1e3 # não temos o T passado no Prop, eh necessario pedir na funcao
            Pl = self.p[i]
            self.h[i] = Prop('H','P',Pl*1e3,'Q',1,self.fluid)/1e3
            self.s[i] = Prop('S','P',Pl*1e3,'Q',1,self.fluid)/1e3
        else:        
            if Tsa == 'sat':
                self.T[i] = Prop('T','P',Pl*1e3,'Q',1,self.fluid)
                self.h[i] = Prop('H','P',Pl*1e3,'Q',1,self.fluid)/1e3
                self.s[i] = Prop('S','P',Pl*1e3,'Q',1,self.fluid)/1e3
            else:
                self.T[i] = Prop('T','P',Pl*1e3,'Q',1,self.fluid) + Tsa
                self.h[i] = Prop('H','P',Pl*1e3,'T',self.T[i],self.fluid)/1e3
                self.s[i] = Prop('S','P',Pl*1e3,'T',self.T[i],self.fluid)/1e3
        if i == 1:
            self.p[i] = self.p[i-2] = Pl
            if self.h[i-2] != '-':
                self.q[i] = self.h[i] - self.h[i-2]
        else:
            self.p[i-1] = self.p[i] = Pl
            if self.h[i-1] != '-':
                self.q[i] = self.h[i]-self.h[i-1]
    #Condensador
    def Condout(self,i,j=0,P='sat',T='sat'):
        # P em kPa 
        # i saida 
        # j entrada
        # dados na saida do condensador
        
        k = 0
        self.x[i] = 0
        
        if P == 'sat':
            # salvando pressao igual antes e depois do condensador
            k += 1
            P = Prop('P','T',T,'Q',0,self.fluid)/1e3
            if j == 0:
                if i == 1:
                    self.p[i] = self.p[i-2] = P
                else:
                    self.p[i] = self.p[i-1] = P
            else:
                self.p[i] = self.p[j] = P
        else:
            if j == 0:
                if i == 1:
                    self.p[i] = self.p[i-2] = P
                else:
                    self.p[i] = self.p[i-1] = P
            else:
                self.p[i] = self.p[j] = P
                
        if T == 'sat':
            # definindo temperatura de saturacao em numeros
            k += 1
            T = Prop('T','P',P*1e3,'Q',0,self.fluid)
            if j ==0:
                if i == 1:
                    self.p[i-2] = self.p[i] = P
                else:
                    self.p[i-1] = self.p[i] = P
            else:
                self.p[j] = self.p[i]            
                
        if k != 0: # saida na condicao de saturacao
            self.h[i] = Prop('H','P',P*1e3,'Q',0,self.fluid)/1e3
            self.s[i] = Prop('S','P',P*1e3,'Q',0,self.fluid)/1e3
            self.T[i] = Prop('T','P',P*1e3,'Q',0,self.fluid)
        else:      # saida nao determinada previamente
            self.h[i] = Prop('H','P',P*1e3,'T',T,self.fluid)/1e3
            self.s[i] = Prop('S','P',P*1e3,'T',T,self.fluid)/1e3
            self.T[i] = T

    def Bomba(self,i,Pm = 0,Pj = 0,Tm=0):
        # i saida | Pm pressao saida | Pj pressao entrada | Tm Temperatura entrada
        self.equip[i] = 'Bomba'
        if Pm == 0:
            Pm = self.p[i]
        else:
            self.p[i] = Pm
            
        if Pj == 0:
            if i == 1:
                Pj = self.p[i-2]
            else:
                Pj = self.p[i-1]
                
        if Tm == 0: # considera liquido saturado
            vj = Prop('D','P',Pj*1e3,'Q',0,self.fluid)**-1
            vm = Prop('D','P',Pm*1e3,'Q',0,self.fluid)**-1
            v = (vj+vm)/2 # media do volume especifico (para liquido saturado a diferenca 
                          # entre os volumes especificos sera muito pequena)
            wb = round(v*(Pm-Pj),2)
            self.wb[i] = wb
            
            if i == 1:
                self.h[i-2] = Prop('H','P',Pj*1e3,'Q',0,self.fluid)/1e3
                self.h[i] = self.h[i-2] + wb
                self.y[i] = self.y[i-2]
            else:
                self.h[i-1] = Prop('H','P',Pj*1e3,'Q',0,self.fluid)/1e3
                self.h[i] = self.h[i-1] + wb
                self.y[i] = self.y[i-1]

        else: # caso T seja passado
            self.h[i] = Prop('H','P',Pm*1e3,'T',Tm,self.fluid)/1e3
            self.T[i] = Tm
            if i == 1:
                wb = self.h[i]-self.h[i-2]
            else:
                wb = self.h[i]-self.h[i-1]
            self.wb[i] = wb
        return wb

    

    # Trabalho das bombas do ciclo
    def TrabB(self):
        self.Wb = 0
        for i in self.wb:
            if self.y[i] == '-':
                if i == 1:
                    self.y[i] = self.y[i-2]
                else:
                    self.y[i] = self.y[i-1]
            self.Wb += self.wb[i]*self.y[i]
        return self.Wb
  

    # Valvula de expansao
    def VE(self,i,P=None,j=0):
        if P != None:
            self.p[i] = P
        if j == 0:
            if i == 1:
                j = i - 2
            else:
                j = i - 1
        self.h[i] = self.h[j]
        self.y[i] = self.y[j]
        self.s[i] = Prop('S','H',self.h[i]*1e3,'P',self.p[i]*1e3,self.fluid)/1e3
        self.T[i] = Prop('T','H',self.h[i]*1e3,'P',self.p[i]*1e3,self.fluid)
        self.x[i] = Prop('Q','H',self.h[i]*1e3,'P',self.p[i]*1e3,self.fluid)

    def ASi(self,m,ti,to,r=0):
        # igualando pressao do duto para caldeira
        if m == 1:
            if self.p[m] == '-':
                self.p[m] = self.p[m-2]
            else:
                self.p[m-2] = self.p[m]
        else:
            if self.p[m] == '-':
                self.p[m] = self.p[m-1]
            else:
                self.p[m-1] = self.p[m]
        # Supondo estado saturação na saida do trocador (após turbina)
        self.p[to] = self.p[ti]
        self.h[to] = Prop('H','P',self.p[to]*1e3,'Q',0,self.fluid)/1e3
        self.T[to] = Prop('T','P',self.p[to]*1e3,'Q',0,self.fluid)
        # Supondo as temperaturas de saida iguais
        self.T[m] = self.T[to]
        self.h[m] = Prop('H','P',self.p[m]*1e3,'T',self.T[m],self.fluid)/1e3

    def ASTI(self,m,ti,to,r=0,j=0):
        # igualando pressao do duto para caldeira
        if j == 0:
            if m == 1:
                if self.p[m] == '-':
                    self.p[m-2] = self.p[m]
                else:
                    self.p[m] = self.p[m-2]
            else:
                if self.p[m] == '-':
                    self.p[m] = self.p[m-1]
                else:
                    self.p[m-1] = self.p[m]
        else:
            if self.p[m] == '-':
                self.p[m] = self.p[j]
            else:
                self.p[j] = self.p[m]
        # Supondo estado saturação na saida do trocador (após turbina)
        self.p[to] = self.p[ti]
        self.h[to] = Prop('H','P',self.p[to]*1e3,'Q',0,self.fluid)/1e3
        self.T[to] = Prop('T','P',self.p[to]*1e3,'Q',0,self.fluid)
        # Supondo as temperaturas de saida iguais
        self.T[m] = self.T[to]
        self.h[m] = Prop('H','P',self.p[m]*1e3,'T',self.T[m],self.fluid)/1e3
        # Realizando o balanço de energia
        if r == 0:
            if m == 1:
                self.y[ti] = self.y[to] = (self.h[m] - self.h[m-2])/(self.h[ti]-self.h[to])
            else:
                self.y[ti] = self.y[to] = (self.h[m] - self.h[m-1])/(self.h[ti]-self.h[to])
        else:
            if m == 1:
                self.y[ti] = ((self.h[to]-self.h[r])*self.y[r] + self.h[m] - self.h[m-2])/(self.h[ti]-self.h[to])
            else:
                self.y[ti] = ((self.h[to]-self.h[r])*self.y[r] + self.h[m] - self.h[m-1])/(self.h[ti]-self.h[to])

    

    # Condensador refrigeracao
    def CondRef(self,i,Ph,Tsr='sat', eficiencia = 1, Tamb=0, VasaoTamb=0):
    
        # Ph pressao high | Tsr temperatura de sub resfriamento
        self.p[i] = Ph
        if Tsr == 'sat':
            self.T[i] = Prop('T','P',Ph*1e3,'Q',0,self.fluid)
            self.h[i] = Prop('H','P',Ph*1e3,'Q',0,self.fluid)/1e3
            self.s[i] = Prop('S','P',Ph*1e3,'Q',0,self.fluid)/1e3
        else:
            self.T[i] = Prop('T','P',Ph*1e3,'Q',0,self.fluid) - Tsr
            self.h[i] = Prop('H','P',Ph*1e3,'T',self.T[i],self.fluid)/1e3
            self.s[i] = Prop('S','P',Ph*1e3,'T',self.T[i],self.fluid)/1e3
        
        
        if i == 1:
            self.p[i-2] = Ph
            if self.h[i-2] != '-':
                self.q[i] = self.h[i] - self.h[i-2]
        else:
            self.p[i-1] = Ph
            if self.h[i-1] != '-':
                self.q[i] = self.h[i]-self.h[i-1]
            
    # Compressor
    def Compress(self,i,P,j=0,Nis=1):
        # P em Kpa
        # Nis eficiencia isentropica
        
            self.p[i] = P
            if self.h[i] == '-':  # usa a eficiencia isentropica
                
                if j == 0:
                    if i == 1:
                        self.s[i] = self.s[i-2]
                        self.h[i] = Prop('H','S',self.s[i]*1e3,'P',self.p[i]*1e3,self.fluid)/1e3
                        wci = self.h[i] - self.h[i-2]
                        self.wc[i] = wci/Nis
                        self.h[i] = self.h[i-2] + self.wc[i]
                        self.s[i] = Prop('S','H',self.h[i]*1e3,'P',self.p[i]*1e3,self.fluid)/1e3
                        self.T[i] = Prop('T','H',self.h[i]*1e3,'P',self.p[i]*1e3,self.fluid)
                    else:
                        self.s[i] = self.s[i-1]
                        wci = self.h[i] - self.h[i-1]
                        self.wc[i] = wci/Nis
                        self.h[i] = self.h[i-1] + self.wc[i]
                        self.s[i] = Prop('S','H',self.h[i]*1e3,'P',self.p[i]*1e3,self.fluid)/1e3
                        self.T[i] = Prop('T','H',self.h[i]*1e3,'P',self.p[i]*1e3,self.fluid)
                else:
                        self.s[i] = self.s[j]
                        self.h[i] = Prop('H','S',self.s[i]*1e3,'P',self.p[i]*1e3,self.fluid)/1e3
                        self.wc[i] = (self.h[i] - self.h[j])/Nis
                        self.h[i] = self.h[j] + self.wc[i]
                        self.s[i] = Prop('S','H',self.h[i]*1e3,'P',self.p[i]*1e3,self.fluid)/1e3
                        self.T[i] = Prop('T','H',self.h[i]*1e3,'P',self.p[i]*1e3,self.fluid)
                        
            else:  # calcula a eficiencia isentropica
                if j == 0:
                    if i == 1:
                        si = self.s[i-2]
                        hi = Prop('H','S',si*1e3,'P',self.p[i]*1e3,self.fluid)/1e3
                        wci = hi - self.h[i-2]
                        self.wc[i] = self.h[i] - self.h[i-2]
                        self.n[i] = wci/self.wc[i]
                    else:
                        si = self.s[i-1]
                        hi = Prop('H','S',si*1e3,'P',self.p[i]*1e3,self.fluid)/1e3
                        wci = hi - self.h[i-1]
                        self.wc[i] = self.h[i] - self.h[i-1]
                        self.n[i] = wci/self.wc[i]
                else:
                        si = self.s[j]
                        hi = Prop('H','S',si*1e3,'P',self.p[i]*1e3,self.fluid)/1e3
                        wci = hi - self.h[j]
                        self.wc[i] = self.h[i] - self.h[j]
                        self.n[i] = wci/self.wc[i]

    def Estado(self,i,P,T):
        self.T[i] = T
        self.p[i] = P
        self.h[i] = Prop('H','P',P*1e3,'T',T,self.fluid)/1e3
        self.s[i] = Prop('S','P',P*1e3,'T',T,self.fluid)/1e3

    # Balanço de energia
    def EnergyB(self,s1,s2,e1,e2):
        if self.y[s1] == '-':   
            self.y[s1] = self.y[e1] = (self.y[s2]*(self.h[s2]-self.h[e2]))/(self.h[e1]-self.h[s1])
            if self.y[s1] > 1 or self.y[s1] < 0:
                raise ValueError
        else:
            self.y[s2] = self.y[e2] = (self.y[s1]*(self.h[s1]-self.h[e1]))/(self.h[e2]-self.h[s2])
            if self.y[s2] > 1 or self.y[s2] < 0:
                raise ValueError

    def fluxsep(self,*kargs):
        # kargs recebe as posicoes
        # funcao define a fracao massica de fluxo em algum equipamento que divida o fluxo
        k = 0
        sf = 0
        for i in kargs:
            if self.y[i] != '-':
                sf += self.y[i]
                k += 1
        if k != len(kargs)-1:
            print('Vazoes insuficientes para calculo')
        for i in kargs:
            if self.y[i] == '-':
                self.y[i] = 1 - sf
    def CameraMistura(self,i,l,Vflash):
        # i estado de saida, l entrada vinda do primero compressor e Vflash é o fluxo vindo da camera de flash 
        fracMass = self.x[Vflash-3]
        self.h[i] = fracMass*self.h[Vflash] + (1-fracMass)*self.h[l]
        self.p[i] = self.p[l]
        self.s[i] = Prop('S','P',self.p[i]*1e3,'H',self.h[i]*1e3,self.fluid)
        return 
    def Tflash(self,l,v,*entrada,P=0):
        #entrada são uma tupla de pontos de entrada
        #l e v são os pontos de saida liquido e vapor 
        # CASO O PARAMETRO P NAO SEJA PASSADO, HAVERA UMA VERIFICAÇÃO
        # PARA IDENTIFICAR SE ALGUM DOS PONTOS POSSUI UMA PRESSÃO DEFINIDA
        # IGUALANDO-A PARA TODOS OS PONTOS DO TFLASH
        
        if P == 0:
            if self.p[l] != '-':
                ptf = self.p[l]
                for i in entrada:
                    self.p[i] = ptf
                self.p[v] = ptf
                P = ptf
            elif self.p[v] != '-':  
                ptf = self.p[v]
                for i in entrada:
                    self.p[i] = ptf
                self.p[l] = ptf
                P = ptf
            else:
                ptf = '-'
                for k in entrada:
                    if self.p[k] != '-':
                        ptf = self.p[k]
                for i in entrada:
                    self.p[i] = ptf
                self.p[v] = ptf
                self.p[l] = ptf
                P = ptf
        else:
            for k in entrada:
                
                self.p[k] = P
            self.p[l] = P
            self.p[v] = P
        # CALCULANDO OS ESTADOS DE SAIDA SATURADOS
        self.h[l]=Prop('H','P',P*1e3,'Q',0,self.fluid)/1e3
        self.h[v]=Prop('H','P',P*1e3,'Q',1,self.fluid)/1e3
        self.s[l]=Prop('S','P',P*1e3,'Q',0,self.fluid)/1e3
        self.s[v]=Prop('S','P',P*1e3,'Q',1,self.fluid)/1e3
        
        
        ## ANALISANDO QTDE DE VARIAVEIS ##
        if len(entrada) == 1:
            for i in entrada:
                self.y[l] = (self.h[i] - self.h[v])/(self.h[l]-self.h[v])
                self.y[v] = 1 - self.y[l]
                self.y[i] = 1
                if self.m[l] != '-':
                    self.m[i] = self.m[l]/self.y[l]
                    self.m[v] = self.m[i] - self.m[l]
                elif self.m[i] != '-':
                    self.m[l] = self.y[l]*self.m[i]
                    self.m[v] = self.y[v]*self.m[i]
                elif self.m[v] != '-':
                    self.m[i] = self.m[v]/self.y[v]
                    self.m[l] = self.m[i] - self.m[v]
        else:
            if self.m[l] == '-':
                if self.m[v] == '-':
                    self.m[v] = (self.h[entrada[0]]*self.m[entrada[0]] + self.h[entrada[1]]*self.m[entrada[1]] - self.h[l]*(self.m[entrada[0]]+self.m[entrada[1]]))/(self.h[v]-self.h[l])
                    self.m[l] = self.m[entrada[0]] + self.m[entrada[1]] - self.m[v]
                if self.m[entrada[0]] == '-':
                    self.m[entrada[0]] = (self.h[v]*self.m[v] - self.h[entrada[1]]*self.m[entrada[1]] + self.h[l]*(self.m[entrada[1]]-self.m[v]))/(self.h[entrada[0]]-self.h[l])
                    self.m[l] = self.m[entrada[0]] + self.m[entrada[1]] - self.m[v]
                if self.m[entrada[1]] == '-':
                    self.m[entrada[1]] = (self.h[v]*self.m[v] - self.h[entrada[0]]*self.m[entrada[0]] + self.h[l]*(self.m[entrada[0]]-self.m[v]))/(self.h[entrada[1]]-self.h[l])
                    self.m[l] = self.m[entrada[0]] + self.m[entrada[1]] - self.m[v]
            if self.m[v] == '-':
                if self.m[entrada[0]] == '-':
                    self.m[entrada[0]] = (self.h[l]*self.m[l] - self.h[entrada[1]]*self.m[entrada[1]] + self.h[v]*(self.m[entrada[1]]-self.m[l]))/(self.h[entrada[0]]-self.h[v])
                    self.m[v] = self.m[entrada[0]] + self.m[entrada[1]] - self.m[l]
                if self.m[entrada[1]] == '-':
                    self.m[entrada[1]] = (self.h[l]*self.m[l] - self.h[entrada[0]]*self.m[entrada[0]] + self.h[v]*(self.m[entrada[0]]-self.m[l]))/(self.h[entrada[1]]-self.h[v])
                    self.m[v] = self.m[entrada[0]] + self.m[entrada[1]] - self.m[l]

    def SetMass(self,i,m):
        self.m[i] = m

    def Tub(self,*kargs):
    # Recebe todos os pontos da tubulacao para definir a fracao massica e vasao massica
        for i in kargs:
            if self.y[i] != '-':
                ft = self.y[i]
                for i in kargs:
                    self.y[i] = ft 
            if self.m[i] != '-':
                mf = self.m[i]
                for i in kargs:
                    self.m[i] = mf

    def Exibir(self,*kargs):
        # argumentos: h, p, s, T, x 
        pontos = ['Pontos analisados - ']
        for i in range(1,len(self.h)):

                pontos.append(f' {i} -')
        print(pontos)
        for j in kargs:          
               
            if j == 'h':
                hp=['Entalpia (kJ/kg):']
                for i in range(1,len(self.h)):
                    if self.h[i] == '-':
                        hp.append('-')
                    else:
                        hp.append(round(self.h[i],2))
                print(hp)
            if j == 'p':
                pp=['Pressao (kPa):']
                for i in range(1,len(self.p)):
                    if type(self.p[i]) == str:
                        pp.append(self.p[i])
                    else:
                        pp.append(round(self.p[i],2))
                print(pp)
            if j == 's':
                sp = ['Entropia (kJ/kgK)']
                for i in range(1,len(self.s)):
                    if type(self.s[i]) == str:
                        sp.append(self.s[i])
                    else:
                        sp.append(round(self.s[i],3))
                print(sp)        
            if j == 'T':
                Tp =['Temperatura (K):']
                for i in range(1,len(self.T)):
                    if self.T[i] == '-':
                        Tp.append('-')
                    else:
                        Tp.append(round(self.T[i],2))
                print(Tp)
            if j == 'x':
                xp = ['Titulo']
                for i in range(1,len(self.x)):
                    if self.x[i] == '-':
                        xp.append('-')
                    else:
                        xp.append(round(self.x[i],3))
                print(xp)
            if j == 'y':
                yp = ['Fracao massica']
                for i in range(1,len(self.y)):
                    if self.y[i] == '-':
                        yp.append('-')
                    else:
                        yp.append(round(self.y[i],2))
                print(yp)
            if j == 'm':
                mp = ['Vazao massica']
                for i in range(1,len(self.m)):
                    if self.m[i] == '-':
                        mp.append('-')
                    else:
                        mp.append(round(self.m[i],10))
                print(mp)
            if j == 'q':
                qp = {}
                for i in self.q:
                    qp[i] = round(self.q[i],2)
                print(qp)
            if j == 'wb':
                wbp = {}
                for i in self.wb:
                    wbp[i] = round(self.wb[i],2)
                print(wbp)
            if j == 'wt':
                wtp = {}
                for i in self.wt:
                    wtp[i] = round(self.wt[i],2)
                print(wtp)
            if j == 'wc':
                wcp = {}
                for i in self.wc:
                    wcp[i] = round(self.wc[i],2)
                print(wcp)

    # Trocador casco e tubo
    def TCT(self,t,c):
    # t tubo e c casco
        mt, mos, mic, hic, his, hos, hot = symbols('mt mos mic hic his hos hot')
        mc = Eq(mic + mt - mos, 0)
        ec = Eq(mt*hot + mos*hos -mt*hic - mic*hic - mt*his, 0)
        dados = [('hos',self.h[c])]
        var = []
        if t == 2:
            dados.append(('hic',self.h[t-1]))
            if self.m[t] == '-':
                var.append('mt')
            else:
                dados.append(('mt',self.m[t]))
            if self.m[t-1] == '-':
                var.append('mic')
            else:
                dados.append(('mic',self.m[t-1]))
            if self.h[t] == '-':
                var.append('hot')
            else:
                dados.append(('hot',self.h[t]))
        elif t == 1:
            dados.append(('hic',self.h[t-2]))
            if self.m[t] == '-':
                var.append('mt')
            else:
                dados.append(('mt',self.m[t]))
            if self.m[t-1] == '-':
                var.append('mic')
            else:
                dados.append(('mic',self.m[t-2]))
            if self.h[t] == '-':
                var.append('hot')
            else:
                dados.append(('hot',self.h[t]))
        else:
            dados.append(('hic',self.h[t-1]))
            if self.m[t] == '-':
                var.append('mt')
            else:
                dados.append(('mt',self.m[t]))
            if self.m[t-1] == '-':
                var.append('mic')
            else:
                dados.append(('mic',self.m[t-1]))
            if self.h[t] == '-':
                var.append('hot')
            else:
                dados.append(('hot',self.h[t]))
        dados.append(('hos',self.h[c]))
        if c == 1:
            if self.h[c-2] == '-':
                var.append('his')
            else:
                dados.append(('his',self.h[c-2]))
        else:
            if self.h[c-1] == '-':
                var.append('his')
            else:
                dados.append(('his',self.h[c-1]))
        if self.m[c] == '-':
            var.append('mos')
        else:
            dados.append(('mos',self.m[c]))
        sol = solve((mc.subs(dados),ec.subs(dados)),var)
        for k in sol:
            if k == mic:
                if t == 1:
                    self.m[t-2] = sol[k]
                else:
                    self.m[t-1] = sol[k]
            if k == mos:
                self.m[c] = sol[k]
            if k == mt:
                self.m[t] = sol[k]
                if t == 2:
                    self.m[t-3] = sol[k]
                else:
                    self.m[t-2] = sol[k]
                if c == 1:
                    self.m[c-2] = sol[k]
                else:
                    self.m[c-1] = sol[k]
        print(sol)

    def COP(self,l):
        trabalho = self.TrabC()
        #print ("%0.5f kW" %trabalho)
        if self.m[l] != '-':
            Cop = self.q[l]*self.m[l]/trabalho
        elif self.y[l] != '-':
            Cop = self.q[l]*self.y[l]/self.TrabC()
        else:
            Cop = self.q[l]/self.TrabC()
        #    print('Calculo do COP realizado supondo unico fluxo')
        #print(f'COP Calculado do ciclo: {round(Cop,4)}')
        return round(Cop,4)

        
    # Condensador de refrigeração com eficiencia
   
    def calculoEvapRefrigeracaoEfetividade(self, i, j = 0):
        '''
        FUNCAO: calcula a capacidade frigorifica do sistema por kg de refrigerante. 
                Requer as propriedades de entrada do evaporador
                definidas (entalpia)
        '''
        if j == 0:
            if i == 1:
                j=i-2
            else:
                j=i=1
        
        self.q[i] = (self.h[i]- self.h[j])
        return self.q[i] * self.m[i]

    
    def ResultadosWc(self):
        trabalhoCompressor = int((self.h[2] - self.h[1]))
        return trabalhoCompressor 
    def ResultadosCf(self):
        Cf = int(self.h[1]-self.h[4])
        return Cf
    

    def ResultadosCop(self):
        trabalhoCompressor = self.h[2] - self.h[1]
        calorUtil = self.h[1] - self.h[4]
        COP = calorUtil/trabalhoCompressor
        return COP