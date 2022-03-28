#Bibliotecas
from CoolProp.CoolProp import PropsSI as CP
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import get_test_data

#Listas
lista_n = []
Wcomp_total_lista = []
COP_lista = []

#Dados do problema
Pfrig = 120 * 1000 #[W]
T1 = -30 + 273.15 #[K]
T3 = -8 + 273.15 #[K]
T5 = -12 + 273.15 #[K]
T7 = 35 + 273.15 #[K]
fluid_high = 'R12'
fluid_low = 'R22'
drop_suc = 12000 #[Pa]
drop_desc = 0 #[Pa]

#Pressão critíca do fluido superior
P_crit_high = CP('PCRIT', fluid_high)

#Ciclo inferior
P1 = CP('P', 'T', T1, 'Q', 1, fluid_low) 
h1 = CP('H', 'T', T1, 'Q', 1, fluid_low)
ha = h1
Pa = P1 - drop_suc
Ta = CP('T', 'H', ha, 'P', Pa, fluid_low)
Pb = Pa
Tb = Ta + 0
vb = 1 / CP('D', 'T', Tb, 'P', Pb, fluid_low)
P3 = CP('P', 'T', T3, 'Q', 0 , fluid_low)
P2 = P3
Pc = P2 + drop_desc
h3 = CP('H', 'T', T3, 'Q', 0, fluid_low)
h4 = h3
m_flow_low = Pfrig / (h1 - h4)
print('Vazão mássica do ciclo inferior = ' +str (round(m_flow_low, 2)) + ' kg/s')

#Ciclo superior
P5 = CP('P', 'T', T5, 'Q', 1, fluid_high)
h5 = CP('H', 'T', T5, 'Q', 1, fluid_high)
hw = h5
Pw = P5 - drop_suc
Tw = CP('T', 'H', hw, 'P', Pw, fluid_high)
Px = Pw
Tx = Tw + 0 
vx = 1 / CP('D', 'T', Tx, 'P', Px, fluid_high)
P7 = CP('P', 'T', T7, 'Q', 0, fluid_high)
P6 = P7
Py = P6 + drop_desc
h7 = CP('H', 'T', T7, 'Q', 0, fluid_high)
h8 = h7

n_low = 1.169
n_high = 1.081
#Ciclo inferior
vc = (Pb * vb ** n_low / Pc)**(1 / n_low)
hc = CP('H', 'P', Pc, 'D', 1 / vc, fluid_low)
h2 = hc
#Trabalho específico do compressor do ciclo inferior
w_low = n_low / (n_low-1) * Pb * vb * ((Pc/Pb)**((n_low-1)/n_low) - 1)
#Trabalho do compressor do ciclo inferior
Wcomp_low = m_flow_low * w_low
print('Potência consumida no compressor do ciclo inferior = ' + str(round(Wcomp_low/1000, 2)) + ' kW')
#Calor trocado no trocador central
Qcond_low =  m_flow_low * (h2 - h3)
#Ciclo superior
Qevap_high = Qcond_low
m_flow_high = Qevap_high / (h5 - h8)
print('Vazão mássica do ciclo superior = ' + str(round(m_flow_high,2)) + ' kg/s')
#Trabalho específico do compressor do ciclo superior
w_high = n_high / (n_high-1) * Px * vx * ((Py/Px)**((n_high-1)/n_high) - 1)
#Trabalho no compressor do ciclo superior
Wcomp_high = m_flow_high * w_high 
print('Potência consumida no compressor do ciclo superior = ' + str(round(Wcomp_high/1000, 2)) + ' kW')
#Trabalho total do ciclo
Wcomp_total = Wcomp_low + Wcomp_high
Wcomp_total_lista.append(Wcomp_total / 1000)
#COP
COP = Pfrig / Wcomp_total
print('COP = ' + (str(round(COP, 2))))
COP_lista.append(COP)