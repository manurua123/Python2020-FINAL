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
listaPorDefecto={'PuntajeLetra':{'a':1,'b':3,'c':2,'d':2,'e':1,'f':4,'g':2,'h':10,'i':1,'j':6,'k':8,'l':1,'m':3,'n':1,'o':1,'p':3,'q':8,'r':1,'s':1,'t':1,'u':1,'v':4,'w':8,'x':8,'y':4,'z':10},'CantidadLetras':{'a':11,'b':3,'c':4,'d':4,'e':11,'f':2,'g':2,'h':0,'i':6,'j':0,'k':0,'l':4,'m':3,'n':5,'o':8,'p':0,'q':0,'r':0,'s':7,'t':4,'u':6,'v':0,'w':0,'x':0,'y':0,'z':0},'TipoPalabra':['/NM','/VB','/JJ','/PRP','/DT','/IN'],'Tiempo': 60,'TipoTablero':1}

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
class BotonesAtrilPC():
    def __init__ (self,x):
        self.valor= ' '
        self.x = x
        self.estado = 0    #0 si esta libre o 1 si esta ocupado
        self.bloqueo = True  #bloquea el boton para evitar bugs
        self.key = (x,0)
        self.boton  = sg.Button(' ',size= (4,2),key = self.key,disabled=self.bloqueo,pad=(1,1), button_color=('#222831','#e0dede'))
        self.tipo = 0
    def getLetra(self):
        return self.valor
    def setLetra(self,v):
        self.valor = v
        self.estado = 1
    def getEstado(self):
        return self.estado

#Atril del la maquina, del jugador y el tablero de juego
AtrilLetrasPC = [0 for y in range(7)]                                             #creo una lista de vacia con 7 lugares [0,0,0,0,0,0,0,0]
def botonesAtrilPC(x):
    'genera un boton en la cordenada x'
    AtrilLetrasPC[x] =  BotonesAtrilPC(x)
    return AtrilLetrasPC[x].boton
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
#inicil de la partida
def asignarPuntajesTablero(listaConfiguracion):
    'asigna un tipo especifico a cada boton del tablero'
    if (listaConfiguracion['TipoTablero']==1):
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
    elif(listaConfiguracion['TipoTablero']==2):
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
    elif(listaConfiguracion['TipoTablero']==3):
        for i in range(15):
            for j in range(15):
                if(i+j==14)|(i==j):
                    TableroLetras[i][j].tipoCelda(1)
                if(((i==0) &((j+1)%4==0))|((j==0) &((i+1)%4==0))|((i==14) &((j+1)%4==0))|((j==14) &((i+1)%4==0))|(((i+1)%4==0)&((j+1)%4==0))):
                    TableroLetras[i][j].tipoCelda(3)
                if(((i==0) &((j+1)%8==0))|((j==0) &((i+1)%8==0))|((i==14) &((j+1)%8==0))|((j==14) &((i+1)%8==0))|(((i+1)%8==0)&((j+1)%8==0))):
                    TableroLetras[i][j].tipoCelda(2)
                if(i==7)&(j==7):
                    TableroLetras[i][j].tipoCelda(0)
#turno del jugador
def repartirFichas(bolsa_letras):
    'reparte fichas de la bolsa de letras por cada boton vacio en el atril del jugador o de la pc'
    for i in range(7):
        if(AtrilLetras[i].getLetra() == ' '):
            letra = random.choice(string.ascii_letters).lower()
            while(bolsa_letras[letra] == 0):
                letra = random.choice(string.ascii_letters).lower()
            AtrilLetras[i].setLetra(letra)
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
    dato = parse(palabra,tokenize = True,tags = True,chunks = False).replace(palabra,'')
    if(dato in tipoPalabra):
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

