import PySimpleGUI as sg



def janela_Inicial():
    sg.theme('Dark Grey 13')
    Ciclo1 =  [[sg.Radio('Ciclo Simples','Ciclo',key='CicloSimples')],[sg.Image(r'img1.png',size=(420,400))]]
    Ciclo2 = [[sg.Radio('Ciclo Cascata','Ciclo',key='CicloCascataSimples')],[sg.Image(r'img2.png',size=(420,400))]]
    Ciclo3=[[sg.Radio('Ciclo com camera Flash, tipo - 2','Ciclo',key='CicloCameraFlash')],[sg.Image(r'img3.png',size=(420,400))]]
    Ciclo4 = [[sg.Radio('Ciclo com camera Flash, tipo - 1','Ciclo',key='CicloCameraFlashCaso2')],[sg.Image(r'img4.png',size=(420,400))]]
    
    layout = [  [sg.Text('Olá, Lucas ')],
                [sg.Text('Qual tipo de ciclo quer calcular ?')],
                [sg.TabGroup([[sg.Tab('Ciclos',Ciclo1),sg.Tab('Ciclo 2',Ciclo2),sg.Tab('Ciclo 3',Ciclo3),sg.Tab('Ciclo 4',Ciclo4)]])],
                [sg.Button('Continuar')]
            ]
    return sg.Window('Escolha do ciclo',layout=layout,finalize=True,auto_close=True)

def janela_CicloSimples():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Calcule a eficiência do seu ciclo de refrigeração  ')],
            [sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a'),key='Combo')],           
            [sg.Text('Temperatura do refrigerante no condensador em °C:'),sg.Input(key='Tc',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador em °C:'),sg.Input(key='Te',size=(5,5))],
            [sg.Text('Temperatura de superaquecimento'),sg.Input(key='Tsa',size=(5,5),default_text='0')],
            [sg.Text('Temperatura de subresfriamento'),sg.Input(key='Tsub',size=(5,5),default_text='0')],
            [sg.Text('Eficiência isentropica do compressor'),sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='Nis')],
            [sg.Button('Voltar'),sg.Button('Executar')],
            [sg.Output(size=(55,25))]           
            ]
    return sg.Window('Ciclo de compreesão simples',layout=layout,finalize=True)
def janela_CicloCascataSimples():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Capacidade Frigorífica em KW'),sg.Input(key='CF',size=(5,5))],
            [sg.Text('Fluido refrigerante ciclo de pressão alta'),sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a','R22'),key='RefriHP')],
            [sg.Text('Fluido refrigerante ciclo de pressão baixa'),sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a','R22'),key='RefriPL')],
            [sg.Text('Eficiência isentropica do compressor de alta pressão'),sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='NisHP')],
            [sg.Text('Eficiência isentropica do compressor de baixa pressão'),sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='NisLP')],                
            [sg.Text('Temperatura do refrigerante no condensador de alta pressão em °C:'),sg.Input(key='TcHP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador de alta pressão em °C:'),sg.Input(key='TeHP',size=(5,5))],
            [sg.Text('Temperatura de superaquecimento no ciclo pressão alta'),sg.Input(key='TsaHP',size=(5,5),default_text='0')],
            [sg.Text('Temperatura do refrigerante no condensador de baixa pressão em °C:'),sg.Input(key='TcLP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador de baixa pressão em °C:'),sg.Input(key='TeLP',size=(5,5))],
            [sg.Text('Temperatura de superaquecimento no ciclo pressão baixa'),sg.Input(key='TsaLP',size=(5,5),default_text='0')],
            [sg.Button('Voltar'),sg.Button('Calcular')],
            [sg.Output(size=(50,30))]  
            ]
    return sg.Window('Ciclo Cascata',layout=layout,finalize=True)
def janela_CicloCameraFlash():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Capacidade Frigorífica em KW'),sg.Input(key='CF',size=(5,5))],
            [sg.Text('Fluido refrigerante'),sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a','R22'),key='Refri')],
            [sg.Text('Eficiência isentropica do compressor'),sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='Nis')],        
            [sg.Text('Pressão no condensador em kPa:'),sg.Input(key='Pc',size=(5,5))],
            [sg.Text('Pressão no evaporador  em kPa:'),sg.Input(key='Pe',size=(5,5))],
            [sg.Text('Pressão Intermediaria em kPa:'),sg.Input(key='Pint',size=(5,5))],
            
            [sg.Button('Voltar'),sg.Button('Calcular ')],
             [sg.Output(size=(40,15))]  
            ]
    return sg.Window('Ciclo com Camera Flash',layout=layout,finalize=True)

def janela_CicloFlashCaso2():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Capacidade Frigorífica em KW'),sg.Input(key='CF',size=(5,5))],
            [sg.Text('Fluido refrigerante'),sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a','R22'),key='Refri')],
            [sg.Text('Eficiência isentropica do compressor'),sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='Nis')],        
            [sg.Text('Temperatura do refrigerante no condensador em °C'),sg.Input(key='Tc',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador em °C'),sg.Input(key='Te',size=(5,5))],
            [sg.Text('Pressão Intermediaria em kPa:'),sg.Input(key='Pint',size=(5,5))],            
            [sg.Button('Voltar'),sg.Button('Calcular  ')],
            [sg.Output(size=(40,15))]  
            ]
    return sg.Window('Ciclo com Camera Flash',layout=layout,finalize=True)
