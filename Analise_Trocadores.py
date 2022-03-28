from CoolProp.CoolProp import PropsSI as Prop

from math import pi as PI
from math import log as ln
from math import exp
from matplotlib.pyplot import text

import numpy as np

# Funcoes de Bessel modificadas (usado apenas para calculo de eficiencia de aletas)
from scipy.special import i0e as I0
from scipy.special import i1e as I1
from scipy.special import k0e as K0
from scipy.special import k1e as K1

g = 9.8 # [m/s]
pressaoATM = 101325 # [PA]
erroAceitavel = 0.05

def compressaoMecanica(fluido, Text, Tref, # Parametros de operacao
                       Lc, DcI, DcE, VasaoArCond, velArC, nPlacasTubosC, kTuboC, areaTotalC, # Parametros do Condensador
                       Le, DeI, DeE, VasaoArEvap, velArE, nPlacasTubosE, kTuboE, areaTotalE, # Parametros do evaporador
                       Li, di, do, Di, k_TI,                                                 # Parametros do trocador intermediario
                       Wc, n_is, Tmin, Tmax,                                                 # Parametros do compressor
                       efSupC = 1, efSupE = 1,                                               # Eficiencia da superficie dos trocadores
                       Patm=pressaoATM                                                       # Parametros opcionais
                       ):
    '''
    Descricao:
        A partir de parametros do aparelho de refrigeracao (compressor, evaporador e condensa-
        dor) e dos ambientes (temperatura externa e temperatura do ambiente refrigerado) cal-
        cula o COP maximo que pode ser obtido.
    
    Parametros:
        fluido: fluido refrigerante
        Text: temperatura do ambiente externo [K]
        Tref: temperatura do ambiente refrigerado [K]
        Lc: comprimento do condensador [m]
        DcI: diametro interno do condensador [m]
        DcE: diametro externo do condensador [m]
        VasaoArCond: vasao de ar no condensador [m**3/s]
        velArC: velocidade do ar no condensador [m/s]
        nPlacasTubosC: numero de placas de tubos paralelos (em relacao a profundidade) do condensador
        kTuboC: Condutividade termica do tubo do condensador [W/m^2/°C]
        areaTotalC: Superficie externa total de troca termica do condensador [m2]
        Le: comprimento do evaporador[m]
        DeI: diametro interno do evaporador [m]
        DeE: diametro externo do evaporador [m]
        VasaoArEvap: vasao de ar no evaporador [m**3/s]
        velArE: velocidade do ar no evaporador [m/s]
        nPlacasTubosE: numero de placas de tubos paralelos (em relacao a profundidade) do evaporador
        kTuboE: Condutividade termica do tubo do evaporador [W/m^2/°C]
        areaTotalE: Superficie externa total de troca termica do evaporador [m2]
        Li: Comprimento do trocador intermediario [m]
        di: Diametro interno do tubo interno [m]
        do: Diametro externo do tudo interno [m]
        Di: Diametro interno do tubo externo [m]
        k_TI: Condutividade termica do tubo do trocador intermediario [W/m^2/°C]
        Wc: Trabalho do compressor [W]
        n_is: eficiencia isentropica do compressor
        Tmin: Temperatura minima do compressor [K]
        Tmax: Temperatura maxima do compressor [K]
        efSupC: Eficiencia da superficie externa de troca termica do condensador
        efSupE: Eficiencia da superficie externa de troca termica do evaporador
        Patm: pressao atmosferica
    '''
    
    # Nomenclatura utilizada:
    #  IVC: Interno Vapor Condensador
    #  TPC: Two Phase Condensador
    #  ILC: Interno Liquido Condensador
    #  EC:  Externo Condensador
    #  IVE: Interno Vapor Evaporador
    #  TPE: Two Phase Evaporador
    #  ILE: Interno Liquido Evaporador
    #  EE:  Externo Evaporador
        
    # parametros que serao variados: vasao massica (m) e temperatura de evaporacao (Tevap)
    
    vasaoArCondConsiderada = VasaoArCond * nPlacasTubosC
    vasaoArEvapConsiderada = VasaoArEvap * nPlacasTubosE

    PassoT2 = 0.1
    PassoT1 = 0.5
    lastErro = None
    
    Resultado = {}
    
    for Tevap in list(np.arange(Tref-1, Tmin, -1*PassoT1)):
        resultadoT2 = None
        iteracao = 0
        
        for Tcond in list(np.arange(Text+1, Tmax, PassoT2)):
            motivo = ''
            iteracao += 1
            
            ######################################### TROCADOR INTERMEDIARIO #########################################
            
            # ponto 1
            T1 = Tevap
            P6 = P2 = P1 = Prop('P', 'T', T1, 'Q', 1, fluido)
            H2 = H1 = Prop('H', 'T', T1, 'Q', 1, fluido)
            S2 = S1 = Prop('S', 'T', T1, 'Q', 1, fluido)
            
            # ponto 4
            T4 = Tcond
            P5 = P3 = P4 = Prop('P', 'T', T4, 'Q', 0, fluido)
            H4 = Prop('H', 'T', T4, 'Q', 0, fluido)
            S4 = Prop('S', 'T', T4, 'Q', 0, fluido)
            
            # iteracao para encontrar a vasao massica 
            # a partir do trocador intermediario
            erro_m = 1
            H_is = Prop('H', 'P', P3, 'S', S2, fluido)
            H3 = (H_is-H2)/n_is + H2
            m = Wc/(H3-H2)
            
            while erro_m > 0.01:
                viscosidade_dinamica4 = Prop("V", "P", P4, "Q", 0, fluido)  # [Pa.s]
                Re4 = 4*m/(PI*di*viscosidade_dinamica4)
                Pr4 = Prop("PRANDTL", "P", P4, "Q", 0, fluido)
                k4 = Prop("L", "P", P4, "Q", 0, fluido)  # [W/(mK)]
                c_p4 = Prop("C", "P", P4, "Q", 0, fluido) # [J/(kgK)]
                h_tubo = hInterno(Re4, Pr4, k4, di)

                dh_anulo = Di - do
                de_anulo = (Di**2 + do**2)/do
                viscosidade_dinamica1 = Prop("V", "P", P1, "Q", 0, fluido)  # [Pa.s]
                Re1 = 4*m/(PI*dh_anulo*viscosidade_dinamica1)
                Pr1 = Prop("PRANDTL", "P", P1, "Q", 0, fluido)
                k1 = Prop("L", "P", P1, "Q", 0, fluido)  # [W/(mK)]
                c_p1 = Prop("C", "P", P1, "Q", 0, fluido) # [J/(kgK)]
                h_anulo = hInterno(Re1, Pr1, k1, de_anulo)
                
                UA = ( 1/(h_tubo*PI*di*Li) +
                       1/(h_anulo*PI*Di*Li) +
                       ln(do/di)/(2*PI*k_TI*Li)
                       )**(-1)
                
                if c_p4 > c_p1:
                    C_min_TI = m*c_p1
                    Cr = c_p1/c_p4
                else:
                    C_min_TI = m*c_p4
                    Cr = c_p4/c_p1
                
                NUT_TI = UA / C_min_TI
                e_TI = (1 - exp( -NUT_TI*(1-Cr) ))/( 1 - Cr*exp( -NUT_TI*(1-Cr) ) )
                
                q_max_TI = C_min_TI*(T4 - T1)
                q_TI = e_TI*q_max_TI
                
                T2 = q_TI/(m*c_p1) + T1
                H2 = Prop('H', 'T', T2, 'P', P2, fluido)
                S2 = Prop('S', 'T', T2, 'P', P2, fluido)

                T5 = T4 - q_TI/(m*c_p4)
                
                # recalculo de m
                H_is = Prop('H', 'P', P3, 'S', S2, fluido)
                H3 = (H_is-H2)/n_is + H2
                m_new = Wc/(H3-H2)
                erro_m = abs((m - m_new)/m_new)
                m = m_new
            
            T3 = Prop('T', 'P', P3, "H", H3, fluido)
            S3 = Prop('S', 'P', P3, 'H', H3, fluido)
            if T3 == Prop('T', 'P', P3, "Q", 1, fluido): print('falha T3')
            
            H6 = H5 = Prop('H', 'T', T5, 'P', P5, fluido)
            S5 = Prop('S', 'T', T5, 'P', P5, fluido)
            
            T6 = Prop('T', 'P', P6, 'H', H6, fluido)
            S6 = Prop('S', 'P', P6, 'H', H6, fluido)
            
            # Todos os pontos ja estão determinados, falta conferir se a saida 
            # dos trocadores batem com as condicoes assumidas inicialmente
            
            ######################################### CONDENSADOR #########################################
            
            # propriedades do ar do ambiente externo
            viscosidade_dinamicaEC = Prop("V", "P", Patm, "T", Text, "air")
            rhoArEC = Prop("D", "P", Patm, "T", Text, "air")
            PrEC = Prop("PRANDTL", "P", Patm, "T", Text, "air")
            kEC = Prop("L", "P", Patm, "T", Text, "air")
            ReEC = rhoArEC*velArC*DcE/viscosidade_dinamicaEC
            c_pEC = Prop("C", "P", Patm, "T", Text, "air") # [J/(kgK)]
            
            # h externo do condensador
            if ReEC*PrEC >= 0.2:
                hEC = hExterno(ReEC, PrEC, kEC, DcE)
            else:
                print ("valores de Reynolds e/ou Prandtl fora de limites", ReEC, PrEC, 2)
                achou_resultado=False
                break
            
            # propriedades vapor superaquecido no condensador
            try:
                viscosidade_dinamicaIVC = Prop("V", "P", P3, "T", T3, fluido)  # [Pa.s]
                ReIVC = 4*m/(PI*DcI*viscosidade_dinamicaIVC)
                PrIVC = Prop("PRANDTL", "P", P3, "T", T3, fluido)
                kIVC = Prop("L", "P", P3, "T", T3, fluido)  # [W/(mK)]
                c_pIVC = Prop("C", "P", P3, "T", T3, fluido) # [J/(kgK)]
            except ValueError:
                # caso o vapor superaquecido esteja muito proximo do vapor saturado, o CoolPack levanta erro
                # Solucao: usar valores de vapor saturado
                viscosidade_dinamicaIVC = Prop("V", "P", P3, "Q", 1, fluido)  # [Pa.s]
                ReIVC = 4*m/(PI*DcI*viscosidade_dinamicaIVC)
                PrIVC = Prop("PRANDTL", "P", P3, "Q", 1, fluido)
                kIVC = Prop("L", "P", P3, "Q", 1, fluido)  # [W/(mK)]
                c_pIVC = Prop("C", "P", P3, "Q", 1, fluido) # [J/(kgK)]
                
            try:
                hIVC = hInterno(ReIVC, PrIVC, kIVC, DcI)
            except: 
                print ("Valores de Re e Pr fora da faixa aceitavel", ReIVC, PrIVC, 1)
                return Resultado
            
            # coeficiente global (VC vapor condensador)
            U_VC = 1/( 1/hIVC +                                     # resistencia refrigerante
                      (PI*DcI*Lc)*ln(DcE/DcI)/(2*PI*kTuboC*Lc) +    # resistencia parede
                      (PI*DcI*Lc)/(areaTotalC * efSupC * hEC))      # resistencia ar
            A_VC = -ln((Text-Tcond)/(Text-T3)) * m * c_pIVC / U_VC  # area necessaria
            L_VC = A_VC / (PI * DcI) # comprimento necessario
            
            if (Lc - L_VC) <=0: # deve haver comprimento de tubo restante para ocorrer a mudanca de fase
                motivo = 'Comprimento insuficiente para iniciar a condensacao'
                achou_resultado = False
                break
            
            # Propriedades da mudanca de fase
            try:
                h_TPC = hCondensacao(P4, m, DcI, fluido)
            except:
                motivo = 'erro em h_TPC'
                achou_resultado = False
                break
            U_TPC = 1/(1/h_TPC +                                    # resistencia refrigerante
                       (PI*DcI*Lc)*ln(DcE/DcI)/(2*PI*kTuboC*Lc) +   # resistencia parede
                       (PI*DcI*Lc)/(areaTotalC * efSupC * hEC))     # resistencia ar
            
            # efetividade do trocador durante a condensacao
            efet_cond = 1 - exp(- U_TPC * PI*DcI*Lc / (vasaoArCondConsiderada * rhoArEC * c_pEC))
            
            # calor trocado desejado
            h_lSatC = Prop("H", "P", P3, "Q", 0, fluido)
            h_vSatC = Prop("H", "P", P3, "Q", 1, fluido)
            qCondComp = m * (h_vSatC - h_lSatC)  # deseja-se condensar todo o refrigerante
            # comprimento necessario
            L_TPC = qCondComp * Lc / (efet_cond * rhoArEC * c_pEC * (Tcond - Text) * vasaoArCondConsiderada)
            
            if (1-2*erroAceitavel) <= L_TPC/(Lc - L_VC) <= (1+2*erroAceitavel): # saida do condensador como liquido saturado
                erroCond = 1- L_TPC/(Lc - L_VC)
                
            elif L_TPC < (Lc - L_VC): 
                # saida do condensador como liquido subresfriado
                # necessario diminuir a temperatura de condensacao -> proximo Tevap
                break
                    
            else: 
                # saida do condensador como mistura
                # necessario aumentar Tcond, apenas passar para a proxima iteracao
                continue
                
            H6 = H5
            S6 = Prop("S", "P", P6, "H", H6, fluido)
                        
            entalpiaLiquidoSat = Prop("H", "P", P6, "Q", 0, fluido)
            if H6 >= entalpiaLiquidoSat:
                frassao_massica_vapor = Prop("Q", "P", P6, "H", H6, fluido)
            else:
                frassao_massica_vapor = False
                
            ######################################### EVAPORADOR #########################################

            # Propriedades do ar refrigerado
            viscosidade_dinamicaEE = Prop("V", "P", Patm, "T", Tref, "air")
            rhoArEE = Prop("D", "P", Patm, "T", Tref, "air")
            ReEE = rhoArEE*velArE*DeE/viscosidade_dinamicaEE
            PrEE = Prop('PRANDTL', "P", Patm, "T", Tref, "air")
            kEE = Prop("L", "P", Patm, "T", Tref, "air")
            rhoEE = Prop("D", "P", Patm, "T", Tref, "air")
            c_pEE = Prop("C", "P", Patm, "T", Tref, "air")

            if ReEE*PrEE > 0.02:
                hEE = hExterno(ReEE, PrEE, kEE, DeE)
            else:
                print ("Produto Re*Pr fora da faixa de valores aceitaveis", ReEE*PrEE, 4)
                achou_resultado = False
                break

            # Liquido subresfriado (nao ira ocorrer mas o codigo sera
            # mantido no arquivo por ja estar pronto)
            if frassao_massica_vapor == False:
                # ILE Interno Liquido Evaporador
                viscosidade_dinamicaILE = Prop("V", "P", P6, "T", T6, fluido) # [Pa.s]
                ReILE = 4*m/(PI*DeI*viscosidade_dinamicaILE)
                PrILE = Prop("PRANDTL", 'P', P6, 'T', T6, fluido)
                kILE = Prop('L', 'P', P6, 'T', T6, fluido) # [W/(mK)]
                c_pILE = Prop("C", "P", P6, "T", T6, fluido) # [J/kgK]
                hILE = hInterno(ReILE, PrILE, kILE, DeI)
                
                U_LE = 1/((1/hILE + 
                          (PI*DeI*Le)*ln(DeE/DeI)/(2*PI*kTuboE*Le) + 
                          (PI*DeI*Le)/(areaTotalE*efSupE*hEE)))
                AILE = ln((Tref-Tevap)/(Tref-T6)) * m * c_pILE / U_LE # area necessaria
                L_LE = AILE / (2*PI*DeI/2) # comprimento necessario
                if (Le - L_LE) < 0:
                    print ('Líquido subresfriado domina o evaporador')
                    continue
            else:
                L_LE = 0
            
            # mudanca de fase evaporador
            xValores = [] # Lista de valores de x
            n=4
            for indice in range(n):
                x = 1/n/2 + indice * 1/n
                xValores.append(x)
            
            lista_hE = []
            for elem in xValores:
                # propriedades de liquido saturado
                viscosidade_dinamica_liquido_evap = Prop("V", "P", P6, "Q", 0, fluido)
                Re_liq = 4 * m / (PI * DeI * viscosidade_dinamica_liquido_evap)
                Pr_liq = Prop('PRANDTL', "P", P6, "Q", 0, fluido)
                k_liq = Prop('L', "P", P6, "Q", 0, fluido)
                rho_liq = Prop("D", "P", P6, "Q", 0, fluido)
                rho_vap = Prop("D", "P", P6, "Q", 1, fluido)
                sigma = Prop("I", "P", P6, "Q", 0, fluido)
                Ts = Prop("T", "P", P6, "Q", 0, fluido)
                i_lg = Prop("H", "P", P6, "Q", 1, fluido) - Prop("H", "P", P6, "Q", 0, fluido)
                
                lista_hE.append(hEvaporacao(Re_liq, Pr_liq, k_liq, DeI, elem, rho_liq, rho_vap, m, sigma, Ts, hEE, Tref, i_lg))
                
            somaHTP = 0
            for elem in lista_hE:
                somaHTP += elem
            h_TPE = somaHTP/(len(lista_hE))
            U_TPE = 1/(1/h_TPE +                                    # resistencia refrigerante
                       (PI*DeI*Le)*ln(DeE/DeI)/(2*PI*kTuboE*Le) +   # resistencia parede
                       (PI*DeI*Le)/(areaTotalE*efSupE*hEE))         # resistencia ar
            
            efetividade_evap = 1 - exp(- U_TPE * (PI * DeI * Le) / (rhoEE * vasaoArEvapConsiderada * c_pEE))
            
            # quantidade de calor trocado desejado
            if frassao_massica_vapor != False:
                q_desejadoevap = m * (Prop("H", "P", P6, "Q", 1, fluido) - H6)
            else:
                q_desejadoevap = m * (Prop("H", "P", P6, "Q", 1, fluido) - Prop("H", "P", P6, "Q", 0, fluido))
                
            # vasao de ar necessaria para evaporar todo o refrigerante
            L_TPE = q_desejadoevap * Le / (efetividade_evap * rhoEE * c_pEE * (Tref - Prop("T", "P", P6, "Q", 1, fluido)) * vasaoArEvapConsiderada)

            if (1-2*erroAceitavel) <= L_TPE/(Le-L_LE) <= (1+2*erroAceitavel): 
                erroEvap = 1- L_TPE/(Le-L_LE)
            elif L_TPE/(Le-L_LE) < (1-erroAceitavel): break
            else: continue
                
            # Destruicao de exergia
            Ad_comp = Text * (m*(S3-S2))
            Ad_cond = Text * (m*(S4-S3) - m*(H4-H3)/Text)
            Ad_de   = Text * (m*(S6-S5))
            Ad_evap = Text * (m*(S1-S6) - m*(H1-H6)/Tref)
            Ad_troc_int = Text*m*(S5+S2-S4-S1)
            
            dest_exergia = [Ad_comp, Ad_cond, Ad_de, Ad_evap, Ad_troc_int]
            eta_II = 1- sum(dest_exergia)/Wc
            
            COP = (H1-H6)/(H3-H2)
            dicionario = {
                'Fluido': fluido,
                'M': m,
                'T': ('Kelvin', T1, T2, T3, T4, T5, T6),
                'P': ('kPa', P1, P2, P3, P4, P5, P6),
                'H': ('kJ/kg', H1, H2, H3, H4, H5, H6),
                'S': ('kJ/kgK', S1, S2, S3, S4, S5, S6),
                'A': ('kW Evaporador(1) Compressor(2) Condensador(3) DE(4) TI(5)', Ad_evap, Ad_comp, Ad_cond, Ad_de, Ad_troc_int),
                'Destruicao exergia': dest_exergia,
                'COP': COP,
                'CF': (H1-H6)*m,
                'Wc': Wc,
                'hTPe': h_TPE,
                'hTPc': h_TPC,
                'Tcond': Tcond,
                'Tevap': Tevap,
                'efet_cond': efet_cond,
                'efet_evap': efetividade_evap,
                'eta_II': eta_II,
                'erro': (abs(erroCond)+abs(erroEvap))/2
            }
            
            if resultadoT2 == None: resultadoT2 = dicionario
            elif abs(resultadoT2['erro']) > abs(dicionario['erro']): resultadoT2 = dicionario
            else: break
            # Fim For temperatura ponto 1
        # Continuacao For temperatura ponto 2
        if resultadoT2 != None:
            Resultado[T2] = resultadoT2
            if lastErro != None and lastErro < resultadoT2['erro']: return Resultado
            lastErro = resultadoT2['erro']
    return Resultado
    
