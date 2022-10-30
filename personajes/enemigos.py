from items.items import *
from items.dinero import *
from random import random, randint, choice
from .clases import Mago, Guerrero
from .personaje import Personaje

class PNJ(Personaje):
    """
    Modela el manejo de un Personaje por medio de la IA
    """

    # Los personajes no jugadores tan solo atacan ciegamente
    def accion(self, arena):
        return self.atacar(arena.adversarios(self).random())

    # Los no jugadores a veces también dropean items
    def drop(self):
        return []

class Hongo(PNJ):
    def __init__(self):
        super().__init__('Hongo', 1, 0, '1d1', 0.01)

    def drop(self):
        if random() < 0.5:
            return [PocionHP(randint(3,5))]
        else:
            return [Dinero(randint(3,5))]
        return []

class Lobo(PNJ):
    def __init__(self):
        super().__init__('Lobo', 80, 0, '1d6', 0.2)

class Goblin(PNJ):
    def __init__(self):
        super().__init__('Goblin', 120, 0, '2d4', 0.2)

    def drop(self):
        if random() < 0.3:
            return [Dinero(randint(3,5))]
        return []

class Orco(PNJ):
    def __init__(self):
        super().__init__('Orco', 130, 0, '2d6', 0.25)

    def drop(self):
        if random() < 0.4:
            return [Dinero(randint(5,10))]
        if random() < 0.2:
            return [Escudo(0.1)]
        return []

class PNJMago(PNJ, Mago):

    def accion(self, arena):

        # Encontramos el coste mayor
        max_coste = 0
        for h in self.hechizos:
            if h.coste > max_coste:
                max_coste = h.coste

        # Si tenemos mp de sobra, tiramos magia
        if self.mp > max_coste:
            hechizo = choice(self.hechizos)
            hechizo.efecto(arena.adversarios(self).random())
            self.mp -= hechizo.coste
            return

        if self.mochila and self.mochila.tiene(PocionMP):
            self.mochila.tomar(PocionMP).efecto(self)

        # Si no, ataque normal
        dmg = self.atacar(arena.adversarios(self).random())


class PNJGuerrero(PNJ, Guerrero):
    pass
