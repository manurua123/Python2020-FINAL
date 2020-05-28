import PySimpleGUI as sg
import json

def obtener_listado(ruta,nivel_seleccionado):
    archivo_niveles=open(ruta,'r')
    lista_niveles=json.loads(archivo_niveles)
    json.close()
    if nivel_seleccionado is 'Nivel facil':
        dicc_niveles=lista_niveles['nivel_facil']         #se guarda en el dicc a los puntajes del modo facil
        ventana_puntajes('Nivel facil',dicc_niveles)
    if nivel_seleccionado is 'Nivel medio':
        dicc_niveles=lista_niveles['nivel_medio']         #se guarda en el dicc a los puntajes del modo facil
        ventana_puntajes('Nivel medio',dicc_niveles)
    if nivel_seleccionado is 'Nivel dificil':
        dicc_niveles=lista_niveles['nivel_dificil']         #se guarda en el dicc a los puntajes del modo facil
        ventana_puntajes('Nivel dificil',dicc_niveles)

def ventana_puntajes(nivel,dicc_niveles):
    layout=[
     [sg.Text('Puntejes del',nivel)],
     [sg.Text(dicc_niveles)]
    ]

layout_puntajes = [
 [sg.Text('Seleccione top 10 puntajes' , size=(20,2) , font=('Arial',12,'bold'))],
 [sg.Button('Nivel facil' , size=(20,2) , tooltip='recibira un listado de los 10 mejores puntajes del nivel facil')],
 [sg.Button('Nivel medio' , size=(20,2) , tooltip='recibir un listado de los 10 mejores puntajes del nivel medio')],
 [sg.Button('Nivel dificil' , size=(20,2) , tooltip='recibir un listado de los 10 mejores puntajes del nivel medio')]
]

def main():
    window = sg.Window('', layout_puntajes, text_justification='center',size= (200,250),)
    while True:
        event, value = window.read()
        if event is None:
            break
        if event == 'Nivel facil':
            obtener_listado('archivopuntajes','Nivel facil')
        if event == 'Nivel medio':
            obtener_listado('archivopuntajes','Nivel medio')
        if event == 'Nivel dificil':
            obtener_listado('archivopuntajes','Nivel dificil')
    window.close()

if __name__ == '__main__':
    main()
#lo mismo que en configuracion
