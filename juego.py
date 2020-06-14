import PySimpleGUI as sg
import random
import string
import pattern.es
from pattern.es import parse
import time
from threading import Timer
import sys


#configurtacion de colores
sg.SetOptions(background_color='#222831',
       text_element_background_color='#222831',
       element_background_color='#9FB8AD',
       button_color=('#222831','#00adb5'),
       text_justification='center',
       border_width=1,

       )
#valores para testear
listaPorDefecto={'PuntajeLetra':{'a':1,'b':3,'c':2,'d':2,'e':1,'f':4,'g':2,'h':10,'i':1,'j':6,'k':8,'l':1,'m':3,'n':1,'o':1,'p':3,'q':8,'r':1,'s':1,'t':1,'u':1,'v':4,'w':8,'x':8,'y':4,'z':10},'CantidadLetras':{'a':11,'b':3,'c':4,'d':4,'e':11,'f':2,'g':2,'h':0,'i':6,'j':0,'k':0,'l':4,'m':3,'n':5,'o':8,'p':0,'q':0,'r':0,'s':7,'t':4,'u':6,'v':0,'w':0,'x':0,'y':0,'z':0},'TipoPalabra':['/NM','/VB','/JJ'],'Tiempo': 60}
def repartirFichas(bolsa_letras):
    'reparte fichas de la bolsa de letras por cada boton vacio en el atril del jugador o de la pc'
    for i in range(7):
        if(AtrilLetras[i].getLetra() == ' '):
            letra = random.choice(string.ascii_letters).lower()
            while(bolsa_letras[letra] == 0):
                letra = random.choice(string.ascii_letters).lower()
            AtrilLetras[i].setLetra(letra)
class BotonLetra():
    def __init__ (self,x,y=0):
        self.valor= ' '
        self.x = x
        self.y = y
        self.estado = 0    #0 si esta libre o 1 si esta ocupado
        self.bloqueo = True  #bloquea el boton para evitar bugs
        self.key = (x,y)
        self.boton  = sg.Button(self.valor,size= (4,2),key = self.key,disabled=self.bloqueo,pad=(1,1), button_color=('#222831','#e0dede'))
        self.tipo = 0
    def update(self):
        self.boton .update(self.valor,disabled=self.bloqueo)
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
            self.boton.update(self.valor,button_color=('black','#ffcd3c')) #centro
        if (valor ==1):
            self.tipo=valor
            #self.valor='Pala\nx2'
            self.boton.update(self.valor,button_color=('black','#f07b3f')) #naranja
        if(valor== 2):
            self.tipo=valor
            #self.valor='Letra\nx2'
            self.boton.update(self.valor,button_color=('black','#1fab89')) #verde
        if(valor== 3):
            self.tipo=valor
            #self.valor='Pala\n x3'
            self.boton.update(self.valor,button_color=('black','#e84545')) #rojo
        else:
            None

AtrilLetras = [0 for y in range(7)]                                             #creo una lista de vacia con 7 lugares [0,0,0,0,0,0,0,0]
def botonesAtril(x):
    'genera un boton en la cordenada x'
    AtrilLetras[x] = BotonAtril(x)
    return AtrilLetras[x].boton
TableroLetras = [[' ' for a in range(0,15)] for b in range(0,15)]               #creo una matriz de 15x15 vacia
def botonTablero(x,y):
    'genera un boton en las cordenadas (x,y)'
    TableroLetras[x][y] = BotonTablero(x,y)
    return TableroLetras[x][y].boton
def asignarPuntajesTablero():
    'asigna un tipo especifico a cada boton del tablero'
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
def bloquearTablero():
    'bloque los botones del tablero de juego'
    for x in range(15):
        for y in range(15):
            TableroLetras[x][y].bloquear()
def desbloquerTablero():
    'desbloque los botones del tablero de juego'
    for x in range(15):
        for y in range(15):
            TableroLetras[x][y].desbloquear()
