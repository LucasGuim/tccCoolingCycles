import CoolProp
from CoolProp.Plots import PropertyPlot
from CoolProp.Plots import SimpleCompressionCycle
from CoolProp.CoolProp import PropsSI as Prop

def teste (T):
    P = Prop('P','T',T+273,'Q',1,'R134a')

    print(P)

def testeP (P):
    T= Prop('T','P',P*1e6,'Q',0,'R134a')
    print(T)
testeP(1.2)