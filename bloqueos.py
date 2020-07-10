'''
contiene todas las funciones que bloquean y desbloquean los botones del juegador
'''

def bloquearTablero(tablero):
    '''bloque los botones del tablero de juego'''
    for x in range(15):
        for y in range(15):
            tablero[x][y].bloquear()
def desbloquerTablero(tablero):
    '''desbloque los botones del tablero de juego'''
    for x in range(15):
        for y in range(15):
            tablero[x][y].desbloquear()
def bloquearAtril(atril):
    '''bloque los botones del atril del jugador'''
    for x in range(7):
        atril[x].bloquear()
def desbloquearAtril(atril):
    '''desbloquea los botones del atril del jugador'''
    for x in range(7):
        atril[x].desbloquear()
def bloquearJuego(window,tablero,atril):
    '''bloque TODOS los botones de la pantalla'''
    bloquearAtril(atril)
    bloquearTablero(tablero)
    window['Pasar'].update(disabled=True)
    window['Confirmar'].update(disabled=True)
    window['Cambiar'].update(disabled=True)
def desbloquearJuego(window,tablero,atril):
    '''desbloquea TODOS los botones de la pantalla'''
    desbloquearAtril(atril)
    desbloquerTablero(tablero)
    window['Pasar'].update(disabled=False)
    window['Confirmar'].update(disabled=False)
    window['Cambiar'].update(disabled=False)
