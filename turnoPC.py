from itertools import permutations
import pattern.es
import random
from pattern.es import parse

def clasifico(palabra, tipoPalabra):
    '''
    Función que recibe una palabra y verifica que sea adjetivo o verbo
    :param palabra: es un string
    :param clasificacion: un diccionario que tiene las clasficaciones que busco
    :return: True si está dentro de la clasificación, False caso contrario
    '''
    dato = parse(palabra,tokenize = True,tags = True,chunks = False).replace(palabra,'')
    # print(s)
    if(dato in tipoPalabra):
        #print('la palabra {} es de tipo {}'.format(palabra,dato))
        return True
def es_pal(pal):
    '''
    Verifica si es una palabra válida
    :param pal: un string
    :return: True si es, False caso contrario
    '''
    if pal in pattern.es.lexicon:
        #print(pal + " en lexicon ")
        if pal in pattern.es.spelling:
            #print(pal + " en spelling ")
            return True
    return False
def armo_palabra(letras_palabras):
    '''
    Armo las posibles combinaciones y permutaciones con una lista de letras recibidas
    :param letras_palabras: lista de letras
    :return: un conjunto con las palabras armadas
    '''
    letras = ''
    # for letra in letras_palabras:
    #    letras += entradas[letra]
    for letra in letras_palabras:
        letras += letra
    palabras = set()
    for i in range(2, len(letras) + 1):
        palabras.update((map("".join, permutations(letras, i))))
    return (palabras)
def generarPalabra(mano,tipo):
    #print(mano)
    lista_palabras = armo_palabra(mano)
    palabras_adj_verb = []
    palabras_validas = []
    for pal in lista_palabras:
        if es_pal(pal):
            palabras_validas.append(pal)
            if clasifico(pal, tipo):
                palabras_adj_verb.append(pal)
    if(palabras_adj_verb):
        return(palabras_adj_verb[0])
    else:
        return None
def crearPalabra(Atril,listaConfiguracion,listaAcciones,ventana):
    '''crea una palabra con las letras que se pusieron en el tablero, sin no puede generar una palabra avisa por pantalla que ya no puede. '''
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
    '''la pc intenta colocar la palabra que formo en una ubicacion random dentro del tablero'''
    orientacion = random.choice(['vertical','horizontal']) #la palabra va a ir Verticarl u Horizoantal
    cant = 0
    vacio = True
    Lpalabra =[]
    if(orientacion == 'horizontal'):
        if(tablero[7][7].getEstado()==1):
            x = random.randrange(14)
            if(x + len(palabra)>=15): #evita elegir una cordenada que exeda el tablero
                x=x-len(palabra)
            y = random.randrange(14)
        else:
            x = 7
            y = 7

        while (vacio) & (cant<len(palabra)):
            if(tablero[x][y].getEstado()==0):
                Lpalabra.append((x,y))
            else:
                vacio = False
            x = x +1
            cant = cant + 1
        if vacio:
            return (True,Lpalabra)
        else:
            return (False,None)
    if( orientacion == 'vertical'):
        if(tablero[7][7].getEstado()==1):
            y = random.randrange(14)
            if(y + len(palabra)>=15): #evita elegir una cordenada que exeda el tablero
                y=y-len(palabra)
            x = random.randrange(14)
        else:
            x = 7
            y = 7

        while (vacio) & (cant<len(palabra)):
            if(tablero[x][y].getEstado()==0):
                Lpalabra.append((x,y))
            else:
                vacio = False
            y = y +1
            cant = cant + 1
        if vacio:
            return (True,Lpalabra)
        else:
            return (False,None)
def colocaPalabra(palabra,tablero):
    '''la pc coloca la palabra en una ubicacion random permitida dentro del tablero'''
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
     mano = []
     for i in range(7):
         mano.append(atril[i].getLetra())
     for i in palabra:
         aux = 0
         while(mano[aux]!=i):
             aux = aux +1
         atril[aux].vaciar()
