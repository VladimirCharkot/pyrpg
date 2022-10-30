from time import sleep
from sys import stdout
from random import randint
from json import load

# Config

config = load(open('compartido/config.json'))

# Printing

def progresivo(texto):
    if config['silencioso']:
        return
    for letra in texto:
            print(letra, end='')
            sleep(config['delay_progresivo'])
            stdout.flush()
    print()
    sleep(config['delay_progresivo_final'])


# Define la función getch, que lee un solo caracter y lo devuelve sin esperar que se presione enter
# Como la consola es diferente en windows y en linux/mac, usamos un try/except para definir la función dependiendo la plataforma

try:
    # Win32
    from msvcrt import getch
except ImportError:
    # UNIX
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


# Dados

def dados(cuantos, caras):
    suma = 0
    for i in range(cuantos):
        suma += randint(1,caras)
    return suma

def tirada(patron):
    cantidad, caras = patron.split('d')
    return dados(int(cantidad), int(caras))


# Menúes

def menu_sn():
    opcion = getch()
    while opcion.upper() not in ['S', 'N']:
        opcion = getch()
    return opcion.upper() == 'S'

# Parámetro default
def menu(opciones, volver=False):
    '''Recibe un diccionario teclas como clave, cada una mapeada a otro diccionario con 'texto' y 'valor':
    {[tecla1] : {[texto] : "...", [valor]: objeto1, [tecla2] : {[texto] : "...", [valor]: objeto2, ...}
    Devuelve el [valor] de la opción seleccionada (mediante la [tecla])'''
    if volver:
        opciones['V'] = {'texto' : '[V]olver', 'valor' : None}
    for c in opciones:
        opcion = opciones[c]
        texto = opcion['texto']
        print(f'{texto}')
    eleccion = getch().upper()
    while not eleccion in opciones:
        eleccion = getch().upper()
    elegido = opciones[eleccion]
    return elegido['valor']

def menu_numerico(opciones, volver=True):
    '''Recibe lista de diccionarios con [texto] y [valor], y devuelve [valor]'''
    opcs = {}
    for i, opc in enumerate(opciones):
        opc['texto'] = str(i + 1) + ' - ' + opc['texto']
        opcs[str(i + 1)] = opc
    if volver:
        opcs[str(i + 2)] = {'texto' : f'{str(i + 2)} - Volver', 'valor' : None}
    return menu(opcs)

def menu_sencillo(opciones, volver=False):
    '''Recibe lista de strings, y devuelve el número de opción seleccionada'''
    opcs = []
    for i, opc in enumerate(opciones):
        opcs.append({'texto': opc, 'valor' : str(i + 1)})
    return menu_numerico(opcs, volver=volver)

def menu_textual(opciones, volver=False):
    '''Recibe lista de strings, y devuelve el string mismo'''
    opcs = []
    for opc in opciones:
        opcs.append({'texto': opc, 'valor' : opc})
    return menu_numerico(opcs, volver=volver)

# Por ejemplo:
# menu({
#     'U': {'texto' : '[U]no', 'valor' : 1},
#     'D': {'texto' : '[D]os', 'valor' : 2}
#     })
