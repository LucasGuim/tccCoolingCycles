import PySimpleGUI as sg



def janela_Inicial():
    sg.theme('Dark Blue 14')
    Ciclo1 =  [[sg.Radio('Ciclo Simples','Ciclo',key='CicloSimples')],[sg.Image(r'img1.png',size=(420,400))]]
    Ciclo2 = [[sg.Radio('Ciclo Cascata','Ciclo',key='CicloCascataSimples')],[sg.Image(r'img2.png',size=(420,400))]]
    Ciclo3=[[sg.Radio('Ciclo com camera Flash, tipo - 2','Ciclo',key='CicloCameraFlash')],[sg.Image(r'img3.png',size=(420,400))]]
    Ciclo4 = [[sg.Radio('Ciclo com camera Flash, tipo - 1','Ciclo',key='CicloCameraFlashCaso2')],[sg.Image(r'img4.png',size=(420,400))]]
    Ciclo5 = [[sg.Radio('Ciclo Simples com trocador de calor','Ciclo',key='CicloSimplesTrocador')],[sg.Image(r'img6.png',size=(420,400))]]
    
    layout = [  [sg.Text('Qual tipo de ciclo quer calcular ?')],
                [sg.TabGroup([[sg.Tab('Ciclos',Ciclo1),sg.Tab('Ciclo 2',Ciclo2),sg.Tab('Ciclo 3',Ciclo3),sg.Tab('Ciclo 4',Ciclo4),sg.Tab('Ciclo 5',Ciclo5)]])],
                [sg.Button('Continuar')]
            ]
    return sg.Window('Escolha do ciclo',layout=layout,finalize=True,auto_close=True)

def janela_CicloSimples():
    sg.theme('Reddit')
    layoutRight = [

        [sg.Button('Adicionar')],
        [sg.Input(key='CF',size=(5,5),default_text=0)],
        [sg.Input(key='Tc',size=(5,5))],
        [sg.Input(key='Te',size=(5,5))],
        [sg.Input(key='Tsa',size=(5,5),default_text='0')],
        [sg.Input(key='Tsub',size=(5,5),default_text='0')],
        [sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='Nis')],
        [sg.Button('Executar')]

        ]
    layoutLeft = [
        [sg.Combo(values=('R134a','R717','R600a','R600','R601a','R744','R22','NH3','R12','R32','R143A','R11','R290','R410a','R600','R50','R152a','R404a','R407c','R1233ZDE','R1234yf','R1234ZE','SO2','R1234ZE(Z)','R1234ZF','R1270','1-Butene','CO','O2','ISOBUTENE','ISOHEXANE','H2'),key='Refri')],
        [sg.Text('Capacidade Frigorífica (kW)')],
        [sg.Text('Temperatura do refrigerante no condensador (°C):')],
        [sg.Text('Temperatura do refrigerante no evaporador (°C):')],
        [sg.Text('Grau de superaquecimento (K)')],
        [sg.Text('Grau de subresfriamento (K)')],
        [sg.Text('Eficiência isentropica do compressor',pad=((0,0),(20,10)))],
        [sg.Button('Voltar')]
        ]
    
    
    layoutFinal = [ 
        [sg.Text('Escolha um ou mais fluidos refrigerantes')],
        [sg.Output(size=(66,6))],
        [[sg.Col(layoutLeft), sg.Col(layoutRight)]]
      ]

    return sg.Window('Ciclo de compressão simples',layout=layoutFinal,finalize=True)
def janela_CicloCascataSimples():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Capacidade Frigorífica (kW)'),sg.Input(key='CF',size=(5,5),default_text=0)],
            [sg.Text('Fluido refrigerante ciclo de pressão alta'),sg.Combo(values=('R134a','R717','R600a','R600','R12','R601a','R744','R22','R32','R143A','R11','R290','R410a','R600','R50','R152a','R404a','R407c','R1233ZDE','R1234yf','R1234ZE','SO2','R1234ZE(Z)','R1234ZF','R1270','1-Butene','CO','O2','ISOBUTENE','ISOHEXANE','H2'),key='RefriHP')],
            [sg.Text('Fluido refrigerante ciclo de pressão baixa'),sg.Combo(values=('R134a','R717','R600a','R600','R12','R601a','R744','R22','R32','R143A','R11','R290','R410a','R600','R50','R152a','R404a','R407c','R1233ZDE','R1234yf','R1234ZE','SO2','R1234ZE(Z)','R1234ZF','R1270','1-Butene','CO','O2','ISOBUTENE','ISOHEXANE','H2'),key='RefriPL')],
            [sg.Text('Eficiência isentropica do compressor de alta pressão'),sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='NisHP')],
            [sg.Text('Eficiência isentropica do compressor de baixa pressão'),sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='NisLP')],                
            [sg.Text('Temperatura do refrigerante no condensador de alta pressão (°C):'),sg.Input(key='TcHP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador de alta pressão (°C):'),sg.Input(key='TeHP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no condensador de baixa pressão (°C):'),sg.Input(key='TcLP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador de baixa pressão (°C):'),sg.Input(key='TeLP',size=(5,5))],
            [sg.Text('Grau de superaquecimento no ciclo de pressão alta (K)'),sg.Input(key='TsaHP',size=(5,5),default_text='0')],
            [sg.Text('Grau de superaquecimento no ciclo pressão baixa (K)'),sg.Input(key='TsaLP',size=(5,5),default_text='0')],
            [sg.Text('Grau de subresfriamento no ciclo de pressão alta (K)'),sg.Input(key='TsubH',size=(5,5),default_text='0')],
            [sg.Text('Grau de subresfriamento no ciclo de pressão baixa (K)'),sg.Input(key='TsubL',size=(5,5),default_text='0')],               
            [sg.Button('Voltar'),sg.Button('Calcular')],
             
            ]
    return sg.Window('Ciclo Cascata',layout=layout,finalize=True)