def bloquearAtril():
    'bloque los botones del atril'
    for x in range(7):
        AtrilLetras[x].bloquear()
def desbloquearAtril():
    'desbloquea los botones del atril'
    for x in range(7):
        AtrilLetras[x].desbloquear()
def bloquearJuego(window):
    bloquearAtril()
    bloquearTablero()
    window['Pasar'].update(disabled=True)
    window['Confirmar'].update(disabled=True)
    window['Cambiar'].update(disabled=True)
def desbloquearJuego(window):
    desbloquearAtril()
    desbloquerTablero()
    window['Pasar'].update(disabled=False)
    window['Confirmar'].update(disabled=False)
    window['Cambiar'].update(disabled=False)


def formarPalabra(listaLetras):
    '''
    recibe la lista de las posciones donde se colocaron las letrasPuntos
    devulve una plabra formada por las letras consecutivas horizontalmente
    '''
    palabra = []
    x=int(listaLetras[0][0])
    y=int(listaLetras[0][1])
    palabra.append(TableroLetras[x][y].getLetra())
    for i in listaLetras:
        if(i[0] == x+1):
            x=int(i[0])
            y=int(i[1])
            palabra.append(TableroLetras[x][y].getLetra())
    return(''.join(palabra))
def confirmarPalabra(palabra):
    '''
    recibe una palabra y confirma si es un sustantivo (/NM), un vervo (/VB), un adjetivo(/JJ) o un pronombre (/PRS)
    '''
    dato = parse(palabra,tokenize = True,tags = True,chunks = False).replace(palabra,'')
    if(dato in ['/NM','/VB','/JJ','/PRS']):
        print('{} es valida, es un {}'.format(palabra,dato))
        return True
    else:
        print('{} NO es valida, es un {}'.format(palabra,dato))
        return False
def borrarPalabras(listaLetras):
    'devuelvo las letras usasas al atril y borro todas las letras que se pusieron en el tablero'
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
def sumarPuntos(palabra,listaPorDefecto):
    'calcula el puntaje de la palabra ingresada'
    suma = 0
    for i in palabra:
        suma = suma + listaPorDefecto['PuntajeLetra'][i]
    print('puntos de la pabra {}: {}'.format(palabra,suma))
    return suma

def ventana_salir():
    'ventana que confirma si se decea salir del juego'
    layout = [
        [sg.Text('¿Seguro que desea salir?')],
        [sg.Button('SI'),sg.Button('NO')]
    ]
    window = sg.Window('', layout,font=("Helvetica", 12))
    event , values = window.read()
    while  True:
        if event == 'SI':
            return True
        else:
            return False
    window.close() #FALTA TERMINAR



#Interface grafica
Atril = [[botonesAtril(x)for x in range(7)]]                                    #creo el atril de 7 botones
Tablero = [[botonTablero(x,y) for x in range(15)] for y in range(15)]           #creo el el trablero de 15x15 botones
botonesTurno= [
    [sg.Button('Confirmar',tooltip='Probar si la plabra es correcta',disabled=True,size= (10,1)),
    sg.Button('Cambiar',tooltip='cambiar Fichas',disabled=True,size= (10,1)),
    sg.Button('Pasar',tooltip='Pasar turno',disabled=True,size= (10,1))],
]
columna1 = [                                                                    #Contiene el tablero de juego y atril con las fichas de la mano
    [sg.Column(Tablero)],
    [sg.Text('ATRIL',size=(30,1),font=("Helvetica", 15))],
    [sg.Column(Atril), sg.Column(botonesTurno)],
]
columnaPuntaje=[
    [sg.Text('PUNTAJE')],
    [sg.Text('Jugador'),sg.Text('---',key ='contadorPuntosPJ',)],
    [sg.Text('Computadora'),sg.Text('---',key ='contadorPuntosPC',)],

]
columnaTiempo=[
    [sg.Text('TIEMPO')],
    [sg.Text('---',key='cronometro')],
]
columna2= [                                                                     #contiene los puntajes y el tiempo que resta del turno
        [sg.Column(columnaPuntaje,pad=(10,0))],
        [sg.Column(columnaTiempo,pad=(10,0))],
        [sg.Button('Comenzar',auto_size_button=False,tooltip='Comenzar Partida',size= (12,2))],
        [sg.Button('Pausar',auto_size_button=False,tooltip='Comenzar Partida',size= (12,2))],
        [sg.Button('Salir',auto_size_button=False,tooltip='salir al menu',size= (12,2))]
]

