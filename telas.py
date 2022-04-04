import PySimpleGUI as sg

def janela_CicloSimples():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Calcule a eficiência do seu ciclo de refrigeração  ')],
            [sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a'),key='Combo')],           
            [sg.Text('Temperatura do refrigerante no condensador em °C:'),sg.Input(key='Tc',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador em °C:'),sg.Input(key='Te',size=(5,5))],
            [sg.Text('Temperatura de superaquecimento'),sg.Input(key='Tsa',size=(5,5))],
            [sg.Text('Eficiência isentropica do compressor'),sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='Nis')],
            [sg.Button('Voltar'),sg.Button('Executar')],
            [sg.Output(size=(40,15))]           
            ]
    return sg.Window('Ciclo de compreesão simples',layout=layout,finalize=True)
def janela_CicloCascataSimples():
    sg.theme('Reddit')
    layout = [
            [sg.Text('Capacidade Frigorífica em KW'),sg.Input(key='CF',size=(5,5))],
            [sg.Text('Fluido refrigerante ciclo de pressão alta'),sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a','R22'),key='RefriHP')],
            [sg.Text('Fluido refrigerante ciclo de pressão baixa'),sg.Combo(values=('R134a','Water','R717','R600a', 'R290','R1234yf', 'R1234ze(E)', 'R410a','R22'),key='RefriPL')],
            [sg.Text('Eficiência isentropica do compressor'),sg.Slider(range=(0,1),default_value=(0.7),resolution=0.1,orientation='h',key='Nis')],            
            [sg.Text('Temperatura do refrigerante no condensador de alta pressão em °C:'),sg.Input(key='TcHP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador de alta pressão em °C:'),sg.Input(key='TeHP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no condensador de baixa pressão em °C:'),sg.Input(key='TcLP',size=(5,5))],
            [sg.Text('Temperatura do refrigerante no evaporador de baixa pressão em °C:'),sg.Input(key='TeLP',size=(5,5))],
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
            [sg.Text('Pressão Intermediaria'),sg.Input(key='Pint',size=(5,5))],
            
            [sg.Button('Voltar'),sg.Button('Calcular ')],
            [sg.Output(size=(40,15))]  
            ]
    return sg.Window('Ciclo com Camera Flash',layout=layout,finalize=True)