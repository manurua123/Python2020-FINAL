#liberias
import PySimpleGUI as sg
import random
import string

from pattern.es import parse
import time
from datetime import datetime, date, time, timedelta
import json
from itertools import permutations
from time import sleep

#otros archivos.py
import generarPalabra
import test
import cambiarLetras


#configurtacion de colores
sg.SetOptions(background_color='#222831',
       text_element_background_color='#222831',
       element_background_color='#9FB8AD',
       button_color=('#222831','#00adb5'),
       text_justification='center',
       border_width=1,
       )
#valores para testear
listaPorDefecto={'PuntajeLetra':{'a':1,'b':3,'c':2,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':6,'k':8,'l':1,'m':3,'n':1,'o':1,'p':3,'q':8,'r':1,'s':1,'t':1,'u':1,'v':4,'w':8,'x':8,'y':4,'z':10},
'CantidadLetras':{'a':11,'b':3,'c':4,'d':4,'e':11,'f':2,'g':2,'h':0,'i':6,'j':2,'k':0,'l':4,'m':3,'n':5,'o':8,'p':2,'q':0,'r':4,'s':5,'t':4,'u':6,'v':0,'w':0,'x':0,'y':0,'z':0},
'TipoPalabra':['/WP','/AO', '/JJ', '/AQ', '/DI', '/DT','/VAG', '/VBG', '/VAI', '/VAN', '/MD', '/VAS', '/VMG', '/VMI', '/VB', '/VMM', '/VMN', '/VMP', '/VBN', '/VMS', '/VSG', '/VSI', '/VSN', '/VSP', '/VSS'],
'TiempoTurno': 30,
'TiempoPartida':10,
'TipoTablero':1,
'Nivel': 'medio'}
#clases de los botones, tablero, atril pc y atril jugador
class BotonLetra():
    def __init__ (self,x,y=0):
        self.valor= ' '
        self.x = x
        self.y = y
        self.estado = 0    #0 si esta libre o 1 si esta ocupado
        self.bloqueo = True  #bloquea el boton para evitar bugs
        self.key = (x,y)
        self.boton  = sg.Button(self.valor,size= (4,2),key = self.key,disabled=self.bloqueo,pad=(1,1), button_color=('#222831','#e0dede'),)
        self.tipo = 0
    def update(self):
        self.boton.update(self.valor,disabled=self.bloqueo)
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
        self.valor = ' '
        self.estado = 0
        self.update()
    def getEstado(self):
        return self.estado
    def getTipo(self):
        return self.tipo
    def marcar(self):
        self.estado = 0
        self.bloqueo = True
        self.boton.update(self.valor,disabled=self.bloqueo,button_color=('#222831','#f6d743'))
        return self.valor
class BotonAtril(BotonLetra):
    def __init__ (self,x):
        BotonLetra.__init__ (self,x)
class BotonTablero(BotonLetra):
    def __init__ (self,x,y):
        BotonLetra.__init__ (self,x,y)
    def tipoCelda(self,valor):
        '''
        actualiza el color y el tipo de boton segun los multiplicadores que tenga
        '''
        if(valor == 0):
            self.tipo=valor
            #self.valor='X'
            self.boton.update(self.valor,button_color=('black','#fbfd8a')) #centro
        if (valor ==1):
            self.tipo=valor
            #self.valor='Pala\nx2'
            self.boton.update(self.valor,button_color=('black','#21bf73')) #PALABRA x2
        if(valor== 2):
            self.tipo=valor
            #self.valor='Letra\nx2'
            self.boton.update(self.valor,button_color=('black','#4f98ca')) #LETRAS x2
        if(valor== 3):
            self.tipo=valor
            #self.valor='Pala\n x3'
            self.boton.update(self.valor,button_color=('black','#fd5e53')) #Resta Letra
        else:
            None
class BotonesAtrilPC():
    def __init__ (self,x):
        self.valor= ' '
        self.x = x
        self.estado = 0    #0 si esta libre o 1 si esta ocupado
        self.bloqueo = True  #bloquea el boton para evitar bugs
        self.key = (x,0)
        self.boton  = sg.Button(' ',size= (4,2),key = self.key,disabled=self.bloqueo,pad=(1,1), button_color=('#222831','#e0dede'))
        self.tipo = 0
    def update(self):
        self.boton.update(self.valor)
    def getLetra(self):
        return self.valor
    def setLetra(self,v):
        self.valor = v
        self.estado = 1
    def getEstado(self):
        return self.estado
    def vaciar(self):
        self.valor = ' '
        self.estado = 0
        self.update()

#Atril del la maquina, del jugador y el tablero de juego
AtrilLetrasPC = [0 for y in range(7)]                                             #creo una lista de vacia con 7 lugares [0,0,0,0,0,0,0,0]
def botonesAtrilPC(x):
    '''genera un boton en la cordenada x'''
    AtrilLetrasPC[x] =  BotonesAtrilPC(x)
    return AtrilLetrasPC[x].boton
AtrilLetras = [0 for y in range(7)]                                             #creo una lista de vacia con 7 lugares [0,0,0,0,0,0,0,0]
def botonesAtril(x,atril):
    '''genera un boton en la pocicion x del atril'''
    atril[x] = BotonAtril(x)
    return atril[x].boton
TableroLetras = [[' ' for a in range(0,15)] for b in range(0,15)]               #creo una matriz de 15x15 vacia
def botonTablero(x,y):
    '''genera un boton en las cordenadas (x,y)'''
    TableroLetras[x][y] = BotonTablero(x,y)
    return TableroLetras[x][y].boton

#bloqueo tablero, atril o el juego para evitar bugs
def bloquearTablero():
    '''bloque los botones del tablero de juego'''
    for x in range(15):
        for y in range(15):
            TableroLetras[x][y].bloquear()
def desbloquerTablero():
    '''desbloque los botones del tablero de juego'''
    for x in range(15):
        for y in range(15):
            TableroLetras[x][y].desbloquear()
def bloquearAtril():
    '''bloque los botones del atril del jugador'''
    for x in range(7):
        AtrilLetras[x].bloquear()
def desbloquearAtril():
    '''desbloquea los botones del atril del jugador'''
    for x in range(7):
        AtrilLetras[x].desbloquear()
def bloquearJuego(window):
    '''bloque TODOS los botones de la pantalla'''
    bloquearAtril()
    bloquearTablero()
    window['Pasar'].update(disabled=True)
    window['Confirmar'].update(disabled=True)
    window['Cambiar'].update(disabled=True)
def desbloquearJuego(window):
    '''desbloquea TODOS los botones de la pantalla'''
    desbloquearAtril()
    desbloquerTablero()
    window['Pasar'].update(disabled=False)
    window['Confirmar'].update(disabled=False)
    window['Cambiar'].update(disabled=False)

#inicil de la partida
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
                    TableroLetras[i][j].tipoCelda(0)
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
                    TableroLetras[i][j].tipoCelda(0)
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
                    TableroLetras[i][j].tipoCelda(0)
def repartirFichas(bolsa_letras,atril):
    '''reparte fichas de la bolsa de letras por cada boton vacio en el atril del jugador o de la pc'''
    for i in range(7):
        if(atril[i].getLetra() == ' '):
            letra = random.choice(string.ascii_letters).lower()
            while(bolsa_letras[letra] == 0):
                letra = random.choice(string.ascii_letters).lower()
            atril[i].setLetra(letra)
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
        letra = TableroLetras[i[0]][i[1]].getLetra()
        tipo =  TableroLetras[i[0]][i[1]].getTipo()
        if(tipo == 0):
            suma = suma + valorLetras[letra]
        elif(tipo ==1):
            suma = suma + valorLetras[letra]
            aux = aux +1
        elif(tipo == 2):
            suma = suma + valorLetras[letra]*2
        elif(tipo == 3):
            suma = suma - valorLetras[letra]
    return (suma * aux)
def ventana_salir(ventana):
    '''bloquea el juego y depues confirma si el juegador quiere salir'''
    bloquearJuego(ventana)
    layout = [
        [sg.Text('¿Seguro que desea salir?')],
        [sg.Button('SI',size= (5,1)),sg.Button('NO',size= (5,1))]
    ]
    window = sg.Window('', layout,font=("Helvetica", 12))
    event , values = window.read()
    while  True:
        if event == 'SI':
            window.close()
            desbloquearJuego(ventana)
            return True
        else:
            window.close()
            desbloquearJuego(ventana)
            return False

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

#turno del jugador
def formarListaPalabra(listaLetras):
    '''
    recibe la lista de las posciones donde se colocaron las letrasPuntos
    devulve una lista con las posiciones de las letras consecutivas
    '''
    palabra = []
    x=int(listaLetras[0][0])
    y=int(listaLetras[0][1])
    palabra.append((x,y))
    for i in listaLetras:
        if(i[0] == x+1):
            x=int(i[0])
            y=int(i[1])
            palabra.append((x,y))
    return(palabra)
def confirmarPalabra(Lpalabra,tipoPalabra):
    '''
    recibe una palabra y confirma si es un sustantivo (/NM), un vervo (/VB), un adjetivo(/JJ) o un pronombre (/PRS)
    '''
    aux = []
    for i in Lpalabra:
        aux.append(TableroLetras[i[0]][i[1]].getLetra())
    palabra = ''.join(aux)
    if(len(palabra)>1):
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
        TableroLetras[i[0]][i[1]].setLetra(' ')
        ok = True
        while(ok) & (x<7):
            if(AtrilLetras[x].getLetra() == ' '):
                AtrilLetras[x].setLetra(letra)
                ok= False
            x = x + 1
def cambioMano(atrilPJ):
    '''Cambia la mano del jugador'''
    AtrilCambiar = [0 for x in range(7)] #atril de 7 elementos
    Atril = [botonesAtril(x,AtrilCambiar) for x in range(7)] #creo en cada elemento del atril un boton

    layout2 = [
    [sg.Text('seleccione las letras que decea cambiar')],
    [sg.Column([Atril])],
    [sg.Button('Confirmar',size= (15,1)),sg.Button('Cancelar',size= (15,1))],
    ]


    window = sg.Window('', layout2,font=("Helvetica", 12))

    while True:
        event, values = window.read(timeout=10)
        for i in range(7):
            AtrilCambiar[i].setLetra(atrilPJ[i].getLetra())
    window.close()

#turno de la PC
def crearPalabra(Atril,listaConfiguracion):
    '''crea una palabra con las letras que se pusieron en el tablero'''
    mano = []
    palabra = ''
    for i in range(7):
        mano.append(Atril[i].getLetra())
    palabra = generarPalabra.main(mano,listaConfiguracion['TipoPalabra'])
    if(palabra != None):
        return palabra
def intentoColocarPalabra(palabra):
    '''la pc intenta colocar la palabra que formo en una ubicacion random dentro del tablero'''
    x = random.randrange(14)
    if(x + len(palabra)>=15): #evita elegir una cordenada que exeda el tablero
        x=x-len(palabra)
    y = random.randrange(14)
    vacio = True
    cant = 0
    Lpalabra =[]

    while (vacio) & (cant<len(palabra)):
        if(TableroLetras[x][y].getEstado()==0):
            Lpalabra.append((x,y))
        else:
            vacio = False
        x = x +1
        cant = cant + 1
    if vacio:
        return (True,Lpalabra)
    else:

        return (False,None)
def colocaPalabra(palabra):
    '''la pc coloca la palabra en una ubicacion random permitida dentro del tablero'''
    aux = intentoColocarPalabra(palabra)
    while( aux[0] == False):
        aux = intentoColocarPalabra(palabra)
    numero = 0
    while(numero < len(palabra)):
        i = aux[1][numero]
        TableroLetras[i[0]][i[1]].setLetra(palabra[numero])
        numero = numero +1
    return(aux[1])
def elimiarLetrasAtril(palabra,atril):
     mano = []
     for i in range(7):
         mano.append(atril[i].getLetra())
     for i in palabra:
         aux = 0
         while(mano[aux]!=i):
             aux = aux +1
         atril[aux].vaciar()



def main(listaConfiguracion=listaPorDefecto):

    #Interface grafica
    Atril = [botonesAtril(x,AtrilLetras)for x in range(7)]  #creo el atril de 7 botones
    AtrilPC = [botonesAtrilPC(x)for x in range(7)] #creo el atril de 7 botones para la PC
    Tablero = [[botonTablero(x,y) for x in range(15)] for y in range(15)] #creo el el trablero de 15x15 botones
    botonesTurno= [
    [sg.Button('Confirmar',tooltip='Probar si la plabra es correcta',disabled=True,size= (12,2)),
    sg.Button('Cambiar',tooltip='cambiar Fichas',disabled=True,size= (12,2)),
    sg.Button('Pasar',tooltip='Pasar turno',disabled=True,size= (12,2))],
    ]
    #Contiene el tablero de juego y atril con las fichas de la mano
    columna1 = [
    [sg.Text('ATRIL Computadora',size=(30,1),font=("Helvetica", 15))],
    [sg.Column([AtrilPC])],
    [sg.Column(Tablero)],
    [sg.Text('ATRIL Jugador',size=(30,1),font=("Helvetica", 15))],
    [sg.Column([Atril]), sg.Column(botonesTurno)],
    ]
    columnaPuntajePJ=[
    [sg.Text('Jugador', size=(10,1))],
    [sg.Text('---',key ='contadorPuntosPJ', size=(10,1))]
    ]
    columnaPuntajePC=[
    [sg.Text('Computadora', size=(10,1))],
    [sg.Text('---',key ='contadorPuntosPC', size=(10,1))]
    ]
    columnaPuntaje=[
    [sg.Column(columnaPuntajePJ),sg.Column(columnaPuntajePC)]
    ,

    ]
    columnaTiempo=[
    [sg.Text('Tiempo Partida ',size=(15,1)),sg.Text(key='timerPartida',size=(7,1)),],
    [sg.Text('TURNO',size=(10,1))],
    [sg.Text('---',key='contTurno')],
    [sg.Text('Tiempo Turno',size=(15,1)),sg.Text(key='timerTurno',size=(7,1)),],

    ]
    #contiene los puntajes y el tiempo que resta del turno
    columna2= [
    [sg.Column(columnaPuntaje,)],
    [sg.Column(columnaTiempo,)],
    [sg.Text('MULTIPLICADORES',size=(20,1))],
    [sg.Button(' ',size= (4,2),disabled=True,pad=(1,1), button_color=('#222831','#4f98ca')),sg.Text('Duplica el valor de la letra',)], #duplica Letra
    [sg.Button(' ',size= (4,2),disabled=True,pad=(1,1), button_color=('#222831','#21bf73')),sg.Text('Duplica el valor de la palabra',)], #duplica palabra
    [sg.Button(' ',size= (4,2),disabled=True,pad=(1,1), button_color=('#222831','#fd5e53')),sg.Text('Resta el valor de la letra',)], #resta letra
    [sg.Text('¿Que fue pasando?')],
    [sg.Listbox('',size =(30,12),key='acciones')],
    [sg.Button('Comenzar',auto_size_button=False,tooltip='Comenzar Partida',size= (20,2))],
    [sg.Button('Pausar',auto_size_button=False,tooltip='Falta Implementar',size= (20,2),disabled = True)],
    [sg.Button('Salir',auto_size_button=False,tooltip='salir al menu',size= (20,2))],


    ]

    cordAtril = ['(0, 0)7','(1, 0)8','(2, 0)9','(3, 0)10','(4, 0)11','(5, 0)12','(6, 0)13'] #no se me ocurrio una forma mejor, las cordenasd de las letras se guardan de una forma extraña
    cordTablero = [(a,b) for a in range(0,15) for b in range(0,15)]
    #Programa

    layout  = [
        [sg.Text('SCREBLE_AR',font=("Helvetica", 20,'bold'),size=(50,1))],
        [sg.Column(columna1),sg.Column(columna2)],
    ]
    window = sg.Window('', layout,font=("Helvetica", 12))
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
            if(ventana_salir(window)):
                guardarPuntaje(listaConfiguracion,puntosPJ,'archivoPuntajes.json')
                break
        #TURNO DEl JUGADOR
        window['contadorPuntosPJ'].update(puntosPJ)
        window['contadorPuntosPC'].update(puntosPC)
        if event is 'Comenzar':
            window['Comenzar'].update(disabled=True)
            window['Pasar'].update(disabled=False)
            window['Confirmar'].update(disabled=False)
            window['Cambiar'].update(disabled=False)
            desbloquearAtril()
            repartirFichas(listaConfiguracion['CantidadLetras'],AtrilLetras)
            asignarPuntajesTablero(listaConfiguracion)
            window['contTurno'].update(cont_turno)
            comenzar = True
        if event in ['Confirmar','Cambiar','Pasar','Comenzar','Pausar']:
            #BOTON CONFIRMAR
            if (event is 'Confirmar') &(len(listaPoiciones)>0): #si se preciona el boton confirmar y se pusieron fichas en el tablero
                if(confirmarPalabra(formarListaPalabra(listaPoiciones),listaConfiguracion['TipoPalabra'])):
                    puntos = sumarPuntos(formarListaPalabra(listaPoiciones),listaConfiguracion['PuntajeLetra'])
                    puntosPJ =puntosPJ + puntos
                    window['contadorPuntosPJ'].update(puntosPJ)
                    listaAcciones.append('CORRECTO \n y sumaste {} puntos'.format(puntos))
                    window['acciones'].update(listaAcciones[::-1])
                    del listaPoiciones[:]
                    turno = False
                else:
                    borrarPalabras(listaPoiciones)
                    listaAcciones.append('Esa palabra no cuenta')
                    window['acciones'].update(listaAcciones[::-1])
                    del listaPoiciones[:] #vacio la lista con las letras que se usaron
            #BOTON PASAR
            if (event is 'Pasar')&(len(listaPoiciones)==0) :  #si se preciona el boton confirmar y no se pusieron fichas en el tablero
                turno = False
                del listaPoiciones[:]
            #BOTON CAMBIAR
            if event is 'Cambiar':
                if (intentosCambio <3):
                    bloquearJuego(window)
                    letrasCambio = cambiarLetras.main(AtrilLetras)
                    if (letrasCambio):
                        intentosCambio =intentosCambio+1
                        for i in letrasCambio:
                            AtrilLetras[i].vaciar()
                            listaConfiguracion['CantidadLetras'][AtrilLetras[i].getLetra()] =+1
                    repartirFichas(listaConfiguracion['CantidadLetras'],AtrilLetras)
                    desbloquearJuego(window)

                else:
                    window['Cambiar'].update(disabled=True)
        #se preciona algun boton en el atril
        elif event in cordAtril:  #se preciona algun boton en el atril
            letraAtril = event
            letra = AtrilLetras[int(letraAtril[1])].getLetra()
            desbloquerTablero()
        #se precion algun boton en el tablero
        elif event in cordTablero:
            cord = event
            #reviso si el tablero esta vacion en esa posicion
            if(TableroLetras[cord[0]][cord[1]].getLetra()==' '):
                TableroLetras[cord[0]][cord[1]].setLetra(letra) #asigno la letra a la posicion
                AtrilLetras[int(letraAtril[1])].vaciar()  #elimino esa ficha del atril
                listaPoiciones.append(cord)
            bloquearTablero()

        #TURNO DE LA PC
        if (not turno) or (contadorTiempoTurno == (100*listaConfiguracion['TiempoTurno'])):
            bloquearJuego(window)
            if listaPoiciones: #si todavia quedan letras en el tablero que no son una palabra
                borrarPalabras(listaPoiciones)
                del listaPoiciones[:]
            repartirFichas(listaConfiguracion['CantidadLetras'],AtrilLetrasPC)
            contadorTiempoTurno = 0
            lPalabra =[]
            palabra = crearPalabra(AtrilLetrasPC,listaConfiguracion)
            if (palabra !=None):
                puntos = sumarPuntos(colocaPalabra(palabra),listaConfiguracion['PuntajeLetra'])
                puntosPC =puntosPC + puntos
                listaAcciones.append('La maquina encontro la plabra {}'.format(palabra))
                listaAcciones.append('La maquina sumo {} puntos'.format(puntos))
                window['acciones'].update(listaAcciones[::-1])
                window['contadorPuntosPC'].update(puntosPC)
                elimiarLetrasAtril(palabra,AtrilLetrasPC)
            repartirFichas(listaConfiguracion['CantidadLetras'],AtrilLetras)
            repartirFichas(listaConfiguracion['CantidadLetras'],AtrilLetrasPC)
            turno = True
            window['contTurno'].update(cont_turno)
            cont_turno +=1;
            sleep(1) #pasa de 3 seg porque sino va todo muy rapido
            desbloquearJuego(window)
            bloquearTablero()

    window.close()
if __name__ == '__main__':
    main()
