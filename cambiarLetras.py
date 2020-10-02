import PySimpleGUI as sg
import juego

def main(atrilPJ,listaConfiguracion):
    '''
    cambia las letras del atril de JUGADOR

    Parametros:
    atrilPJ -- el atril del juegador donde estan las letrasPuntos
    listaConfiguracion -- contienee todos los valores de configuracion del juego.

    Retorna:
    lista -- contiene las fichas que se desean cambiar.

    '''

    AtrilCambiar = [0 for x in range(7)] #atril de 7 elementos
    Atril = [juego.botonesAtril(listaConfiguracion['Nivel'],x,AtrilCambiar) for x in range(7)] #creo en cada elemento del atril un boton

    layout2 = [
    [sg.Text('seleccione las letras que decea cambiar')],
    [sg.Column([Atril])],
    [sg.Button('Confirmar',size= (15,1)),sg.Button('Cancelar',size= (15,1))],
    ]

    window = sg.Window('', layout2,font=("Helvetica", 12))
    cordAtril =  [(x,0) for x in range(0,7)]
    aux = True
    lista=[]

    while True:
        event, values = window.read(timeout=10)
        if(aux):
            for i in range(7):
                AtrilCambiar[i].setLetra(atrilPJ[i].getLetra())
                AtrilCambiar[i].desbloquear()
            aux = False
        if event in cordAtril:
            letra = AtrilCambiar[event[0]].marcar()
            lista.append(event[0])
        if event is 'Confirmar':
            window.close()
            return lista
        if event is 'Cancelar':
            window.close()
            del lista[:]
            return(lista)
if __name__ == '__main__':
    main()
