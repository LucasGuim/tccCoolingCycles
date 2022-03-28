from Equipamentos_MkII import *
from CoolProp.CoolProp import PropsSI as Prop
from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference, 
    Series
)
import os

precisao = 0.9999

def CicloCompressaoDeVapor_1Estagio (fluido, efetividade_cond, efetividade_evap, eficiencia_is,
                                     t_amb, t_ref, v_ar_cond, v_ar_evap, capacidade_f = 0, trabalho_c = 0,
                                     t_sa = 0, t_sr = 0):
    '''
        Descricao:
            Calcula o cop do ciclo a partir da potencia frigorifica ou do trabalho do compressor
            Temperatura de sub-resfriamento e superaquecimento é opcional

        Parametros:
            fluido: Fluido refrigerante
            efetividade_cond: Efetividade do condensador
            efetividade_evap: Efetividade do evaporador
            eficiencia_is: Eficiencia isentropica do compressor
            t_amb: Temperatura do ambiente externo [K]
            t_ref: Temperatura do ambiente refrigerado [K]
            v_ar_cond: Vasao massica de ar no condensador [kg/s]
            v_ar_evap: Vasao massica de ar no evaporador [kg/s]
            capacidade_f: Capaciadade frigorifica [kW]
            trabalho_c: Trabalho compressor [kW]
            t_sa: Temperatura de superaquecimento [K]
            t_sr: Temperatura de sub resfriamento [K]

        Observacao:
            Para a efetividade do condensador e evaporador, eh considerado a temperatura de saturacao como
        a temperatura de entrada do fluido no trocador
            O programa funciona a partir de iteracoes, eh chutado um valor inicial para a temperatura de 
        condensacao, define-se todos os pontos do ciclo e ao fim a convergencia eh analisada comparando o
        quanto de calor rejeitado ao ambiente e retirado do refrigerante, para a coerencia do sistema buscamos
        a igualdade entre essas duas grandezas
    '''

    # Calculo a partir da capacidade frigorifica
    if capacidade_f == 0 and trabalho_c == 0:
        print('Voce precisa informar a capacidade frigorifica ou o trabalho do compressor')
               
    if capacidade_f != 0:
        ciclo = Ciclo(4, fluido)
    
        # achamos a temperatura do evaporador a partir da capacidade frigorifica, da evetividade do evaporador e
        # da temperatura do ambiente refrigerado
        Tevap = ciclo.evapRefEfetividade(1, efetividade_evap, t_ref, t_sa, v_ar_evap, capacidade_f)

        # inicio da funcao de iteracao que ira encontrar o valor de Th
        erro = 1
        Testimada = t_amb + (t_ref - Tevap) # chute inicial - valor de T3 igual a Tamb mais a
                                            # diferenca de temperaturas entrado no evaporador
        Tmax = Testimada
        Tmin = t_amb
        iteracao = 0

        while erro > (1-precisao):
            iteracao += 1

            # define a pressao alta
            pressaoH = Prop("P", "T", Testimada, "Q", 0, fluido)/1e3
            # limpa a saida do compressor da iteracao anterior
            ciclo.h[2] = '-'
            # define o ponto 2
            ciclo.Compress(2, pressaoH, j=1, Nis=eficiencia_is)                                  
            # define o ponto 3 e calcula a vasao massica
            ciclo.CondRefEfetividade(3, t_amb, Testimada-t_amb, t_sr, efetividade_cond, v_ar_cond, 2)
            # define o ponto 4
            ciclo.VE(4, ciclo.p[1], 3)

            # agora podemos calcular a capacidade frigorifica estimada
            Qestimada = ciclo.calculoEvapRefrigeracaoEfetividade(1, 4)
            erro = (Qestimada - capacidade_f)/capacidade_f

            if erro > 0: #se o valor estimado de CF for maior que o valor real devemos pegar uma temperatura menor
                Tmax = Testimada
                Testimada = (Tmax + Tmin) / 2.0
            else:
                if iteracao == 1: #caso o chute inicial seja menor do que o Treal
                    Tmin = Testimada
                    Testimada = (Tmax-t_amb)*2+t_amb
                else:
                    Tmin = Testimada
                    Testimada = (Tmax + Tmin) / 2.0

            if erro < 0:
                erro = erro * (-1)
        return ciclo, erro
    
    # Calculo a partir do trabalho do compressor
    elif trabalho_c != 0:
        ciclo = Ciclo(4, fluido)
        Th_estimada = t_amb + 5 #chute inicial para a temperatura do refrigerante no condensador
        iteracao = 1
        erro = 1

        Tmax = Th_estimada
        Tmin = t_amb

        
        while erro > (1-precisao):
            QcondExterna = v_ar_cond * Cp_ar * (Th_estimada - t_amb) * efetividade_cond
            Qevap = QcondExterna - trabalho_c
            Tl_estimada = t_ref - Qevap / (v_ar_evap * Cp_ar * efetividade_evap)

            # ponto 1
            if t_sa != 0:
                ciclo.T[1] = Tl_estimada + t_sa
                ciclo.p[1] = Prop('P', 'T', Tl_estimada, 'Q', 1, ciclo.fluid)/1e3
                ciclo.s[1] = Prop('S', 'T', ciclo.T[1], 'P', ciclo.p[1]*1e3, ciclo.fluid)/1e3
                ciclo.h[1] = Prop('H', 'T', ciclo.T[1], 'P', ciclo.p[1]*1e3, ciclo.fluid)/1e3
            else:
                ciclo.T[1] = Tl_estimada
                ciclo.p[1] = Prop('P', 'T', ciclo.T[1], 'Q', 1, ciclo.fluid)/1e3
                ciclo.s[1] = Prop('S', 'T', ciclo.T[1], 'Q', 1, ciclo.fluid)/1e3
                ciclo.h[1] = Prop('H', 'T', ciclo.T[1], 'Q', 1, ciclo.fluid)/1e3

            # ponto 3
            if t_sr != 0:
                ciclo.T[3] = Th_estimada - t_sr
                ciclo.p[3] = Prop('P', "T", Th_estimada, "Q", 0, ciclo.fluid)/1e3
                ciclo.s[3] = Prop('S', "T", ciclo.T[3], "P", ciclo.p[3]*1e3, ciclo.fluid)/1e3
                ciclo.h[3] = Prop('H', "T", ciclo.T[3], "P", ciclo.p[3]*1e3, ciclo.fluid)/1e3
            else:
                ciclo.T[3] = Th_estimada
                ciclo.p[3] = Prop('P', "T", ciclo.T[3], "Q", 0, ciclo.fluid)/1e3
                ciclo.s[3] = Prop('S', "T", ciclo.T[3], "Q", 0, ciclo.fluid)/1e3
                ciclo.h[3] = Prop('H', "T", ciclo.T[3], "Q", 0, ciclo.fluid)/1e3

            # ponto 4
            ciclo.VE(4, P=ciclo.p[1])
            
            # limpar ponto h[2] da iteracao anterior
            ciclo.h[2] = '-'

            # ponto 2
            #ciclo.saidaCompressor(2, trabalho_c, eficiencia_is)

            ciclo.Compress(2, ciclo.p[3], j=1, Nis=eficiencia_is)

            # definindo a massa
            m = trabalho_c / (ciclo.h[2] - ciclo.h[1])
            ciclo.SetMass(2, m)
            ciclo.Tub(2, 1, 3, 4)

            QcondInterna = ciclo.CalEsp(3, 2) * ciclo.m[3] * (-1)

            #QevapInterna = ciclo.calculoEvapRefrigeracaoEfetividade(1,4)

            erro = (QcondExterna - QcondInterna) / QcondInterna

            if erro > 0 :
                Tmax = Th_estimada
                Th_estimada = (Tmax + Tmin) / 2
            else:
                Tmin = Th_estimada
                if Tmax == Th_estimada:
                    Th_estimada += 5
                    Tmax = Th_estimada
                else:
                    Th_estimada = (Tmax + Tmin) / 2
            if erro < 0:
                erro = erro * -1
            
            iteracao += 1

        return ciclo, erro


ciclo, erro = CicloCompressaoDeVapor_1Estagio('R410a',0.8,0.8,0.8,300,288,1,1,2.64)
print(ciclo,erro)
ciclo.Exibir("T", 'p', 'h', 'm', 's')
