import random
import PySimpleGUI as sg
import json

def abrirArchivo(ruta):
    with open(ruta) as file:
        data = json.load(file)
        file.close()
    return(data)
def ventana_error_archivo():
    '''
    indica que el archivo que se busca no existe en la ubicacion seleccionada
    '''
    layout = [[sg.Text('no se encontro el archivo de configuracion',pad=(0,10),font=("Arial", 14),justification='center',size=(24,0))],
              [sg.OK(size=(32,2))]
              ]
    window = sg.Window('ERROR', layout)
    event, values = window.read()
    window.close()

def nivel_facil(letrasPuntos,letrasCantidad):
    letrasPuntosF={}
    letrasCantidadF={}
    for i in letrasPuntos.keys():
        letrasPuntosF[i] = letrasPuntos[i] *2
        letrasCantidadF[i] = letrasCantidad[i]*2
    tipoPalabra = ['/VB','/AO', '/JJ', '/AQ', '/DI', '/DT','/VAG', '/VBG', '/VAI', '/VAN', '/MD', '/VAS', '/VMG', '/VMI', '/VB', '/VMM', '/VMN', '/VMP', '/VBN', '/VMS', '/VSG',
                 '/VSI', '/VSN', '/VSP', '/VSS','/PRP','/JJ','/PRP$','/NN','/DT','/VBG',]
    return {'PuntajeLetra':letrasPuntosF,'CantidadLetras':letrasCantidadF,'TipoPalabra':tipoPalabra,'TipoTablero':1,'Nivel': 'facil'}

def nivel_medio(letrasPuntos,letrasCantidad):
    tipoPalabra = ['/VB','/AO', '/JJ', '/AQ', '/DI', '/DT','/VAG', '/VBG', '/VAI', '/VAN', '/MD', '/VAS', '/VMG', '/VMI', '/VB', '/VMM', '/VMN', '/VMP', '/VBN', '/VMS', '/VSG',
                 '/VSI', '/VSN', '/VSP', '/VSS','/VBG',]
    return {'PuntajeLetra':letrasPuntos,'CantidadLetras':letrasCantidad,'TipoPalabra':tipoPalabra,'TipoTablero':2,'Nivel': 'medio'}

def nivel_dificil():
    letrasPuntos={'a':1,'b':2,'c':2,'d':2,'e':1,'f':2,'g':2,'h':2,'i':1,'j':3,'k':4,'l':1,'m':1,'n':1,'o':1,'p':1,'q':4,'r':1,'s':1,'t':1,'u':1,'v':2,'w':4,'x':4,'y':2,'z':5}
    letrasCantidad={'a':11,'b':3,'c':4,'d':4,'e':11,'f':2,'g':2,'h':2,'i':6,'j':2,'k':1,'l':4,'m':3,'n':5,'o':8,'p':2,'q':1,'r':4,'s':7,'t':4,'u':6,'v':2,'w':2,'x':1,'y':1,'z':1}
    tipos= ['/VB','/AO', '/JJ', '/AQ', '/DI', '/DT','/VAG', '/VBG', '/VAI', '/VAN', '/MD', '/VAS', '/VMG', '/VMI', '/VB', '/VMM', '/VMN', '/VMP', '/VBN', '/VMS', '/VSG',
                 '/VSI', '/VSN', '/VSP', '/VSS','/VBG',]
    tipoPalabra=list(random.choice(tipos))
    return {'PuntajeLetra':letrasPuntos,'CantidadLetras':letrasCantidad,'TipoPalabra':tipoPalabra,'TipoTablero':3,'Nivel': 'dificil'}

def main():
    layout = [
        [sg.Text('Duracion del TURNO',size = (25,1)), sg.Slider(background_color='#abbccf',range = (10, 120),orientation = 'h', size = (20,20), default_value = 60, key = 'tiempoTurno',tooltip='Duracion del turno en segundos')],
        [sg.Text('Duracion de la PARTIDA',size = (25,1)), sg.Slider(background_color='#abbccf',range = (5, 15),orientation = 'h', size = (20,20), default_value = 10, key = 'tiempoPartida',tooltip='Duracion total de la partida en minutos')],
        [sg.Text('Nivel de dificultad',),
        sg.Button('Facil',tooltip='Fichas: Muchas\nPuntos: Muchos\nCategorias: TODAS',size= (8,2),pad=(3,4),),
        sg.Button('Medio',tooltip='Fichas: Algunas\nPuntos: Normal\nCategorias: Verbos | Adjetivos ',size= (8,2),pad=(3,4)),
        sg.Button('Dificil',tooltip='Fichas: Pocas\nPuntos: Pocos\nCategorias:Verbos | Adjetivos',size= (8,2),pad=(3,4))],
        [sg.Button('Confirmar',disabled=True,size= (20,2)),sg.Button('Cancelar',size= (20,2),)],
    ]
    window = sg.Window('Configuracion', layout, text_justification='center',size= (420,220),font=('Arial', 13))
    try:
        listaConfiguracion = abrirArchivo('archivos/configuracion.json')
    except FileNotFoundError:
        ventana_error_archivo()

    while True:
        event, value = window.read()
        if event is None or event == 'Cancelar':
            listaConfiguracion = nivel_medio(listaConfiguracion['PuntajeLetra'],listaConfiguracion['CantidadLetras'])
            listaConfiguracion['TiempoTurno'] = 60
            listaConfiguracion['TiempoPartida'] =10
            break
        if event == 'Facil':
            listaConfiguracion = nivel_facil(listaConfiguracion['PuntajeLetra'],listaConfiguracion['CantidadLetras'])
            window['Facil'].update(disabled=True)
            window['Medio'].update(disabled=False)
            window['Dificil'].update(disabled=False)
            window['Confirmar'].update(disabled=False)
        if event == 'Medio':
            listaConfiguracion = nivel_medio(listaConfiguracion['PuntajeLetra'],listaConfiguracion['CantidadLetras'])
            window['Facil'].update(disabled=False)
            window['Medio'].update(disabled=True)
            window['Dificil'].update(disabled=False)
            window['Confirmar'].update(disabled=False)
        if event == 'Dificil':
            listaConfiguracion = nivel_dificil()
            window['Facil'].update(disabled=False)
            window['Medio'].update(disabled=False)
            window['Dificil'].update(disabled=True)
            window['Confirmar'].update(disabled=False)
        if event == 'Confirmar':
            listaConfiguracion['TiempoTurno'] = value['tiempoTurno']
            listaConfiguracion['TiempoPartida'] = value['tiempoPartida']
            break
    window.close()
    return listaConfiguracion

if __name__ == '__main__':
    main()