def hInterno(Re, Pr, k, d_e):
    """
    Calcula o coeficiente de transferencia de calor no interior do tubo para o ponto desejado
    """
    h = None
    if Re < 2300: # Escoamento laminar
        h = 4.36 * k / d_e
        
    elif 2300 <= Re < 3000:# Escoamento de transicao
        hiL = 4.36 * k / d_e # laminar

        f = (0.790 * ln(Re) - 1.64)**(-2) # Fator de atrito
        Nu = ((f/8)*(Re-1000)*Pr)/(1+12.7*(f/8)**(0.5)*(Pr-1)) # Nusselt
        
        hiT = Nu * k / d_e # Turbulento
        
        xRe = (Re - 2300)/(3000-2300)
        
        h = (1-xRe)*hiL + xRe*hiT # media ponderada baseado no Re
        
    elif 3000 <= Re <= 5*10**6 and 0.5 < Pr < 2000: # Escoamento Turbulento
        f = (0.790 * ln(Re) - 1.64)**(-2) # Fator de atrito
        Nu = ((f/8)*(Re-1000)*Pr)/(1+12.7*(f/8)**(0.5)*(Pr-1)) # Nusselt
        
        h = Nu * k / d_e # Turbulento
        
    else:
        # Valores de Re e Pr fora da faixa aceitavel
        raise ValueError
            
    return h

