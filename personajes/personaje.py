from random import random, randint
from compartido.utils import *
from .cualidades import *

class Personaje(Criatura, Equipadora, Batalladora):

    def __init__(self, nombre, hp, mp, atk, dfs):
        Criatura.__init__(self, nombre, hp, mp)
        Equipadora.__init__(self)
        Batalladora.__init__(self, atk, dfs)

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return self.strstatus()

    ## Status

    def status(self):
        progresivo(self.strstatus())

    def strstatus(self):
        if self.vivo():
            simbolo = '✓'
        else:
            simbolo = 'x'
        status = f'[{simbolo}] {self.nombre} - {self.hp}/{self.hp_max}HP'
        if self.mp_max:
            status += f', {self.mp}/{self.mp_max}MP'
        return status
