from itertools import permutations
import pattern.es
import random
from pattern.es import parse

def clasifico(palabra, tipoPalabra):
    '''
    Función que recibe una palabra y verifica que sea adjetivo o verbo

    Parametros:
    palabra -- es un string
    tipoPalabra -- lista con los tag de los tipos de palabras validas.

    Retorna
    True si está dentro de la clasificación, False caso contrario
    '''
    dato = parse(palabra,tokenize = True,tags = True,chunks = False).replace(palabra,'')
    if(dato in tipoPalabra):
        return True

def esPalabra(palabra):
    '''
    Verifica si es una palabra válida
    Parametros:
    palabra -- un string

    Retorna:
    True si la plabra se encuentra en lexicon y spelling (es valida)
    False si el string no es una palabra valida
    '''
    if palabra in pattern.es.lexicon:
        #print(pal + " en lexicon ")
        if palabra in pattern.es.spelling:
            #print(pal + " en spelling ")
            return True
    return False

def armoPalabra(letrasPalabras):
    '''
    Armo las posibles combinaciones y permutaciones con una lista de letras recibidas

    Parametros:
    letrasPalabras -- letras que contiene la mano o el atril de la pc

    Retorna:
    palabras -- una lista con todas las posibles combinaciones de 2 hasta 7 caracteres de las letras de la mano
    '''
    letras = ''
    for letra in letrasPalabras:
        letras += letra
    palabras = set()
    for i in range(2, len(letras) + 1):
        palabras.update((map("".join, permutations(letras, i))))
    return (palabras)

def generarPalabra(mano,tipo):
    '''
    genera una lista de palabras validas con las letras de la mano y devuelve la primera de ellas si es que existe.

    Parametros:
    mano -- lista de letras que contiene la mano o el atril de la pc
    tipo -- lista con los tag de los tipos de palabras validas

    Retorna:
    la primer palabra valida o False si no encontro palabras.
    '''
    listaPalabras = armoPalabra(mano)
    palabrasClasificadas = []
    palabrasValidas = []
    for pal in listaPalabras:
        if esPalabra(pal):
            palabrasValidas.append(pal)
            if clasifico(pal, tipo):
                palabrasClasificadas.append(pal)
    if(palabrasClasificadas):
        return(palabrasClasificadas[0])
    else:
        return None

def crearPalabra(Atril,listaConfiguracion,listaAcciones,ventana):
    '''intenta una palabra con las letras del atril, sin no puede generar una palabra avisa por pantalla que ya no puede.

    Parametros:
    atril -- atril que contiene las letras de la mano de la pc
    listaConfiguracion -- diccionario que contiene las configuraciones del juego
    listaAcciones -- lista con todas las acciones (palabras colocadas y puntajes obtenidos)
    ventana -- interface generada por PySimpleGUI
    '''
    mano = []
    palabra = ''
    for i in range(7):
        mano.append(Atril[i].getLetra())
    palabra = generarPalabra(mano,listaConfiguracion['TipoPalabra'])
    if(palabra != None):
        return palabra
    else:
        listaAcciones.append('----------------------------------')
        listaAcciones.append('La PC ya no tiene palabra')
        ventana['acciones'].update(listaAcciones[::-1])

def intentoColocarPalabra(palabra,tablero):
    '''la pc intenta colocar la palabra que formo en una ubicacion random dentro del tablero

    Parametros:
    palabra -- string que intenta colocar en el Tablero
    tablero -- tablero de juego de 15x15

    Retorna:
    una tupla que el primer valor es si pudo colocar la palabra en el tablero y la segunda la lista de posiciones donde va cada letra
    '''
    orientacion = random.choice(['vertical','horizontal'])
    cant = 0
    vacio = True
    Lpalabra =[]
    if(tablero[7][7].getEstado()==1):
        a = random.randrange(14)
        if(a + len(palabra)>=15):
            a=a-len(palabra)
        b = random.randrange(14)
    else:
        a = 7
        b = 7
    if(orientacion == 'horizontal'):
        while (vacio) & (cant<len(palabra)):
            if(tablero[a][b].getEstado()==0):
                Lpalabra.append((a,b))
            else:
                vacio = False
            a = a +1
            cant = cant + 1
        if vacio:
            return (True,Lpalabra)
        else:
            return (False,None)
    if( orientacion == 'vertical'):
        while (vacio) & (cant<len(palabra)):
            if(tablero[b][a].getEstado()==0):
                Lpalabra.append((b,a))
            else:
                vacio = False
            a = a +1
            cant = cant + 1
        if vacio:
            return (True,Lpalabra)
        else:
            return (False,None)

def colocaPalabra(palabra,tablero):
    '''la pc coloca la palabra en una ubicacion random permitida dentro del tablero

    Parametros:
    palabra -- string que intenta colocar en el Tablero
    tablero -- tablero de juego de 15x15

    '''
    aux = intentoColocarPalabra(palabra,tablero)
    while(aux[0] == False):
        aux = intentoColocarPalabra(palabra,tablero)
    numero = 0
    while(numero < len(palabra)):
        i = aux[1][numero]
        tablero[i[0]][i[1]].setLetra(palabra[numero])
        numero = numero +1
    return(aux[1])

def elimiarLetrasAtril(palabra,atril):
    ''' elimina las letras utilizadas en la palabra del AtrilLetras

    Parametros:
    palabra -- string que intenta colocar en el Tablero
    atril -- atril que contiene las letras de la mano de la pc
    '''
    mano = []
    for i in range(7):
        mano.append(atril[i].getLetra())
    for i in palabra:
        aux = 0
        while(mano[aux]!=i):
            aux = aux +1
    atril[aux].vaciar()