def hExterno(Re, Pr, k, D):
    '''
    Calcula o valor do coeficiente convectivo externo, referente ao ar
    para escoamento ao redor de um cilindro
    '''
    Nu = 0.3 + ((0.62 * Re**0.5 * Pr**(1/3))/(1 + (0.4/Pr)**(2/3))**0.25) * (1 + (Re/282000)**(5/8))**(4/5)
    h = Nu * k / D
    return h

def hCondensacao(Ps, m, DcI, fluido):
    '''
    Calcula o coeficiente convectivo durante a condensacao
    '''
    p_r = Ps / Prop("PCRIT", fluido) # Pressao reduzida
    mi_l = Prop("V", "P", Ps, "Q", 0, fluido) # Viscosidade Dinamica
    Pr_l = Prop("PRANDTL", "P", Ps, "Q", 0, fluido)
    k_l = Prop("L", "P", Ps, "Q", 0, fluido)
    Z = p_r**0.4 # usando x=0.5, logo (1-x)/x = 1
    G = m / (PI*DcI**2/4) # vasao massica dividida pela area
    h_l = 0.023 * (G * 0.5 * DcI / mi_l)**0.8 * Pr_l**0.4 * k_l/ DcI # coeficiente do liquido
    h = h_l * (1 + 3.8/Z**0.95)
    return h

