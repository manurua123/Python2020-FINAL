import PySimpleGUI as sg
import time

# Basic timer in PSG

def Timer():
    sg.theme('Dark')
    sg.set_options(element_padding=(0, 0))
    form_rows = [[sg.Text(size=(8, 2), font=('Helvetica', 20),
                       justification='center', key='text')],
                [ sg.Exit(button_color=('white', 'firebrick4'))]]
    window = sg.Window('Running Timer', form_rows,
                       no_titlebar=True, auto_size_buttons=False)
    i = 0
    paused = False
    start_time = int(round(time.time() * 100))

    while True:
        # This is the code that reads and updates your window
        button, values = window.read(timeout=10)
        window['text'].update('{:02d}.{:02d}'.format((i // 100) % 60, i % 100))
        if(i == 10):
            paused = True
        if values is None or button == 'Exit':
            break

        if button == 'Reset':
            i = 0


        if not paused:
            i += 1

    window.close()

Timer()
