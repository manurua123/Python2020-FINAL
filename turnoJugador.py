from pattern.es import parse
import pattern.es
def formarListaPalabra(listaLetras,tablero,atril):
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
        borrarPalabras(palabraV,tablero,atril)
        return palabraH
    else:
        palabraH.pop(0)
        borrarPalabras(palabraH,tablero,atril)
        return palabraV
def confirmarPalabra(Lpalabra,tipoPalabra,tablero):
    '''
    recibe una palabra y confirma si es un sustantivo (/NM), un vervo (/VB), un adjetivo(/JJ) o un pronombre (/PRS)
    '''
    aux = []
    for i in Lpalabra:
        aux.append(tablero[i[0]][i[1]].getLetra())
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
def borrarPalabras(listaLetras,tablero,atril):
    '''devuelvo las letras usasas al atril y borro todas las letras que se pusieron en el tablero'''
    x = 0
    for i in listaLetras:
        letra = tablero[i[0]][i[1]].getLetra()
        tablero[i[0]][i[1]].setLetra('nulo')
        tablero[i[0]][i[1]].setEstado(0)
        tablero[i[0]][i[1]].tipoCelda(tablero[i[0]][i[1]].getTipo()) #devuelvo la imagen que tenia

        ok = True
        while(ok) & (x<7):
            if(atril[x].getLetra() == 'nulo'):
                atril[x].setLetra(letra)
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
def sumarPuntos(Lpalabra,valorLetras,tablero):
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
        letra = tablero[i[0]][i[1]].getLetra()
        tipo =  tablero[i[0]][i[1]].getTipo()
        if(letra != 'nulo'):
            if(tipo == 0):
                suma = suma + valorLetras[letra]
            elif(tipo == 4):
                suma = suma + valorLetras[letra]
            elif(tipo ==1):
                suma = suma + valorLetras[letra]
                aux = aux +1
            elif(tipo == 2):
                suma = suma + (valorLetras[letra]*2)
            elif(tipo == 3):
                suma = suma - valorLetras[letra]
    return (suma * aux)