def hEvaporacao(Re_liq, Pr, k_l, d, x, rho_l, rho_v, m, sigma, Ts, hexterno, Tamb, i_lg):
    '''
    Calcula o coeficiente convectivo para uma dada frassao massica
    durante a evaporacao
    '''
    # 1o passo: encontrar h assumindo que nao ocorre ebulicao nucleada
    h_LO = 0.023*Re_liq**0.8*Pr**0.4*k_l
    G =  m/(2*d**2/4)
    Fr = G**2/(rho_l*g*d)
    if Fr > 0.04:
        Kfr = 1
    else:
        Kfr = (25*Fr)**-0.3
    Co = ((1-x)/x)**0.8 * (rho_v/rho_l)**0.5 * Kfr
    
    if Co >= 1:
        F_cb = 1 + 0.8 * exp(1-Co**0.5)
    else:
        F_cb = 1.8*Co**(-0.8)
    F_0 = F_cb * (1-x)
    h_TP = F_0 * h_LO # h para a ebulicao
    
    # 2o passo: encontrar a temperatura da parede para inicio da ebulicao nucleada
    U = 1/(1/h_TP + 1/hexterno)
    q2linha = U * (Tamb - Ts)
    T_WONB = (8*sigma*q2linha*Ts/(k_l*i_lg*rho_v))**0.5 + Ts
    T_w = q2linha/h_TP + Ts
    
    if T_WONB>T_w:
        return h_TP
    
    # 3o passo continuar o calculo considerando que ha nucleacao
    Bo = q2linha/(m*i_lg)
    if Bo < 1.9*10**(-5):
        return h_TP
    
    if Co >= 1:
        F_nb = 231*Bo**(-0.5)
        if F_cb>F_nb:
            return h_TP
        else:
            F_0 = F_nb*(1-x)
            h_TP = F_0 * h_LO
            return h_TP
    elif 0.02 < Co < 1:
        F_cnb = 231*Bo**(-0.5)*(0.77 + 0.13*F_cb)
        if F_cb > F_cnb:
            return h_TP
        else:
            F_0 = F_cnb * (1-x)
            h_TP = F_0 * h_LO
            return h_TP
    elif Co < 0.02:
        return h_TP