def telaCicloFlashCaso2():
    sg.theme('Reddit')
    layoutRight = [

        [sg.Button('Adicionar')],
        [sg.Input(key='CF',size=(5,5),default_text=0)],
        [sg.Input(key='Tc',size=(5,5))],
        [sg.Input(key='Te',size=(5,5))],
        [sg.Input(key='Tsa',size=(5,5),default_text='0')],
        [sg.Input(key='Tsub',size=(5,5),default_text='0')],
        [sg.Input(key='Pint',size=(5,5),default_text=0)],
        [sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='Nis')],
        [sg.Button('Calcular  ')]

        ]
    layoutLeft = [
        [sg.Combo(values=('R134a','R717','R600a','R600','R601a','R744','R22','R12','R32','R143A','R11','R290','R410a','R600','R50','R152a','R404a','R407c','R1233ZDE','R1234yf','R1234ZE','SO2','R1234ZE(Z)','R1234ZF','R1270','1-Butene','CO','O2','ISOBUTENE','ISOHEXANE','H2'),pad=((0,0),(10,10)),key='Refri')],
        [sg.Text('Capacidade Frigorífica (kW)')],
        [sg.Text('Temperatura do refrigerante no condensador (°C):')],
        [sg.Text('Temperatura do refrigerante no evaporador (°C):')],
        [sg.Text('Grau de superaquecimento (K)')],
        [sg.Text('Grau de subresfriamento (K)')],
        [sg.Text('Pressão Intermediaria (kPa):')],
        [sg.Text('Eficiência isentropica do compressor',pad=((5,0),(25,10)))],
        [sg.Button('Voltar')]
        ]
    
    
    layoutFinal = [ 
        [sg.Text('Escolha um ou mais fluidos refrigerantes')],
        [sg.Output(size=(66,6))],
        [[sg.Col(layoutLeft), sg.Col(layoutRight)]]
      ]

    return sg.Window('Ciclo com Camera Flash Caso 2 ',layout=layoutFinal,finalize=True)

def telaCicloFlashCaso1():
    sg.theme('Reddit')
    layoutRight = [

        [sg.Button('Adicionar')],
        [sg.Input(key='CF',size=(5,5),default_text=0)],
        [sg.Input(key='Tc',size=(5,5))],
        [sg.Input(key='Te',size=(5,5))],
        [sg.Input(key='Tsa',size=(5,5),default_text='0')],
        [sg.Input(key='Tsub',size=(5,5),default_text='0')],
        [sg.Input(key='Pint',size=(5,5),default_text=0)],
        [sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='Nis')],
        [sg.Button('Calcular  ')]

        ]
    layoutLeft = [
        [sg.Combo(values=('R134a','R717','R600a','R600','R601a','R744','R22','R12','R32','R143A','R11','R290','R410a','R600','R50','R152a','R404a','R407c','R1233ZDE','R1234yf','R1234ZE','SO2','R1234ZE(Z)','R1234ZF','R1270','1-Butene','CO','O2','ISOBUTENE','ISOHEXANE','H2'),pad=((0,0),(10,10)),key='Refri')],
        [sg.Text('Capacidade Frigorífica (kW)')],
        [sg.Text('Temperatura do refrigerante no condensador (°C):')],
        [sg.Text('Temperatura do refrigerante no evaporador (°C):')],
        [sg.Text('Grau de superaquecimento (K)')],
        [sg.Text('Grau de subresfriamento (K)')],
        [sg.Text('Pressão Intermediaria (kPa):')],
        [sg.Text('Eficiência isentropica do compressor',pad=((5,0),(25,10)))],
        [sg.Button('Voltar')]
        ]
    
    
    layoutFinal = [ 
        [sg.Text('Escolha um ou mais fluidos refrigerantes')],
        [sg.Output(size=(66,6))],
        [[sg.Col(layoutLeft), sg.Col(layoutRight)]]
      ]

    return sg.Window('Ciclo com Camera Flash Caso 1 ',layout=layoutFinal,finalize=True)

def janela_CicloSimplesComTrocador():
    sg.theme('Reddit')
    layoutRight = [

        [sg.Button('Adicionar')],
        [sg.Input(key='CF',size=(5,5),default_text=0)],
        [sg.Input(key='Tc',size=(5,5))],
        [sg.Input(key='Te',size=(5,5))],
        [sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='Nis')],
        [sg.Button('Executar ')]

        ]
    layoutLeft = [
        [sg.Combo(values=('R134a','R717','R600a','R600','R601a','R744','R22','R12','R32','R143A','R11','R290','R410a','R600','R50','R152a','R404a','R407c','R1233ZDE','R1234yf','R1234ZE','SO2','R1234ZE(Z)','R1234ZF','R1270','1-Butene','CO','O2','ISOBUTENE','ISOHEXANE','H2'),key='Refri')],
        [sg.Text('Capacidade Frigorífica (kW)')],
        [sg.Text('Temperatura do refrigerante no condensador (°C):')],
        [sg.Text('Temperatura do refrigerante no evaporador (°C):')],
        [sg.Text('Eficiência isentropica do compressor',pad=((0,0),(20,10)))],
        [sg.Button('Voltar')]
        ]
    
    
    layoutCoringa = [ 
        [sg.Text('Escolha um ou mais fluidos refrigerantes')],
        [sg.Output(size=(66,6))],
        [[sg.Col(layoutLeft), sg.Col(layoutRight)]]
      ]

    return sg.Window('Ciclo de compressão simples com trocador de calor',layout=layoutCoringa,finalize=True)