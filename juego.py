#liberias
import PySimpleGUI as sg
import random
import string

from pattern.es import parse
import pattern.es
import time
from datetime import datetime, date, time, timedelta
import json
from itertools import permutations
from time import sleep

#otros archivos.py
import bloqueos
import turnoPC
import cambiarLetras

#configurtacion de colores

#valores para testear
listaPorDefecto={'PuntajeLetra':{'a':1,'b':3,'c':2,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':6,'k':8,'l':1,'m':3,'n':1,'o':1,'p':3,'q':8,'r':1,'s':1,'t':1,'u':1,'v':4,'w':8,'x':8,'y':4,'z':10},
'CantidadLetras':{'a':11,'b':3,'c':4,'d':4,'e':11,'f':2,'g':2,'h':2,'i':6,'j':2,'k':1,'l':4,'m':3,'n':5,'o':8,'p':2,'q':1,'r':4,'s':7,'t':4,'u':6,'v':2,'w':2,'x':1,'y':1,'z':1},
'TipoPalabra':['/WP','/AO', '/JJ', '/AQ', '/DI', '/DT','/VAG', '/VBG', '/VAI', '/VAN', '/MD', '/VAS', '/VMG', '/VMI', '/VB', '/VMM', '/VMN', '/VMP', '/VBN', '/VMS', '/VSG', '/VSI', '/VSN', '/VSP', '/VSS'],
'TiempoTurno': 30,
'TiempoPartida':1,
'TipoTablero':2,
'Nivel': 'medio'}
#clases de los botones, tablero, atril pc y atril jugador
class BotonLetra():
    def __init__ (self,nivel,x,y=0,):
        self.valor= 'nulo'
        self.x = x
        self.y = y
        self.estado = 0    #0 si esta libre o 1 si esta ocupado
        self.bloqueo = True  #bloquea el boton para evitar bugs
        self.key = (x,y)
        self.nivel = nivel
        self.boton  = sg.Button( image_filename='imagenes/fichas/{}/{}.png'.format(self.nivel,self.valor), image_size=(40, 40),key = self.key,disabled=self.bloqueo,pad=(1,1), button_color=('#222831','#fbfbfb'),)
        self.tipo = 0
    def update(self):
        self.boton.update(image_filename='imagenes/fichas/{}/{}.png'.format(self.nivel,self.valor),disabled=self.bloqueo)
    def getLetra(self):
        return self.valor
    def setLetra(self,v):
        self.valor = v
        self.estado = 1
        self.update()
    def desbloquear(self):
        self.bloqueo = False
        self.update()
    def bloquear(self):
        self.bloqueo = True
        self.update()
    def vaciar(self):
        if(self.tipo == 0):
            self.valor = 'nulo'
        elif(self.tipo == 1):
            self.valor='palabrax2'
        elif(self.tipo == 2):
            self.valor='letrax2'
        elif(self.tipo == 3):
            self.valor='restaletra'
        elif(self.tipo == 4):
            self.valor='centro'
        self.estado = 0
        self.update()
    def getEstado(self):
        return self.estado
    def setEstado(self,e):
        self.estado = e
    def getTipo(self):
        return self.tipo
    def marcar(self):
        self.estado = 0
        self.bloqueo = True
        self.boton.update(image_filename='imagenes/fichas/{}/{}.png'.format(self.nivel,self.valor),disabled=self.bloqueo,button_color=('#222831','#f6d743'))
        return self.valor
class BotonAtril(BotonLetra):
    def __init__ (self,nivel,x):
        BotonLetra.__init__ (self,nivel,x)
class BotonTablero(BotonLetra):
    def __init__ (self,nivel,x,y):
        BotonLetra.__init__ (self,nivel,x,y)
    def tipoCelda(self,valor):
        '''
        actualiza el color y el tipo de boton segun los multiplicadores que tenga
        '''
        if (valor ==1):
            self.tipo=valor
            self.valor='palabrax2'
            self.boton.update(image_filename='imagenes/fichas/{}/{}.png'.format(self.nivel,self.valor),button_color=('black','#21bf73')) #PALABRA x2
        if(valor== 2):
            self.tipo=valor
            self.valor='letrax2'
            self.boton.update(image_filename='imagenes/fichas/{}/{}.png'.format(self.nivel,self.valor),button_color=('black','#4f98ca')) #LETRAS x2
        if(valor== 3):
            self.tipo=valor
            self.valor='restaletra'
            self.boton.update(image_filename='imagenes/fichas/{}/{}.png'.format(self.nivel,self.valor),button_color=('black','#fd5e53')) #Resta Letra
        if(valor == 4):
            self.tipo=valor
            self.valor='centro'
            self.boton.update(image_filename='imagenes/fichas/{}/{}.png'.format(self.nivel,self.valor),button_color=('#222831','#e0dede')) #centro
        else:
            None
class BotonesAtrilPC():
    def __init__ (self,nivel,x):
        self.valor= 'nulo'
        self.x = x
        self.estado = 0    #0 si esta libre o 1 si esta ocupado
        self.bloqueo = True  #bloquea el boton para evitar bugs
        self.key = (x,0)
        self.nivel = nivel
        self.boton  = sg.Button(image_filename='imagenes/fichas/{}/secreto.png'.format(self.nivel),key = self.key,disabled=self.bloqueo,pad=(1,1), button_color=('#222831','#e0dede'))
        self.tipo = 0
    def update(self):
        self.boton.update(image_filename='imagenes/fichas/{}/secreto.png'.format(self.nivel))
    def getLetra(self):
        return self.valor
    def setLetra(self,v):
        self.valor = v
        self.estado = 1
    def getEstado(self):
        return self.estado
    def vaciar(self):
        self.valor = 'nulo'
        self.estado = 0
        self.update()

#Atril del la maquina, del jugador y el tablero de juego
AtrilLetrasPC = [0 for y in range(7)]                                           #creo una lista de vacia con 7 lugares [0,0,0,0,0,0,0,0]
def botonesAtrilPC(nivel,x):
    '''genera un boton en la cordenada x'''
    AtrilLetrasPC[x] =  BotonesAtrilPC(nivel,x)
    return AtrilLetrasPC[x].boton
AtrilLetras = [0 for y in range(7)]                                             #creo una lista de vacia con 7 lugares [0,0,0,0,0,0,0,0]
def botonesAtril(nivel,x,atril):
    '''genera un boton en la pocicion x del atril'''
    atril[x] = BotonAtril(nivel,x)
    return atril[x].boton
TableroLetras = [[' ' for a in range(0,15)] for b in range(0,15)]               #creo una matriz de 15x15 vacia
def botonTablero(nivel,x,y):
    '''genera un boton en las cordenadas (x,y)'''
    TableroLetras[x][y] = BotonTablero(nivel,x,y)
    return TableroLetras[x][y].boton

#inicil de la partida
def abrirPartida(window,tablero,atrilPJ,atrilPC,listaConfiguracion,puntosPJ,puntosPC):
    '''abre un .json con el tablero de juego, el atril del jugador, el de la PC y la cantidad de letras existentes y lo añade a la partida '''
    with open('partidaGuardada.json','r+') as file:
        datos = json.load(file)
    for x in range(15):
        for y in range(15):
            tablero[x][y].setLetra(datos['tablero']['{},{}'.format(x,y)])
            tablero[x][y].tipoCelda(datos['tipoTablero']['{},{}'.format(x,y)])
            tablero[x][y].setEstado(datos['estadoTablero']['{},{}'.format(x,y)])
    for x in range(7):
        atrilPJ[x].setLetra(datos['atrilPJ']['{}'.format(x)])
        atrilPC[x].setLetra(datos['atrilPC']['{}'.format(x)])
    listaConfiguracion = datos['listaConfiguracion']
    puntosPC = datos['puntosPC']
    puntosPJ = datos['puntosPJ']
    window['contadorPuntosPJ'].update(puntosPJ)
    window['contadorPuntosPC'].update(puntosPC)
def asignarPuntajesTablero(listaConfiguracion):
    '''asigna un tipo especifico a cada boton del tablero'''
    if (listaConfiguracion['TipoTablero']==1):
        for i in range(15):
            for j in range(15):
                if(i+j==14)|(i==j): #DIAGONAL
                    TableroLetras[i][j].tipoCelda(1)
                if(((i==0) &((j+1)%4==0))|((j==0) &((i+1)%4==0))|((i==14) &((j+1)%4==0))|((j==14) &((i+1)%4==0))|(((i+1)%4==0)&((j+1)%4==0))):
                    TableroLetras[i][j].tipoCelda(2) #medio
                if(((i==0) &((j+1)%8==0))|((j==0) &((i+1)%8==0))|((i==14) &((j+1)%8==0))|((j==14) &((i+1)%8==0))|(((i+1)%8==0)&((j+1)%8==0))):
                    TableroLetras[i][j].tipoCelda(3) #extremos
                if(i==7)&(j==7):
                    TableroLetras[i][j].tipoCelda(4)
    elif(listaConfiguracion['TipoTablero']==2):
        for i in range(15):
            for j in range(15):
                if(i+j==14)|(i==j):
                    TableroLetras[i][j].tipoCelda(2)
                if(((i==0) &((j+1)%4==0))|((j==0) &((i+1)%4==0))|((i==14) &((j+1)%4==0))|((j==14) &((i+1)%4==0))|(((i+1)%4==0)&((j+1)%4==0))):
                    TableroLetras[i][j].tipoCelda(1)
                if(((i==0) &((j+1)%8==0))|((j==0) &((i+1)%8==0))|((i==14) &((j+1)%8==0))|((j==14) &((i+1)%8==0))|(((i+1)%8==0)&((j+1)%8==0))):
                    TableroLetras[i][j].tipoCelda(3)
                if(i==7)&(j==7):
                    TableroLetras[i][j].tipoCelda(4)
    elif(listaConfiguracion['TipoTablero']==3):
        for i in range(15):
            for j in range(15):
                if(i+j==14)|(i==j):
                    TableroLetras[i][j].tipoCelda(3)
                if(((i==0) &((j+1)%4==0))|((j==0) &((i+1)%4==0))|((i==14) &((j+1)%4==0))|((j==14) &((i+1)%4==0))|(((i+1)%4==0)&((j+1)%4==0))):
                    TableroLetras[i][j].tipoCelda(2)
                if(((i==0) &((j+1)%8==0))|((j==0) &((i+1)%8==0))|((i==14) &((j+1)%8==0))|((j==14) &((i+1)%8==0))|(((i+1)%8==0)&((j+1)%8==0))):
                    TableroLetras[i][j].tipoCelda(1)
                if(i==7)&(j==7):
                    TableroLetras[i][j].tipoCelda(4)
def repartirFichas(bolsa_letras,atril):
    '''reparte fichas de la bolsa de letras por cada boton vacio en el atril del jugador o de la pc'''
    for i in range(7):
        if(atril[i].getLetra() == 'nulo'):
            letra = random.choice(string.ascii_letters).lower()
            while(bolsa_letras[letra] == 0):
                letra = random.choice(string.ascii_letters).lower()
            atril[i].setLetra(letra)

#ventanas emergentes
def ventana_salir(ventana,tablero,atrilPJ,atrilPC,listaConfiguracion,puntosPJ,puntosPC):
    '''bloquea el juego y depues confirma si el juegador quiere salir'''
    bloqueos.bloquearJuego(ventana,tablero,atrilPJ)
    layout = [
        [sg.Text('¿quiere guardar la partida?',pad=(0,10),font=("Arial", 14),justification='center',size=(24,0))],
        [sg.Button('SI',size= (9,2)),sg.Button('NO',size= (9,2)),sg.Button('Cancelar',size= (9,2))]
    ]
    window = sg.Window('', layout,)
    event , values = window.read()
    while  True:
        if event == 'SI':
            window.close()
            guardarPartida(tablero,atrilPJ,atrilPC,listaConfiguracion,puntosPJ,puntosPC)
            bloqueos.desbloquearJuego(ventana,tablero,atrilPJ)
            return True
        if event == 'NO':
            window.close()
            bloqueos.desbloquearJuego(ventana,tablero,atrilPJ)
            return True
        if event == 'Cancelar':
            window.close()
            bloqueos.desbloquearJuego(ventana,tablero,atrilPJ)
            return False
def ventana_comenzar(ventana,tablero,atrilPJ,atrilPC,listaConfiguracion,puntosPJ,puntosPC):
    '''bloquea el juego y depues confirma si el juegador quiere salir'''
    bloqueos.bloquearJuego(ventana,tablero,atrilPJ)
    layout = [
        [sg.Text('¿Quiere seguir con la partida guardada?',pad=(0,10),font=("Arial", 14))],
        [sg.Button('SI',size= (9,2),pad=(10,2)),sg.Button('NO',size= (9,2),pad=(10,2))]
    ]
    window = sg.Window('', layout,size=(360,100))
    event , values = window.read()
    try:
        while  True:
                if event == 'SI':
                        window.close()
                        abrirPartida(ventana,tablero,atrilPJ,atrilPC,listaConfiguracion,puntosPJ,puntosPC)
                        bloqueos.desbloquearJuego(ventana,tablero,atrilPJ)
                        ventana['Comenzar'].update(disabled=True)
                        ventana['Pasar'].update(disabled=False)
                        ventana['Confirmar'].update(disabled=False)
                        ventana['Cambiar'].update(disabled=False)
                        bloqueos.desbloquearAtril(AtrilLetras)
                        bloqueos.bloquearTablero(TableroLetras)
                        return True
                else:
                    repartirFichas(listaConfiguracion['CantidadLetras'],atrilPJ)
                    repartirFichas(listaConfiguracion['CantidadLetras'],atrilPC)
                    asignarPuntajesTablero(listaConfiguracion)
                    window.close()
                    bloqueos.desbloquearJuego(ventana,tablero,atrilPJ)
                    ventana['Comenzar'].update(disabled=True)
                    ventana['Pasar'].update(disabled=False)
                    ventana['Confirmar'].update(disabled=False)
                    ventana['Cambiar'].update(disabled=False)
                    bloqueos.desbloquearAtril(AtrilLetras)
                    bloqueos.bloquearTablero(TableroLetras)
                    return  True
    except FileNotFoundError:
        ventana_error_archivo()
def ventana_error_archivo():
    '''
    indica que el archivo que se busca no existe en la ubicacion seleccionada
    '''
    layout = [[sg.Text('No existen partidas guardadas',)],
              [sg.OK(size=(10,2))]
              ]
    window = sg.Window('ERROR', layout)
    event, values = window.read()
    window.close()
def informarGanador(puntosPJ,puntosPC):
    '''
    indica que finalizo la partida y da un ganador
    '''
    if(puntosPC<puntosPJ):
        resultado = 'GANASTE'
    else:
        resultado = 'PERDISTE'

    layout = [
        [sg.Text(resultado,font=("Arial", 20),size=(200,1))],
        [sg.Text('{} a {}'.format(puntosPJ,puntosPC),font=("Arial", 15),size=(200,1))],
        [sg.OK(size=(10,2),pad=(50,4))]
              ]
    window = sg.Window('', layout,size=(200,120),text_justification='center')
    event, values = window.read()

    window.close()

#fin de la Partida
def guardarPuntaje(listaConfiguracion,puntaje,ruta):
    '''guarda la fecha, el puntaje y el nivel de dificultad en un archivo'''
    with open(ruta,'r+') as file:
        json_data = json.load(file)
        fecha = datetime.now()  # Obtiene fecha y hora actual
        fecha = "{} de {} del {}".format(fecha.day, fecha.month, fecha.year)
        valores={"fecha": fecha, "puntaje":puntaje, "nivel": listaConfiguracion['Nivel']}
        json_data[listaConfiguracion['Nivel']].append(valores)
        file.seek(0)
        file.write(json.dumps(json_data))
        file.truncate()
def guardarPartida(tablero,atrilPJ,atrilPC,listaConfiguracion,puntosPJ,puntosPC):
    '''recibe el tablero de juego, el atril del jugador, el de la PC y la cantidad de letras existentes y guarda toda esa informacion en un .json '''
    datos = {}
    datoTablero={}
    tipoTablero={}
    estadoTablero={}
    datoPJ={}
    datoPC={}
    for x in range(15):
        for y in range(15):
            datoTablero['{},{}'.format(x,y)] = tablero[x][y].getLetra()
            tipoTablero['{},{}'.format(x,y)]=tablero[x][y].getTipo()
            estadoTablero['{},{}'.format(x,y)]=tablero[x][y].getEstado()
    for x in range (7):
        datoPJ['{}'.format(x)]=atrilPJ[x].getLetra()
        datoPC['{}'.format(x)]=atrilPC[x].getLetra()
    datos['tablero']=datoTablero
    datos['tipoTablero']=tipoTablero
    datos['estadoTablero']=estadoTablero
    datos['atrilPJ']=datoPJ
    datos['atrilPC']=datoPC
    datos['listaConfiguracion']=listaConfiguracion
    datos['puntosPJ'] = puntosPJ
    datos['puntosPC'] = puntosPC
    try:
        with open('partidaGuardada.json','r+') as file:
            file.write(json.dumps(datos))
            file.truncate()
    except FileNotFoundError:
        with open('partidaGuardada.json','w') as file:
            file.write(json.dumps(datos))
            file.truncate()
def finalPartida(atrilPJ,atrilPC,puntosPJ,puntosPC,listaConfiguracion):
    for x in range(7):
        letraPC = atrilPC[x].getLetra()
        letraPJ= atrilPJ[x].getLetra()
        if(letraPC != 'nulo'):
            puntosPC = puntosPC - listaConfiguracion['PuntajeLetra'][letraPC]
        if(letraPJ != 'nulo'):
            puntosPJ = puntosPJ - listaConfiguracion['PuntajeLetra'][letraPJ]
    informarGanador(puntosPJ,puntosPC)
    guardarPuntaje(listaConfiguracion,puntosPJ,'archivoPuntajes.json')

#turno del jugador
def formarListaPalabra(listaLetras):
    '''
    recibe la lista de las posciones donde se colocaron las letrasPuntos
    devulve una lista con las posiciones de las letras consecutivas
    '''
    palabraH = []
    palabraV = []
    x=int(listaLetras[0][0])
    y=int(listaLetras[0][1])
    palabraH.append((x,y))
    palabraV.append((x,y))
    for i in listaLetras:
        if(i[0] == x+1):
            x=int(i[0])
            y=int(i[1])
            palabraH.append((x,y))
        if(i[1] == y+1):
            x=int(i[0])
            y=int(i[1])
            palabraV.append((x,y))
    if(len(palabraH)>len(palabraV)):
        palabraV.pop(0)
        borrarPalabras(palabraV)
        return palabraH
    else:
        palabraH.pop(0)
        borrarPalabras(palabraH)
        return palabraV
def confirmarPalabra(Lpalabra,tipoPalabra):
    '''
    recibe una palabra y confirma si es un sustantivo (/NM), un vervo (/VB), un adjetivo(/JJ) o un pronombre (/PRS)
    '''
    aux = []
    for i in Lpalabra:
        aux.append(TableroLetras[i[0]][i[1]].getLetra())
    palabra = ''.join(aux)
    if(len(palabra)>1):
        if palabra in pattern.es.lexicon:
            if palabra in pattern.es.spelling:
                dato = parse(palabra,tokenize = True,tags = True,chunks = False).replace(palabra,'')
                if(dato in tipoPalabra):
                    return True
        else:
            return False
    else:
        return False
def borrarPalabras(listaLetras):
    '''devuelvo las letras usasas al atril y borro todas las letras que se pusieron en el tablero'''
    x = 0
    for i in listaLetras:
        letra = TableroLetras[i[0]][i[1]].getLetra()
        TableroLetras[i[0]][i[1]].setLetra('nulo')
        TableroLetras[i[0]][i[1]].setEstado(0)
        TableroLetras[i[0]][i[1]].tipoCelda(TableroLetras[i[0]][i[1]].getTipo()) #devuelvo la imagen que tenia

        ok = True
        while(ok) & (x<7):
            if(AtrilLetras[x].getLetra() == 'nulo'):
                AtrilLetras[x].setLetra(letra)
                ok= False
            x = x + 1
def cambioMano(atrilPJ,listaConfiguracion):
    '''Cambia la mano del jugador'''
    AtrilCambiar = [0 for x in range(7)] #atril de 7 elementos
    Atril = [botonesAtril(listaConfiguracion['Nivel'],x,AtrilCambiar) for x in range(7)] #creo en cada elemento del atril un boton

    layout2 = [
    [sg.Text('seleccione las letras que desea cambiar')],
    [sg.Column([Atril])],
    [sg.Button('Confirmar',size= (15,1)),sg.Button('Cancelar',size= (15,1))],
    ]


    window = sg.Window('', layout2,font=("Arial", 12))

    while True:
        event, values = window.read(timeout=10)
        for i in range(7):
            AtrilCambiar[i].setLetra(atrilPJ[i].getLetra())
    window.close()
def sumarPuntos(Lpalabra,valorLetras):
    '''
    recibe una lista con la posicion de las letras que forman la palabra que se ingreso,
    calcula el puntaje de la palabra ingresada y lo multiplica por los cosito de colores (no me sale la palabra)
    tipo 0: nada
    tipo 1: palabra x2
    tipo 2: letras x2
    tipo 3: resto la letra
    '''
    suma = 0
    aux = 1

    for i in Lpalabra:
        print(i)
        letra = TableroLetras[i[0]][i[1]].getLetra()
        tipo =  TableroLetras[i[0]][i[1]].getTipo()
        if(letra != 'nulo'):
            if(tipo == 0):
                suma = suma + valorLetras[letra]
            elif(tipo == 4):
                suma = suma + valorLetras[letra]
            elif(tipo ==1):
                suma = suma + valorLetras[letra]
                aux = aux +1
            elif(tipo == 2):
                suma = suma + valorLetras[letra]*2
            elif(tipo == 3):
                suma = suma - valorLetras[letra]
    return (suma * aux)

def main(listaConfiguracion=listaPorDefecto):
    #Interface grafica
    Atril = [botonesAtril(listaConfiguracion['Nivel'],x,AtrilLetras)for x in range(7)]  #creo el atril de 7 botones
    AtrilPC = [botonesAtrilPC(listaConfiguracion['Nivel'],x)for x in range(7)] #creo el atril de 7 botones para la PC
    Tablero = [[botonTablero(listaConfiguracion['Nivel'],x,y) for x in range(15)] for y in range(15)] #creo el el trablero de 15x15 botones
    botonesTurno= [
    [sg.Button('Confirmar',tooltip='Probar si la plabra es correcta',disabled=True,size= (12,2)),
    sg.Button('Cambiar',tooltip='cambiar Fichas',disabled=True,size= (12,2)),
    sg.Button('Pasar',tooltip='Pasar turno',disabled=True,size= (12,2))],
    ]
    #Contiene el tablero de juego y atril con las fichas de la mano
    columna1 = [
    [sg.Text('ATRIL Computadora',size=(30,1),font=("Arial", 15))],
    [sg.Column([AtrilPC])],
    [sg.Column(Tablero)],
    [sg.Text('ATRIL Jugador',size=(30,1),font=("Arial", 15))],
    [sg.Column([Atril]), sg.Column(botonesTurno)],
    ]
    columnapuntosPJ=[
    [sg.Text('JUGADOR', size=(10,1),font=("Arial", 12,'bold'))],
    [sg.Text('---',key ='contadorPuntosPJ', size=(10,1))]
    ]
    columnapuntosPC=[
    [sg.Text('PC', size=(10,1),font=("Arial", 12,'bold'))],
    [sg.Text('---',key ='contadorPuntosPC', size=(10,1))]
    ]
    columnaPuntaje=[

    [sg.Column(columnapuntosPJ),sg.Column(columnapuntosPC)],

    ]
    columnaTiempo=[
    [sg.Text('Tiempo Partida ',size=(13,1),font=("Arial", 12,'bold')),sg.Text(key='timerPartida',size=(7,1),),],
    [sg.Text('TURNO',size=(6,1),font=("Arial", 12,'bold')),sg.Text('--',key='contTurno', justification='left',size=(6,1),font=("Arial", 12,'bold')),sg.Text(key='timerTurno',size=(7,1))],
    ]
    #contiene los puntajes y el tiempo que resta del turno
    columna2= [
    [sg.Column(columnaPuntaje,)],
    [sg.Column(columnaTiempo,)],
    [sg.Text('¿Que fue pasando?',font=("Arial", 12,'bold'))],
    [sg.Listbox('',size =(23,12),key='acciones')],
    [sg.Button('Comenzar',auto_size_button=False,tooltip='Comenzar Partida',size= (24,2))],
    [sg.Button('Guardar',auto_size_button=False,tooltip='Guarda la partida',size= (24,2),disabled = False)],
    [sg.Button('Salir',auto_size_button=False,tooltip='Salir al menu',size= (24,2))],
    ]
    cordAtril = ['(0, 0)7','(1, 0)8','(2, 0)9','(3, 0)10','(4, 0)11','(5, 0)12','(6, 0)13'] #no se me ocurrio una forma mejor, las cordenasd de las letras se guardan de una forma extraña
    cordTablero = [(a,b) for a in range(0,15) for b in range(0,15)]
    #Programa

    layout  = [
        [sg.Image(filename='imagenes/logo.png',background_color='#abbccf',size= (960,50))],
        [sg.Column(columna1),sg.Column(columna2)],
    ]
    window = sg.Window('', layout,font=("Arial", 12))
    puntosPJ = 0
    puntosPC = 0
    cont_turno = 1
    listaPoiciones = [] #lista de las letras q se van a poner en el tablero
    turno = True #turno del juegador
    contadorTiempoTurno = 0 #mide el tiempo del turno
    contadorTiempoPartida = 0 #mide el tiempo de la partida
    comenzar = False #camienza el jeugo apretando comenzar
    intentosCambio = 0 #cantidad de cambios que le quedan al jugador
    listaAcciones = [] #carga las distintas acciones que pasan cada turno

    while True:
        if((contadorTiempoPartida==(6000*listaConfiguracion['TiempoPartida'])) | (sum(listaConfiguracion['CantidadLetras'].values()) <8)): #si llega el tiempo final o quedan menos de 8 letras termina la partida
            finalPartida(AtrilLetras,AtrilLetrasPC,puntosPJ,puntosPC,listaConfiguracion)
            break

        event, values = window.read(timeout=10)
        #Contador tiempo
        window['timerTurno'].update(
        '{:02d}:{:02d}.{:02d}'.format((contadorTiempoTurno // 100) // 60, (contadorTiempoTurno // 100) % 60, contadorTiempoTurno % 100))
        window['timerPartida'].update(
        '{:02d}:{:02d}.{:02d}'.format((contadorTiempoPartida // 100) // 60, (contadorTiempoPartida // 100) % 60, contadorTiempoPartida % 100))
        if(comenzar):
            contadorTiempoTurno = contadorTiempoTurno +1
            contadorTiempoPartida = contadorTiempoPartida +1
        if event is None or event == 'Salir':
            if(ventana_salir(window,TableroLetras,AtrilLetras,AtrilLetrasPC,listaConfiguracion,puntosPJ,puntosPC)):
                finalPartida(AtrilLetras,AtrilLetrasPC,puntosPJ,puntosPC,listaConfiguracion)
                guardarPuntaje(listaConfiguracion,puntosPJ,'archivoPuntajes.json')
                break
        #TURNO DEl JUGADOR
        if event is 'Comenzar':
            comenzar = ventana_comenzar(window,TableroLetras,AtrilLetras,AtrilLetrasPC,listaConfiguracion,puntosPJ,puntosPC)
            window['contTurno'].update(cont_turno)
            turno = random.choice([True,False])
        if event in ['Confirmar','Cambiar','Pasar','Comenzar','Guardar']:
            #BOTON CONFIRMAR
            if (event is 'Confirmar') &(len(listaPoiciones)>0): #si se preciona el boton confirmar y se pusieron fichas en el tablero
                if(confirmarPalabra(formarListaPalabra(listaPoiciones),listaConfiguracion['TipoPalabra'])):
                    puntos = sumarPuntos(formarListaPalabra(listaPoiciones),listaConfiguracion['PuntajeLetra'])
                    puntosPJ =puntosPJ + puntos
                    window['contadorPuntosPJ'].update(puntosPJ)
                    listaAcciones.append('----------------------------------')
                    listaAcciones.append('y sumaste {} puntos'.format(puntos))
                    listaAcciones.append('CORRECTO  ')
                    window['acciones'].update(listaAcciones[::-1])
                    del listaPoiciones[:]
                    turno = False
                else:
                    borrarPalabras(listaPoiciones)
                    listaAcciones.append('----------------------------------')
                    listaAcciones.append('Esa palabra no cuenta')
                    window['acciones'].update(listaAcciones[::-1])
                    del listaPoiciones[:] #vacio la lista con las letras que se usaron
            #BOTON PASAR
            if (event is 'Pasar'):
                if(len(listaPoiciones)==0):  #si se preciona el boton confirmar y no se pusieron fichas en el tablero
                    turno = False
                    del listaPoiciones[:]
                else:
                    listaAcciones.append('----------------------------------')
                    listaAcciones.append('Todavia quedan letras en el tablero ' )
                    window['acciones'].update(listaAcciones[::-1])
            #BOTON CAMBIAR
            if event is 'Cambiar':
                if (intentosCambio <3):
                    if(len(listaPoiciones)==0):
                        bloqueos.bloquearJuego(window,TableroLetras,AtrilLetras)
                        letrasCambio = cambiarLetras.main(AtrilLetras,listaConfiguracion)
                        if (letrasCambio):
                            intentosCambio =intentosCambio+1
                            for i in letrasCambio:
                                AtrilLetras[i].vaciar()
                                listaConfiguracion['CantidadLetras'][AtrilLetras[i].getLetra()] =+1
                            repartirFichas(listaConfiguracion['CantidadLetras'],AtrilLetras)
                            turno = False
                            bloqueos.desbloquearJuego(window,TableroLetras,AtrilLetras)
                        else:
                            bloqueos.desbloquearJuego(window,TableroLetras,AtrilLetras)
                            bloqueos.bloquearTablero(TableroLetras)

                    else:
                        listaAcciones.append('----------------------------------')
                        listaAcciones.append('Todavia quedan letras en el tablero ' )
                        window['acciones'].update(listaAcciones[::-1])
                else:
                    window['Cambiar'].update(disabled=True)
            if (event is 'Guardar'):
                guardarPartida(TableroLetras,AtrilLetras,AtrilLetrasPC,listaConfiguracion,puntosPJ,puntosPC)
        #se preciona algun boton en el atril
        elif event in cordAtril:  #se preciona algun boton en el atril
            letraAtril = event
            letra = AtrilLetras[int(letraAtril[1])].getLetra()
            if(TableroLetras[7][7].getEstado() == 1):
                bloqueos.desbloquerTablero(TableroLetras)
            else:
                TableroLetras[7][7].desbloquear()

        #se precion algun boton en el tablero
        elif event in cordTablero:
            cord = event

            #reviso si el tablero esta vacion en esa posicion
            if(TableroLetras[cord[0]][cord[1]].getLetra()in['nulo','restaletra','letrax2','palabrax2','centro']):
                TableroLetras[cord[0]][cord[1]].setLetra(letra) #asigno la letra a la posicion
                AtrilLetras[int(letraAtril[1])].vaciar()  #elimino esa ficha del atril
                listaPoiciones.append(cord)
            bloqueos.bloquearTablero(TableroLetras)

        #TURNO DE LA PC
        if (not turno) or (contadorTiempoTurno == (100*listaConfiguracion['TiempoTurno'])):
            bloqueos.bloquearJuego(window,TableroLetras,AtrilLetras)
            repartirFichas(listaConfiguracion['CantidadLetras'],AtrilLetrasPC)
            repartirFichas(listaConfiguracion['CantidadLetras'],AtrilLetras)
            if listaPoiciones: #si todavia quedan letras en el tablero que no son una palabra
                borrarPalabras(listaPoiciones)
                del listaPoiciones[:]


            contadorTiempoTurno = 0
            lPalabra =[]
            palabra = turnoPC.crearPalabra(AtrilLetrasPC,listaConfiguracion,listaAcciones,window)

            if (palabra !=None):
                puntos = sumarPuntos(turnoPC.colocaPalabra(palabra,TableroLetras),listaConfiguracion['PuntajeLetra'])
                puntosPC =puntosPC + puntos
                listaAcciones.append('----------------------------------')
                listaAcciones.append('La PC sumo {} puntos'.format(puntos))
                listaAcciones.append('La PC encontro "{}"'.format(palabra))
                window['acciones'].update(listaAcciones[::-1])
                window['contadorPuntosPC'].update(puntosPC)
                turnoPC.elimiarLetrasAtril(palabra,AtrilLetrasPC)

            turno = True
            window['contTurno'].update(cont_turno)
            cont_turno +=1;

            bloqueos.desbloquearJuego(window,TableroLetras,AtrilLetras)
            bloqueos.bloquearTablero(TableroLetras)

    window.close()
if __name__ == '__main__':
    main()
