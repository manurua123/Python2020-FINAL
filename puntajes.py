import PySimpleGUI as sg
import json
from operator import itemgetter
sg.SetOptions(background_color='#222831',
       text_element_background_color='#222831',
       element_background_color='#9FB8AD',
       button_color=('#222831','#00adb5'),
       text_justification='center',
       border_width=1,
       )

def abrirArchivo(ruta,nivel):
    with open(ruta) as file:
        data = json.load(file)
        file.close()
    return(data[nivel])
def mostrarValores(datos,lista):
    del lista[:]
    newlist = sorted(datos, key=itemgetter('puntaje'), reverse=True)
    aux = 0
    for i in newlist:
        if(aux < 10):
            lista.append(i)
        aux = aux 
def mostrarValoresTotal(ruta,lista):
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

layout_puntajes = [
 [sg.Text('TOP 10' , size=(550,2) ,font=("Helvetica", 15,'bold')),],
 [sg.Button('Nivel facil' , size=(15,2) , tooltip='los 10 mejores puntajes del nivel facil', auto_size_button=False,),sg.Button('Nivel medio' , size=(15,2) , tooltip='los 10 mejores puntajes del nivel medio', auto_size_button=False,),
 sg.Button('Nivel dificil' , size=(15,2) , tooltip='los 10 mejores puntajes del nivel medio', auto_size_button=False,),sg.Button('Todos' , size=(15,2) , tooltip='los 10 mejores puntajes en general', auto_size_button=False,)],
 [sg.Listbox('',size =(100,10),key='listbox',background_color='#9FB8AD'),],
 [sg.Button('Atras',size=(15,3))],
]

def main():
    layout_puntajes = [
     [sg.Text('TOP 10' , size=(550,2) ,font=("Helvetica", 15,'bold')),],
     [sg.Button('Nivel facil' , size=(15,2) , tooltip='los 10 mejores puntajes del nivel facil', auto_size_button=False,),sg.Button('Nivel medio' , size=(15,2) , tooltip='los 10 mejores puntajes del nivel medio', auto_size_button=False,),
     sg.Button('Nivel dificil' , size=(15,2) , tooltip='los 10 mejores puntajes del nivel medio', auto_size_button=False,),sg.Button('Todos' , size=(15,2) , tooltip='los 10 mejores puntajes en general', auto_size_button=False,)],
     [sg.Listbox('',size =(100,10),key='listbox',background_color='#9FB8AD'),],
     [sg.Button('Atras',size=(15,3))],
    ]
    window = sg.Window('Puntajes', layout_puntajes, text_justification='center',size= (600,370),font=("Helvetica", 13))
    while True:
        lista=[]
        event, value = window.read()
        if event is None or event == 'Atras':
            break
        if event == 'Nivel facil':
            del lista[:]
            mostrarValores(abrirArchivo('archivoPuntajes.json','facil'),lista)
            window.FindElement('listbox').Update(lista);
        if event == 'Nivel medio':
            del lista[:]
            mostrarValores(abrirArchivo('archivoPuntajes.json','medio'),lista)
            window.FindElement('listbox').Update(lista);
        if event == 'Nivel dificil':
            del lista[:]
            mostrarValores(abrirArchivo('archivoPuntajes.json','dificil'),lista)
            window.FindElement('listbox').Update(lista);
        if event == 'Todos':
            del lista[:]
            mostrarValoresTotal('archivoPuntajes.json',lista)
            window.FindElement('listbox').Update(lista);
    window.close()

if __name__ == '__main__':
    main()
#lo mismo que en configuracion