def sumarPuntos(Lpalabra,valorLetras):
    '''calcula el puntaje de la palabra ingresada y lo multiplica por los cosito de colores (no me sale la palabra)
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
    print('puntos de la pabra : {}'.format(suma*aux))
    return (suma * aux)

#turno de la PC
def repartirFichasPC(bolsa_letras):
    'reparte fichas de la bolsa de letras por cada boton vacio en el atril del jugador o de la pc'
    for i in range(7):
        if(AtrilLetrasPC[i].getLetra() == ' '):
            letra = random.choice(string.ascii_letters).lower()
            while(bolsa_letras[letra] == 0):
                letra = random.choice(string.ascii_letters).lower()
            AtrilLetrasPC[i].setLetra(letra)
def palabrasEnJuego():
    '''
    arma una lista con las palabras de mas de dos letras y menos de 7 que proporciona pattern.es
    '''
    palabras = list(pattern.es.spelling.keys())
    palabrasOK= []
    for i in palabras:
        if(len(i)<7)&(len(i)>2):
             palabrasOK.append(i)
    return palabrasOK
def generaPalabra(tipoPalabra,AtrilLetrasPC,palabras_validas):
    '''
    genera una palabra al azar dentro del diccionario de palabras que generamos (2<caracteres<7), crea una lista con las letras que la forman,
    tranforma esa esa lista en un conjunto y toma los elementos que comparte este conjunto con las letras de la mano, si todos las letras de la palbra random estan
    en la mano y la palabra es del tipo indicado devuelve la palabra encontrada
    '''
    mano = []
    for i in range(7):
        mano.append(AtrilLetrasPC[i].getLetra())
    palabra = ''
    letras = set(mano)
    aux = False
    while not aux:
        dato = parse(palabra,tokenize = True,tags = True,chunks = False).replace(palabra,'')
        if(dato in tipoPalabra):
            aux = True
        palabraRandom = list(random.choice(palabras_validas))
        print("".join(palabraRandom)) #eso es para ver que este funcionando
        res = list(set(palabraRandom) & letras)
        if (len(res) == len(palabraRandom)):
            palabra = "".join(palabraRandom)
    return palabra


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
AtrilPC = [[botonesAtrilPC(x)for x in range(7)]]
Tablero = [[botonTablero(x,y) for x in range(15)] for y in range(15)]           #creo el el trablero de 15x15 botones
botonesTurno= [
    [sg.Button('Confirmar',tooltip='Probar si la plabra es correcta',disabled=True,size= (12,2)),
    sg.Button('Cambiar',tooltip='cambiar Fichas',disabled=True,size= (12,2)),
    sg.Button('Pasar',tooltip='Pasar turno',disabled=True,size= (12,2))],
]
columna1 = [   #Contiene el tablero de juego y atril con las fichas de la mano
    [sg.Text('ATRIL Computadora',size=(30,1),font=("Helvetica", 15))],
    [sg.Column(AtrilPC)],
    [sg.Column(Tablero)],
    [sg.Text('ATRIL Jugador',size=(30,1),font=("Helvetica", 15))],
    [sg.Column(Atril), sg.Column(botonesTurno)],

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
    [sg.Text('TURNO',size=(10,1))],
    [sg.Text('---',key='contTurno')],
    [sg.Text('TIEMPO',size=(10,1))],
    [sg.Text('---',key='cronometro')],
]
columna2= [                                                                     #contiene los puntajes y el tiempo que resta del turno
        [sg.Column(columnaPuntaje,)],
        [sg.Column(columnaTiempo,)],
        [sg.Text('MULTIPLICADORES',size=(20,1))],
        [sg.Button(' ',size= (4,2),disabled=True,pad=(1,1), button_color=('#222831','#1fab89')),sg.Text('Duplica el valor de la letra',)], #duplica Letra
        [sg.Button(' ',size= (4,2),disabled=True,pad=(1,1), button_color=('#222831','#f07b3f')),sg.Text('Duplica el valor de la palabra',)], #duplica palabra
        [sg.Button(' ',size= (4,2),disabled=True,pad=(1,1), button_color=('#222831','#e84545')),sg.Text('Resta el valor de la letra',)], #resta letra
        [sg.Button('Comenzar',auto_size_button=False,tooltip='Comenzar Partida',size= (20,2))],
        [sg.Button('Pausar',auto_size_button=False,tooltip='Poner partida en pausa',size= (20,2))],
        [sg.Button('Salir',auto_size_button=False,tooltip='salir al menu',size= (20,2))],



]


cordAtril = ['(0, 0)7','(1, 0)8','(2, 0)9','(3, 0)10','(4, 0)11','(5, 0)12','(6, 0)13'] #no se me ocurrio una forma mejor, las cordenasd de las letras se guardan de una forma extraña
#Programa

def main(listaConfiguracion=listaPorDefecto):
    layout  = [
        [sg.Text('SCREBLE_AR',font=("Helvetica", 20,'bold'),size=(50,1))],
        [sg.Column(columna1),sg.Column(columna2)],
    ]
    window = sg.Window('', layout,font=("Helvetica", 12))
    puntosPJ = 0
    puntosPC = 0
    cont_turno = 1
    listaPoiciones = [] #lista de las letras q se van a poner en el tablero
    turno = True
    palabras_validas = palabrasEnJuego()
    counter = 0

    while True:

        event , values = window.read(timeout=10)
        if event is None or event == 'Salir':
            break

        if turno:

            event , values = window.read()
            window['contadorPuntosPJ'].update(puntosPJ)
            window['contadorPuntosPC'].update(puntosPC)
            if event is 'Comenzar':
                window['Comenzar'].update(disabled=True)
                window['Pasar'].update(disabled=False)
                window['Confirmar'].update(disabled=False)
                window['Cambiar'].update(disabled=False)
                desbloquearAtril()
                repartirFichas(listaConfiguracion['CantidadLetras'])
                repartirFichasPC(listaConfiguracion['CantidadLetras'])
                asignarPuntajesTablero(listaConfiguracion)
                window['contTurno'].update(cont_turno)
            if event in ['Confirmar','Cambiar','Pasar','Comenzar','Pausar']:
                if (event is 'Confirmar') &(len(listaPoiciones)>0): #si se preciona el boton confirmar y se pusieron fichas en el tablero
                    if(confirmarPalabra(formarListaPalabra(listaPoiciones),listaConfiguracion['TipoPalabra'])):
                        puntosPJ =puntosPJ + sumarPuntos(formarListaPalabra(listaPoiciones),listaConfiguracion['PuntajeLetra'])
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
                bloquearTablero()   #TURNO JUGADOR

        if not turno: #TURNO DE LA PC
            bloquearJuego(window)
            mano = []
            palabra = generaPalabra(listaConfiguracion['TipoPalabra'],AtrilLetrasPC,palabras_validas)
            print('se encontro la plabra',palabra)
            '''
            puntosPC =puntosPC + sumarPuntos(palabra,listaConfiguracion['PuntajeLetra'])
            window['contadorPuntosPC'].update(puntosPC)
            '''
            repartirFichas(listaConfiguracion['CantidadLetras'])
            turno = True
            desbloquearJuego(window)
            cont_turno +=1;
            window['contTurno'].update(cont_turno)

    window.close()
if __name__ == '__main__':
    main()
