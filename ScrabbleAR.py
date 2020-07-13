import configuracion
import PySimpleGUI as sg
import juego
import puntajes
sg.SetOptions(background_color='#abbccf',
       text_element_background_color='#abbccf',
       text_color='#222831',
       element_background_color='#9FB8AD',
       button_color=('#222831','#3db3fe'),
       text_justification='center',
       border_width=1,
       )
layout = [
[sg.Image(filename='imagenes/logo.png',background_color='#abbccf',size= (5600,100))],
    [sg.Button('Jugar',size= (30,1),pad=(50,6))],
    [sg.Button('Configurar',size= (30,1),pad=(50,6))],
    [sg.Button('Puntajes',size= (30,1),pad=(50,6))],
    [sg.Button('Salir',size= (30,1),pad=(50,6))],
    [sg.Text('Manuel Rúa',size= (500,2),pad=(0,20),font=("Arial", 12,'bold',),)],
]
listaConfiguracion={'PuntajeLetra':{'a':1,'b':3,'c':2,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':6,'k':8,'l':1,'m':3,'n':1,'o':1,'p':3,'q':8,'r':1,'s':1,'t':1,'u':1,'v':4,'w':8,'x':8,'y':4,'z':10},
'CantidadLetras':{'a':11,'b':3,'c':4,'d':4,'e':11,'f':2,'g':2,'h':2,'i':6,'j':2,'k':1,'l':4,'m':3,'n':5,'o':8,'p':2,'q':1,'r':4,'s':7,'t':4,'u':6,'v':2,'w':2,'x':1,'y':1,'z':1},
'TipoPalabra':['/PRP','/JJ','/AO', '/JJ', '/AQ', '/DI', '/DT','/VAG', '/VBG', '/VAI', '/VAN', '/MD', '/VAS', '/VMG', '/VMI', '/VB', '/VMM', '/VMN', '/VMP', '/VBN', '/VMS', '/VSG','/VSI', '/VSN', '/VSP', '/VSS'],
'TiempoTurno': 60,
'TiempoPartida': 1,
'TipoTablero':1,
'Nivel': 'medio'}

window = sg.Window('', layout, text_justification='center',size= (400,380),font=("Arial", 16))
while True:
    event, value = window.read()
    if event is None or event == 'Salir':
        break
    if event == 'Configurar':
        listaConfiguracion= configuracion.main()
    if event == 'Jugar':
        juego.main(listaConfiguracion)
    if event == 'Puntajes':
        puntajes.main()

window.close()

#prueva agregar cosas por github
