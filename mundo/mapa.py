from random import random
from personajes.enemigos import *
from items.items import *
from items.mochila import *
from compartido.utils import *
from .batalla import *


# Cada lugar está representado por una función, como una narración.
# Podemos tener variables globales como en_paz que pueden ser cambiadas
# desde dentro de alguna de estas funciones y afectar también lo que
# sucede en otros lugares, dependiendo de decisiones anteriores que hayamos tomado

en_paz = False
tiene_llave = False
tiene_album = False

def hogar(jugador):
    if en_paz:
        progresivo("Estás en tu hogar.")
        progresivo("Aquí empezó todo.")
        progresivo("Ahora comprendés.")
        print()
        progresivo("The end")
        exit()
    else:
        progresivo("Te encontrás en tu casa.")
        progresivo("Las frías paredes te oprimen.")
        progresivo("Una congoja existencial te agravia.")
        progresivo("Debés salir a la aventura.")
        opcion = menu_sencillo(["Salir al mundo", "Revisar la casa"])
        print(opcion)
        if opcion == '2':
            progresivo("Encontrás tu vieja mochila de viaje")
            jugador.dar(Mochila(10))
            progresivo("Encontrás unas pociones en un viejo armario")
            jugador.dar(PocionHP(24))
            jugador.dar(PocionMP(24))
            progresivo("")
            if not tiene_llave:
                progresivo("...")
                progresivo("Un viejo cajón cerrado.")
                progresivo("Con llave.")
                progresivo("Qué tenía?...")
                progresivo("Lo olvidaste...")
            else:
                progresivo("Con la llave abrís el viejo cajón cerrado.")
                progresivo("Un álbum de fotos.")
                progresivo("Reconocés en algunas a tu madre.")
                progresivo("Hay otras personas que no reconocés.")
                progresivo("[Obtenido: Antiguo álbum de fotos]")
                tiene_album = True



def bosque(jugador):
    progresivo("La tupida arboleda te proteje.")
    progresivo("Pero las criaturas acechan por la noche...")
    progresivo("Pasarás aquí la noche? [s/n]")

    if menu_sn():
        if random() < 0.5:
            progresivo("Un lobo salvage aparece!")
            try:
                Arena().con_jugadores([jugador]).con_enemigos([Lobo()]).batallar()
            except JugadorPierde:
                progresivo('The end')
                exit()
            jugador.dar(PocionHP(30))
        else:
            progresivo("La noche pasa sin mayores problemas...")
            progresivo("Lo que no te mata te fortalece.")
            progresivo("Empezás con +0.3 Dfs en el próximo combate!")
            jugador.dfs += 0.3

def aldea(jugador):
    progresivo("El cálido ronroneo del ajetreo cotidiano.")
    progresivo("Deseas comprar algo?...")
    progresivo("...")
    progresivo("Hm, parece que el desarrollador todavía no implementó la compra de items")
    progresivo("Aquí hay uno gratis...")
    jugador.dar(PocionHP(30))


def rio(jugador):
    progresivo("El suave arruyo de las venas de la tierra restaura toda tu vitalidad.")
    jugador.hp = jugador.hp_max
    jugador.mp = jugador.mp_max
    progresivo("HP y MP recuperado!")

def montaña(jugador):
    global en_paz
    progresivo("No tan rápido.")
    progresivo("La montaña es sagrada.")
    progresivo("El guardián Fermín corta tu paso.")
    progresivo("Prueba tu valía o muere.")
    getch()

    enemigo = None
    # Si el jugador es guerrero el boss va a ser un mago...
    if isinstance(jugador, Guerrero):
        enemigo = PNJMago('Fermín', 200, 150, [BolaDeFuego, PicosDeHielo])

    # Si el jugador es mago el boss va a ser un guerrero...
    if isinstance(jugador, Mago):
        enemigo = PNJGuerrero('Fermín', 200, '3d6', Espada(5))

    try:
        Arena()\
            .con_jugadores([jugador])\
            .con_enemigos([enemigo])\
            .no_manejar_huida()\
            .batallar()
        progresivo("Más allá de los valles y ríos, fría y hostil, la cima del mundo.")
        progresivo("Contemplás el atardecer en silencio.")
        progresivo("Alcanzás la sabiduría.")
        progresivo("Podés volver en paz.")
        en_paz = True
    except JugadorPierde:
        progresivo("Fermín te destrozó.")
        progresivo("No hay sensatez en quien no sabe retirarse a tiempo.")
        print()
        progresivo("Game over")
        exit()
    except Huida:
        progresivo("Tu dignidad no está en riesgo")
        progresivo("Tendrás otra chance")



# Este diccionario representa el mapa. Para cada lugar, le decimos qué función ejecutar y a qué otros lugares se puede llegar desde allí. Esto último es lo que a fin de cuentas lo convierte en un mapa.

mapa = {
    'Hogar'     : {
        'caminos'   : ['Bosque', 'Río'],
        'acciones'  : hogar
        },
    'Bosque'    : {
        'caminos'   : ['Hogar', 'Aldea'],
        'acciones'  : bosque
        },
    'Aldea'     : {
        'caminos'   : ['Montaña', 'Bosque', 'Río'],
        'acciones'  : aldea
        },
    'Río'       : {
        'caminos'   : ['Hogar', 'Aldea'],
        'acciones'  : rio
        },
    'Montaña'   : {
        'caminos'   : ['Aldea'],
        'acciones'  : montaña
        }
}


# Esta función -recursiva- se encarga de ir recorriendo los lugares y ejecutando las funciones. Cuando se la llama ejecuta las acciones de ese lugar y a continuación nos ofrece los destinos posibles. Una vez elegido un destino, se ejecuta a sí misma con ese destino nuevo.
# El mapa está construído como un *grafo*

def aventura(lugar, jugador):
    print()
    accion = mapa[lugar]['acciones']
    accion(jugador)
    print()
    print('Elegí el próximo paso:')
    proximo = menu_textual(mapa[lugar]['caminos'])
    aventura(proximo, jugador)
