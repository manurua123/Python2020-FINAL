import PySimpleGUI as sg
import juego

sg.SetOptions(background_color='#222831',
       text_element_background_color='#222831',
       element_background_color='#9FB8AD',
       button_color=('#222831','#00adb5'),
       text_justification='center',
       border_width=1,
       )

def main(atrilPJ,listaConfiguracion):

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
                #AtrilCambiar[i].setLetra('x')
                AtrilCambiar[i].desbloquear()
            aux = False
        if event in cordAtril:  #se preciona algun boton en el atril
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