layout  = [
    [sg.Text('SCREBLE_AR',font=("Helvetica", 20,'bold'),size=(50,1))],
    [sg.Column(columna1),sg.Column(columna2)],

]
cordAtril = ['(0, 0)0','(1, 0)1','(2, 0)2','(3, 0)3','(4, 0)4','(5, 0)5','(6, 0)6'] #no se me ocurrio una forma mejor, las cordenasd de las letras se guardan de una forma extraña
#Programa

def main(listaConfiguracion=listaPorDefecto):
    window = sg.Window('', layout,font=("Helvetica", 12))
    puntosPJ = 0
    puntosPC = 0
    cont_turno = 0
    listaPoiciones = [] #lista de las letras q se van a poner en el tablero
    turno = True
    while True:
        while turno:
            event , values = window.read()
            if event is None or event == 'Salir':
                sys.exit()
            window['contadorPuntosPJ'].update(puntosPJ)
            window['contadorPuntosPC'].update(puntosPC)
            if event is 'Comenzar':
                window['Comenzar'].update(disabled=True)
                window['Pasar'].update(disabled=False)
                window['Confirmar'].update(disabled=False)
                window['Cambiar'].update(disabled=False)
                desbloquearAtril()
                repartirFichas(listaConfiguracion['CantidadLetras'])
                asignarPuntajesTablero()
            if event in ['Confirmar','Cambiar','Pasar','Comenzar','Pausar']:
                if (event is 'Confirmar') &(len(listaPoiciones)>0): #si se preciona el boton confirmar y se pusieron fichas en el tablero
                    if (confirmarPalabra(formarPalabra(listaPoiciones))):
                        puntosPJ =puntosPJ + sumarPuntos(formarPalabra(listaPoiciones),listaConfiguracion)
                        window['contadorPuntosPJ'].update(puntosPJ)
                        turno = False
                    else:
                        borrarPalabras(listaPoiciones)
                    del listaPoiciones[:] #vacio la lista con las letras que se usaron
                if (event is 'Pasar')&(len(listaPoiciones)==0) :  #si se preciona el boton confirmar y no se pusieron fichas en el tablero
                    turno = False
                    repartirFichas(listaConfiguracion['CantidadLetras'])
                    del listaPoiciones[:]
            elif event in cordAtril:  #se preciona algun boton en el atril
                cord = event
                letraAtril = cord
                letra = AtrilLetras[int(letraAtril[1])].getLetra()
                desbloquerTablero()
            else: #se precion algun boton en el tablero
                cord = event
                #reviso si el tablero esta vacion en esa posicion
                if(TableroLetras[cord[0]][cord[1]].getLetra()==' '):
                    TableroLetras[cord[0]][cord[1]].setLetra(letra) #asigno la letra a la posicion
                    AtrilLetras[int(letraAtril[1])].vaciar()  #elimino esa ficha del atril
                    listaPoiciones.append(cord)
                bloquearTablero()


        if not turno: #termina el turno
            bloquearJuego(window)
            cont_turno +=1;
            print('turno numero:',cont_turno)

            repartirFichas(listaConfiguracion['CantidadLetras'])
            print('aca va el turno de la maquina')
            turno = True
            desbloquearJuego(window)

    window.close()
if __name__ == '__main__':
    main()
