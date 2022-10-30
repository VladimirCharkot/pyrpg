from random import choice, randint

# Import relativo:
from .personaje import Personaje
from compartido.utils import progresivo, menu, menu_numerico, tirada
from compartido.excepciones import MPInsuficiente


class Guerrero(Personaje):

    def __init__(self, nombre, hp, atk, arma):
        super().__init__(nombre, hp, 0, '2d6', 0.3)
        self.equipar(arma)

    def danio(self):
        if self.arma:
            return tirada(self.arma.atk) + self.arma.bonus
        else:
            return super().danio()




class Mago(Personaje):

    def __init__(self, nombre, hp, mp, hechizos):
        super().__init__(nombre, hp, mp, '2d4', 0.2)
        self.hechizos = hechizos

    def magia(self, hechizo, objetivo):
        if self.mp < hechizo.coste:     # Verificamos mp suficiente
            raise MPInsuficiente()
        progresivo(hechizo.expresion)
        hechizo.efecto(objetivo)                # Ejecutamos efecto
        self.mp -= hechizo.coste                # Descontamos mp
