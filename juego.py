import PySimpleGUI as sg
import random
import string
import pattern.es
from pattern.es import parse

#valores para testear
listaPorDefecto={'PuntajeLetra':{'a':1,'b':3,'c':2,'d':2,'e':1,'f':4,'g':2,'h':10,'i':1,'j':6,'k':8,'l':1,'m':3,'n':1,'o':1,'p':3,'q':8,'r':1,'s':1,'t':1,'u':1,'v':4,'w':8,'x':8,'y':4,'z':10},'CantidadLetras':{'a':11,'b':3,'c':4,'d':4,'e':11,'f':2,'g':2,'h':0,'i':6,'j':0,'k':0,'l':4,'m':3,'n':5,'o':8,'p':0,'q':0,'r':0,'s':7,'t':4,'u':6,'v':0,'w':0,'x':0,'y':0,'z':0},'TipoPalabra':['/NM','/VB','/JJ'],'Tiempo': 60}
def repartirFichas(bolsa_letras):
    for i in range(7):
        if(AtrilLetras[i].getLetra() == ' '):
            letra = random.choice(string.ascii_letters).lower()
            while(bolsa_letras[letra] == 0):
                letra = random.choice(string.ascii_letters).lower()
            AtrilLetras[i].setLetra(letra)
class BotonLetra():
    def __init__ (self,x,y=0):
        self.valor      = ' '
        self.x          = x
        self.y          = y
        self.estado     = 0                                                     #0 si esta libre o 1 si esta ocupado
        self.bloqueo    = False                                                 #bloquea el boton para evitar bugs
        self.key        = (x,y)
        self.boton      = sg.Button(self.valor,size= (4,2),key = self.key)
        self.tipo       = 0
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
            self.valor='X'
            self.boton.update(self.valor,button_color=('black','gold'))
        if (valor ==1):
            self.tipo=valor
            self.valor='Pala\nx2'
            self.boton.update(self.valor,button_color=('black','orange'))
        if(valor== 2):
            self.tipo=valor
            self.valor='Letra\nx2'
            self.boton.update(self.valor,button_color=('black','green'))
        if(valor== 3):
            self.tipo=valor
            self.valor='Pala\n x3'
            self.boton.update(self.valor,button_color=('black','red'))
        else:
            None

AtrilLetras = [0 for y in range(7)]                                             #creo una lista de vacia con 7 lugares [0,0,0,0,0,0,0,0]
def botonesAtril(x):                                                            #lleno la lista vacia con botones de tipo BotonAtril
    AtrilLetras[x] = BotonAtril(x)
    return AtrilLetras[x].boton
TableroLetras = [[' ' for a in range(0,15)] for b in range(0,15)]               #creo una matriz de 15x15 vacia
def botonTablero(x,y):                                                          #lleno la matriz vacia con botones de tipo BotonTablero
    TableroLetras[x][y] = BotonTablero(x,y)
    return TableroLetras[x][y].boton
def asignarPuntajesTablero():
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
    for x in range(15):
        for y in range(15):
            TableroLetras[x][y].bloquear()
def desbloquerTablero():
    for x in range(15):
        for y in range(15):
            TableroLetras[x][y].desbloquear()
def bloquearAtril():
    for x in range(7):
        AtrilLetras[x].bloquear()
def desbloquearAtril():
    for x in range(7):
        AtrilLetras[x].desbloquear()

def confirmarPalabra(palabra,letrasPalabra,listaLetrasUsada):
    palabraSrt = ''.join(palabra)
    dato = parse(palabraSrt,tokenize = True,tags = True,chunks = False).replace(palabraSrt,'')
    print(palabraSrt +' es un ' + dato)
    if(dato in ['/NM','/VB','/JJ']):
        print(palabraSrt +' es valida')
        return True,
    else:
        print(palabraSrt +' NO es valida')
        for i in range(len(palabra)):
            AtrilLetras[listaLetrasUsada[i]].setLetra(palabra[i])
        for i in letrasPalabra:
            TableroLetras[i[0]][i[1]].vaciar()
        return False

def sumarPuntos(palabra,listaPorDefecto):
    palabraSrt = ''.join(palabra)
    suma = 0
    for i in palabraSrt:
        suma = suma + listaPorDefecto['PuntajeLetra'][i]
    print('puntos de la pabra {}: {}'.format(palabraSrt,suma))
    return suma


