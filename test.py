from pattern.es import parse
import pattern
while True:
    palabra = input("Ingrasa una palabra: ")
    if palabra in pattern.es.lexicon:
        if palabra in pattern.es.spelling:
            dato = parse(palabra,tokenize = True,tags = True,chunks = False).replace(palabra,'')
            print('{} es de tipo {}'.format(palabra,dato))
        else:
            print('{} no esta en spelling'.format(palabra))
    else:
        print('{} No esta en lexicon'.format(palabra))
