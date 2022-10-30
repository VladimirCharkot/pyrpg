from random import choice
from .clases import Mago, Guerrero
from compartido.utils import progresivo, menu_sn, menu
from compartido.excepciones import AccionInconclusa, NoMochila
from items.items import *
from items.mochila import *
from items.dinero import *

class Jugador:
    """
    Modela el manejo de un Personaje por medio de la interfaz con el usuario (menúes)
    """

    def __init__(self):
        self.menu_acciones = {
            'A' : {'texto': '[A]tacar', 'valor' : 'A'},
            'I' : {'texto': '[I]tem',   'valor' : 'I'},
            'H' : {'texto': '[H]uir',   'valor' : 'H'}
        }

    def accion(self, arena):
        print(f'{self.nombre} - Qué hacer?')
        opcion = menu(self.menu_acciones)
        self.ejecutar_accion(opcion, arena)

    # Los personajes jugadores tienen un menú de acción durante la batalla
    def ejecutar_accion(self, opcion, arena):
        if opcion == 'A':
            dmg = self.atacar(arena.enemigos.elegir())
        if opcion == 'I':
            self.item(arena)
        if opcion == 'H':
            self.huir()

    # Elegir y usar un item
    def item(self, arena):
        if not self.mochila:
            raise NoMochila()

        progresivo('Cuál item?')
        item = self.mochila.extraer()
        if not item:
            raise AccionInconclusa()

        progresivo('Cuál objetivo?')
        objetivo = arena.elegir()
        if not objetivo:
            raise AccionInconclusa()

        item.efecto(objetivo)


    # Qué hacer cuando se recibe un item?
    def dar(self, item):

        if isinstance(item, Dinero):
            progresivo(f'Recibiste {item}.')
            self.dinero += item
            return

        progresivo(f'Recibiste {item}. Qué hacer?')

        # Averiguamos qué clase de item es:
        if isinstance(item, Equipo) or isinstance(item, Mochila):
            opcion = menu({
                'G' : {'texto' : '[G]uardar', 'valor': 'G'},
                'D' : {'texto' : '[D]escartar', 'valor': 'D'},
                'E' : {'texto' : '[E]quipar', 'valor': 'E'}
            })
        if isinstance(item, Pocion):
            opcion = menu({
                'G' : {'texto' : '[G]uardar', 'valor': 'G'},
                'D' : {'texto' : '[D]escartar', 'valor': 'D'},
                'C' : {'texto' : '[C]onsumir', 'valor': 'C'}
            })

        if opcion == 'G':
            if not self.mochila:
                progresivo('No tenés mochila donde guardar!')
                self.dar(item)
                return
            if self.mochila.guardar(item):
                progresivo('Guardado en la mochila!')
            else:
                progresivo('No se puede guardar... excede el peso máximo de la mochila!')

        if opcion == 'E':
            if self.equipar(item):
                progresivo(f'{item} equipado!')
            else:
                equipado = self.que_equipado(item.tipo)
                progresivo(f'Ese espacio ya está ocupado por {equipado}. Querés desequiparlo y cambiarlo por {item}?')
                if menu_sn():
                    self.desequipar(equipado)
                    self.equipar(item)
                    self.dar(equipado)
                else:
                    self.dar(item)  # Volvemos a empezar

        if opcion == 'C':
            item.efecto(self)

        if opcion == 'D':
            progresivo(f'{item} desechado')



class PJMago(Jugador, Mago):

    def __init__(self, nombre, hp, mp, hechizos):
        Jugador.__init__(self)
        self.menu_acciones['M'] = {'texto': '[M]agia',  'valor' : 'M'}
        Mago.__init__(self, nombre, hp, mp, hechizos)

    def ejecutar_accion(self, opcion, arena):
        if opcion == 'M':
            self.magia(arena)
        super().ejecutar_accion(opcion, arena)

    def menu_hechizos(self):
        hechizos = []
        for h in self.hechizos:
            hechizos.append({
                'texto' : f'{h.nombre} ({h.coste}MP)',
                'valor' : h
            })
        return hechizos

    def magia(self, arena):
        print(f'\nQué hechizo?')
        hechizo = menu_numerico(self.menu_hechizos())
        if not hechizo:
            raise AccionInconclusa()
        if self.mp >= hechizo.coste:
            print(f'\nQué objetivo?')
            if hechizo.objetivos == 'arena':
                objetivo = arena.elegir()
            elif hechizo.objetivos == 'jugadores':
                objetivo = arena.jugadores.elegir()
            elif hechizo.objetivos == 'enemigos':
                objetivo = arena.enemigos.elegir()
            super().magia(hechizo, objetivo)
        else:
            progresivo('Mp insuficiente!')
            self.magia(arena)      # Reiniciamos este menú



class PJGuerrero(Jugador, Guerrero):

    def __init__(self, nombre, hp, atk, arma):
        Jugador.__init__(self)
        self.menu_acciones['D'] = {'texto': '[D]efender',   'valor' : 'D'}
        Guerrero.__init__(self, nombre, hp, atk, arma)

    def ejecutar_accion(self, opcion, arena):
        if opcion == 'D':
            return self.defender()
        return super().ejecutar_accion(opcion, arena)
