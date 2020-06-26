import random
import PySimpleGUI as sg
sg.SetOptions(background_color='#222831',
       text_element_background_color='#222831',
       element_background_color='#9FB8AD',
       button_color=('#222831','#00adb5'),
       text_justification='center',
       border_width=1,

       )
letras_puntos={'a':1,'b':3,'c':2,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':6,'k':8,'l':1,'m':3,'n':1,'o':1,'p':3,'q':8,'r':1,'s':1,'t':1,'u':1,'v':4,'w':8,'x':8,'y':4,'z':10}
letras_cantidad={'a':11,'b':3,'c':4,'d':4,'e':11,'f':2,'g':2,'h':2,'i':6,'j':2,'k':1,'l':4,'m':3,'n':5,'o':8,'p':2,'q':1,'r':4,'s':7,'t':4,'u':6,'v':2,'w':2,'x':1,'y':1,'z':1}

def nivel_facil(letrasPuntos,letrasCantidad):
    for i in letrasPuntos.keys():
        letrasPuntos[i] = letrasPuntos[i] *3
        letrasCantidad[i] = letrasCantidad[i]*3
    tipoPalabra = ['/VB','/AO', '/JJ', '/AQ', '/DI', '/DT','/VAG', '/VBG', '/VAI', '/VAN', '/MD', '/VAS', '/VMG', '/VMI', '/VB', '/VMM', '/VMN', '/VMP', '/VBN', '/VMS', '/VSG',
                 '/VSI', '/VSN', '/VSP', '/VSS','/PRP','/JJ']
    return {'PuntajeLetra':letrasPuntos,'CantidadLetras':letrasCantidad,'TipoPalabra':tipoPalabra,'TipoTablero':1,'Nivel': 'facil'}

def nivel_medio(letrasPuntos,letrasCantidad):
    for i in letrasPuntos.keys():
        letrasPuntos[i] = letrasPuntos[i] *2
        letrasCantidad[i] = letrasCantidad[i]*2
    tipoPalabra = ['/VB','/AO', '/JJ', '/AQ', '/DI', '/DT','/VAG', '/VBG', '/VAI', '/VAN', '/MD', '/VAS', '/VMG', '/VMI', '/VB', '/VMM', '/VMN', '/VMP', '/VBN', '/VMS', '/VSG',
                 '/VSI', '/VSN', '/VSP', '/VSS']
    return {'PuntajeLetra':letrasPuntos,'CantidadLetras':letrasCantidad,'TipoPalabra':tipoPalabra,'TipoTablero':2,'Nivel': 'medio'}

def nivel_dificil(letrasPuntos,letrasCantidad):
    for i in letrasPuntos.keys():
        letrasPuntos[i] = letrasPuntos[i]
        letrasCantidad[i] = letrasCantidad[i]
    tipos= ['/VB','/AO', '/JJ', '/AQ', '/DI', '/DT','/VAG', '/VBG', '/VAI', '/VAN', '/MD', '/VAS', '/VMG', '/VMI', '/VB', '/VMM', '/VMN', '/VMP', '/VBN', '/VMS', '/VSG',
                 '/VSI', '/VSN', '/VSP', '/VSS']
    tipoPalabra=list(random.choice(tipos))
    return {'PuntajeLetra':letrasPuntos,'CantidadLetras':letrasCantidad,'TipoPalabra':tipoPalabra,'TipoTablero':3,'Nivel': 'dificil'}


def main():
    layout = [
        [sg.Text('Duracion del TURNO',size = (25,1)), sg.Slider(background_color='#222831',range = (10, 120),orientation = 'h', size = (20,20), default_value = 60, key = 'tiempoTurno',tooltip='Duracion del turno en segundos')],
        [sg.Text('Duracion de la PARTIDA',size = (25,1)), sg.Slider(background_color='#222831',range = (5, 15),orientation = 'h', size = (20,20), default_value = 10, key = 'tiempoPartida',tooltip='Duracion total de la partida en minutos')],
        [sg.Text('Nivel de dificultad',),
        sg.Button('Facil',tooltip='Fichas: Muchas\nPuntos: Muchos\nCategorias: TODAS',size= (8,2),pad=(3,4),),
        sg.Button('Medio',tooltip='Fichas: Algunas\nPuntos: Normal\nCategorias: Verbos | Adjetivos ',size= (8,2),pad=(3,4)),
        sg.Button('Dificil',tooltip='Fichas: Pocas\nPuntos: Pocos\nCategorias:Verbos | Adjetivos',size= (8,2),pad=(3,4))],
        [sg.Button('Confirmar',disabled=True,size= (200,2),pad=(1,4))],
        [sg.Button('Cancelar',size= (200,2),pad=(1,4))],
    ]
    window = sg.Window('Configuracion', layout, text_justification='center',size= (420,280),font=('Helvetica', 13))
    while True:
        event, value = window.read()
        if event is None or event == 'Cancelar':
            listaConfiguracion = nivel_medio(letras_puntos,letras_cantidad)
            listaConfiguracion['TiempoTurno'] = 60
            listaConfiguracion['TiempoPartida'] =10
            break
        if event == 'Facil':
            listaConfiguracion = nivel_facil(letras_puntos,letras_cantidad)
            window['Facil'].update(disabled=True)
            window['Medio'].update(disabled=False)
            window['Dificil'].update(disabled=False)
            window['Confirmar'].update(disabled=False)
        if event == 'Medio':
            listaConfiguracion = nivel_medio(letras_puntos,letras_cantidad)
            window['Facil'].update(disabled=False)
            window['Medio'].update(disabled=True)
            window['Dificil'].update(disabled=False)
            window['Confirmar'].update(disabled=False)
        if event == 'Dificil':
            listaConfiguracion = nivel_dificil(letras_puntos,letras_cantidad)
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
#a
