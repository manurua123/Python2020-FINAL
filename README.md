# ScrabbleAR.py
_Seminario de Lenguajes 2020 Python, Facultad de Informatica, U.N.L.P._
## Informacion :pushpin:
ScrabbleAR es un juego basado en el popular juego Scrabble, en el que se intenta ganar puntos mediante la construcción de palabras sobre un tablero. En ScrabbleAR se juega contra la computadora y se redefinen algunas de las reglas del juego original. En particular, respecto a las palabras a construir, sólo se podrán utilizar palabras clasificadas como adjetivos, sustantivos y verbos, de acuerdo a cómo se configure el juego



## Requisitos 📋
### Software 
  * [Python 3.6.8](https://www.python.org/downloads/release/python-368/) :snake:
### Librerias 
  * [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI/) - _interface grafica_
  * [Pattern](https://github.com/clips/pattern/) - _Procesamiento del lenguaje natural_
### Sistema Operativo 
  [Windows 10 version 1909](https://support.microsoft.com/es-ar/help/4517245/feature-update-via-windows-10-version-1909-enablement-package)   
  [Ubuntu 20.04 LTS](https://ubuntu.com/)
## Contenido :open_file_folder:
### Juego
Contiene todo lo referido a la partida, el tablero, el atril de cada jugador, el marcador de puntaje y el tiempo.
### configuracion
 En este apartado el jugador puede seleccionar la duración máxima de la partida, la duración de cada turno y el nivel de juego:
* **Fácil:** todas las letras otorgan mayor cantidad de putos, se aumenta el número de vocales, el tablero contiene muchos más multiplicadores y se admiten todo tipo de palabras.
* **Medio:** la cantidad de letras y el puntaje es similar al original al igual que el tablero, solo se admite verbos y adjetivos.
* **Difícil:** se reduce el puntaje de cada letra y la cantidad, el tablero contiene más casilleros de penalización y solo se admite verbos y adjetivos.
### Puntajes
En este se pueden observar el top 10 de puntajes en cada una de las dificultades (Fácil, Medio y Difícil) junto con la fecha y además un top 10 general de todas las puntaciones guardadas.


## Como ejecutar **ScrabbleAR.py** 🚀
  1. Compruebar que todas las librerías y programas necesarios están instalados
  
  2. Descomprimir que el contendio del repositorio en la misma carpeta
  
  3. Ejercutar el archivo ScrabbleAR.py

## Autores ✒️ 
  * [Manuel Rua](https://github.com/manurua123)
  
## Licencia :unlock:
  GNU General Public License v3.0
  
## Agradecimientos :balloon:
  * [Tomás Barbieri](https://github.com/tomibarbieri) - _Ayudante_ 