def eficienciaSuperficieAleta(DtuboExt, esp, hExt, k, areaTotal, areaAleta, raioEq=None, distFileira=None, distTubos=None):
    '''
    Calcula a eficiencia de superficie para trocador aletado
    '''
    if raioEq == None and not (distFileira != None and distTubos != None):
        print ('Falta dados')
        return
    
    r1 = DtuboExt/2
    if raioEq != None:
        r2 = raioEq
    else:
        r2 = (distFileira*distTubos/PI)**(0.5)
    r2c = r2 + esp/2
    m = (2*hExt/(k*esp))**0.5
    C2 = (2*r1/m)/(r2c**2-r1**2)
    efAleta = C2 * (K1(m*r1)*I1(m*r2c) - I1(m*r1)*K1(m*r2c)) / (I0(m*r1)*K1(m*r2c) - K0(m*r1)*I1(m*r2c))
    efSup = 1 - areaTotal/areaAleta * (1 - efAleta)
    return efSup

def raioEquivalente(dExterno, nTubos, alturaAleta, profundidadeAleta):
    '''
    Calcula o raio equivalente a partir da area.
    Todas as unidades devem ser a mesma, de forma que a saida sera correspondente.
    '''
    superficieAleta = alturaAleta * profundidadeAleta - PI * dExterno**2/4 * nTubos
    raioEq = ((superficieAleta/nTubos + PI*dExterno**2/4)/PI)**0.5
    return raioEq