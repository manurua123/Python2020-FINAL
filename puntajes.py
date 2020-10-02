import PySimpleGUI as sg
import json
from operator import itemgetter

def ventana_error_archivo():
    '''
    indica que el archivo que se busca no existe en la ubicacion seleccionada
    '''
    layout = [[sg.Text('Falta el documento que almacena los puntajes maximos',)],
              [sg.OK(size=(10,2))]
              ]
    window = sg.Window('ERROR', layout)
    event, values = window.read()
    window.close()
def abrirArchivo(ruta,nivel):
    '''
    abre un archivo .json un diccionario con los puntajes maximos

    Parametros:
    ruta -- ruta del archivo .json
    nivel -- nivel de dificultad (facil, medio, dificul)

    Retorna:
    data[nivel] -- lista de puntajes del nivel solicitado.
    '''
    with open(ruta) as file:
        data = json.load(file)
        file.close()
    return(data[nivel])
def mostrarValores(datos,lista):
    '''muesta los primeros 10 valores de un lisa de valores

    Parametros:
    datos -- lista de puntajes de un nivel.
    lista -- lista vacia donde se cargan los 10 primero puntajes.
    '''
    del lista[:]
    newlist = sorted(datos, key=itemgetter('puntaje'), reverse=True)
    aux = 0
    for i in newlist:
        if(aux < 10):
            lista.append(i)
        aux = aux+1
def mostrarValoresTotal(ruta,lista):
    '''muesta los primeros 10 valores de un lisa de valores

    Parametros:
    datos -- lista de puntajes de todos los niveles.
    lista -- lista vacia donde se cargan los 10 primero puntajes.
    '''
    with open(ruta) as file:
        dato = json.load(file)
        file.close()
    listaAux = []
    for i in dato['facil']:
        listaAux.append(i)
    for i in dato['medio']:
        listaAux.append(i)
    for i in dato['dificil']:
        listaAux.append(i)
    newlist = sorted(listaAux, key=itemgetter('puntaje'), reverse=True)
    aux = 0
    for i in newlist:
        if(aux < 10):
            lista.append(i)
        aux = aux + 1

def main():
    botones=[
        [sg.Button('Nivel facil' , size=(15,2) , tooltip='los 10 mejores puntajes del nivel facil', auto_size_button=False,),sg.Button('Nivel medio' , size=(15,2) , tooltip='los 10 mejores puntajes del nivel medio', auto_size_button=False,),
        sg.Button('Nivel dificil' , size=(15,2) , tooltip='los 10 mejores puntajes del nivel medio', auto_size_button=False,),sg.Button('Todos' , size=(15,2) , tooltip='los 10 mejores puntajes en general', auto_size_button=False,)]
    ]
    layout_puntajes = [
        [sg.Image(filename='archivos/imagenes/puntajes.png',background_color='#abbccf',size= (5600,50))],
        [sg.Column(botones,pad=(10,0) )],
        [sg.Listbox('',size =(100,10),key='listbox',background_color='#abbccf'),],
        [sg.Button('Atras',size=(15,2),pad=(10,0))],
    ]
    window = sg.Window('Puntajes', layout_puntajes, text_justification='center',size= (650,400),font=("Arial", 13))
    while True:
        lista=[]
        event, value = window.read()
        try:
            if event is None or event == 'Atras':
                break
            if event == 'Nivel facil':
                del lista[:]
                mostrarValores(abrirArchivo('archivos/archivoPuntajes.json','facil'),lista)
                window.FindElement('listbox').Update(lista);
            if event == 'Nivel medio':
                del lista[:]
                mostrarValores(abrirArchivo('archivos/archivoPuntajes.json','medio'),lista)
                window.FindElement('listbox').Update(lista);
            if event == 'Nivel dificil':
                del lista[:]
                mostrarValores(abrirArchivo('archivos/archivoPuntajes.json','dificil'),lista)
                window.FindElement('listbox').Update(lista);
            if event == 'Todos':
                del lista[:]
                mostrarValoresTotal('archivos/archivoPuntajes.json',lista)
                window.FindElement('listbox').Update(lista);
        except FileNotFoundError:
            ventana_error_archivo()

    window.close()

if __name__ == '__main__':
    main()