#Interface grafica
Atril = [[botonesAtril(x)for x in range(7)]]                                    #creo el atril de 7 botones
Tablero = [[botonTablero(x,y) for x in range(15)] for y in range(15)]           #creo el el trablero de 15x15 botones
botonesTurno= [
    [sg.Button('Confirmar',tooltip='Probar si la plabra es correcta'),sg.Button('Cambiar',tooltip='cambiar letras')],
    [sg.Button('Pasar',tooltip='Pasar turno')],
]
columna1 = [                                                                    #Contiene el tablero de juego y atril con las fichas de la mano
    [sg.Column(Tablero)],
    [sg.Text('ATRIL')],
    [sg.Column(Atril), sg.Column(botonesTurno)],
]
columna2= [                                                                     #contiene los puntajes y el tiempo que resta del turno
        [sg.Text('PUNTAJE')],
        [sg.Text('Jugador'),sg.Text('---',key ='contadorPuntosPJ')],
        [sg.Text('PC'),sg.Text('---',key ='contadorPuntosPC')],
        [sg.Text('TIEMPO')],
        [sg.Text('---')],
]
layout  = [
    [sg.Text('SCREBLE')],
    [sg.Column(columna1),sg.Column(columna2)],
    [sg.Button('Comenzar',auto_size_button=False,tooltip='Comenzar Partida'),sg.Button('Salir',auto_size_button=False,tooltip='salir al menu')]
]
cordAtril = ['(0, 0)0','(1, 0)1','(2, 0)2','(3, 0)3','(4, 0)4','(5, 0)5','(6, 0)6'] #no se me ocurrio una forma mejor, las cordenasd de las letras se guardan de una forma extraña

#Programa

def main(listaConfiguracion=listaPorDefecto):
    window = sg.Window('', layout)
    palabra =[]                                                                 #la palabra que se forma con las letras que se ponenen
    letrasPalabra = []                                                          #la posisicion donde se ponen las letras
    listaLetrasUsada = []                                                       #la posicion del atril de donde se sacan las letras
    puntosPJ = 0
    puntosPC = 0
    while True:
        event , values = window.read()
        bloquearTablero()
        window['contadorPuntosPJ'].update(puntosPJ)
        window['contadorPuntosPC'].update(puntosPC)
        if event is None or event == 'Salir':
            break
        if event is 'Comenzar':
            window['Comenzar'].update(disabled=True)
            repartirFichas(listaConfiguracion['CantidadLetras'])
            asignarPuntajesTablero()
        turno = True
        if turno:
            if event in ['Confirmar','Cambiar','Pasar','Comenzar']:
                if event is 'Confirmar':
                    if(confirmarPalabra(palabra,letrasPalabra,listaLetrasUsada)): #comprueva si la palabra es valida
                        puntosPJ = puntosPJ + sumarPuntos(palabra,listaPorDefecto)
                        window['contadorPuntosPJ'].update(puntosPJ)
                        turno = False
                        repartirFichas(listaConfiguracion['CantidadLetras'])
                    else:                                                       #si no es valida borra la palabra guardada, la posicion de las letras y desbloquea todo el atril
                        desbloquearAtril()
                    del listaLetrasUsada[:]
                    del palabra[:]
                    del letrasPalabra [:]

                if event is 'Pasar':
                    turno = False
                    repartirFichas(listaConfiguracion['CantidadLetras'])
            elif event in cordAtril:
                cord = event
                pos = cord
                letra = AtrilLetras[int(pos[1])].getLetra()
                desbloquerTablero()
            else:
                cord = event
                TableroLetras[cord[0]][cord[1]].setLetra(letra)
                letrasPalabra.append(cord)
                palabra.append(letra)
                AtrilLetras[int(pos[1])].vaciar()                               #bloque la ultima lesta  del atil que se toco
                listaLetrasUsada.append(int(pos[1]))
                bloquearTablero()
        else:
            repartirFichas(listaConfiguracion['CantidadLetras'])
            print('aca va el turno de la maquina')
    window.close()
if __name__ == '__main__':
    main()
