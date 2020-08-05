import configuracion
import juego
import puntajes


import PySimpleGUI as sg
import json
import webbrowser

sg.SetOptions(background_color='#abbccf',
       text_element_background_color='#abbccf',
       text_color='#222831',
       element_background_color='#9FB8AD',
       button_color=('#222831','#3db3fe'),
       text_justification='center',
       border_width=1,
       )
def abrirArchivo(ruta):
    with open(ruta) as file:
        data = json.load(file)
        file.close()
    return(data)
def ventana_error_geneal(ventana):
    '''
    indica que existe algun error desconocido
    '''
    layout = [[sg.Text('Sucedió un error inesperado',pad=(0,10),font=("Arial", 14),justification='center',size=(24,0))],
             [sg.Button('Ayuda',size= (30,2))]
              ]
    window = sg.Window('ERROR', layout,)
    while True:
        event, values = window.read()
        if event is None:
            break
        if event == 'Ayuda':
            webbrowser.open_new("https://github.com/manurua123/Python2020-FINAL")
            break
    window.close()

layout = [
[sg.Image(filename='archivos/imagenes/logo.png',background_color='#abbccf',size= (5600,100))],
    [sg.Button('Jugar',size= (30,1),pad=(50,6))],
    [sg.Button('Configurar',size= (30,1),pad=(50,6))],
    [sg.Button('Puntajes',size= (30,1),pad=(50,6))],
    [sg.Button('Ayuda',size= (30,1),pad=(50,6))],
    [sg.Button('Salir',size= (30,1),pad=(50,6))],
    [sg.Text('Manuel Rúa',size= (500,2),pad=(0,20),font=("Arial", 12,'bold',),)],
]


window = sg.Window('', layout, text_justification='center',size= (450,440),font=("Arial", 16))
try:
    listaConfiguracion = abrirArchivo('archivos/configuracion.json')
except FileNotFoundError:
    configuracion.ventana_error_archivo()
while True:
    try:
        event, value = window.read()
        if event is None or event == 'Salir':
            break
        if event == 'Configurar':
            listaConfiguracion = configuracion.main()
        if event == 'Jugar':
            juego.main(listaConfiguracion)
        if event == 'Puntajes':
            puntajes.main()
        if event == 'Ayuda':
            webbrowser.open_new("https://github.com/manurua123/Python2020-FINAL")
    except:
        ventana_error_geneal(window)
        break

window.close()
