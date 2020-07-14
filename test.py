from pattern.es import parse
aux = 1
while(aux < 1000):
    palabra = input("¿Cómo se llama? ")
    dato = parse(palabra,tokenize = True,tags = True,chunks = False).replace(palabra,'')
    print('{} es {}'.format(palabra,dato))
