from itertools import permutations
import pattern.es
import random
from pattern.es import parse
'''este programa genera todas las combinaciones posibles con las letras que recibe en una lista'''

#clasificaciones posibles para adjetivos y verbos

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
        print('la palabra {} es de tipo {}'.format(palabra,dato))
        return True

def es_pal(pal):
    '''
    Verifica si es una palabra válida
    :param pal: un string
    :return: True si es, False caso contrario
    '''
    if pal in pattern.es.lexicon:
        print(pal + " en lexicon ")
        if pal in pattern.es.spelling:
            print(pal + " en spelling ")
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
def main(mano,tipo):
    print(mano)
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

if __name__ == '__main__':
    main()
