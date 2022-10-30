from random import random
from compartido.utils import tirada, progresivo

# objetivos posibles: 'enemigos', 'jugadores', 'arena' (todos)

class BolaDeFuego:
    nombre = 'Bola de Fuego'
    expresion = 'Faeris!'
    coste = 8
    objetivos = 'enemigos'
    def efecto(objetivo):
        dmg = tirada('4d6')
        progresivo(f'Bola de Fuego causa {dmg} puntos de daño a {objetivo.nombre}!')
        objetivo.hp -= dmg

class PicosDeHielo:
    nombre = 'Picos de Hielo'
    expresion = 'Frizium!'
    coste = 14
    objetivos = 'enemigos'
    def efecto(objetivo):
        dmg = tirada('6d6')
        progresivo(f'Picos de Hielo causa {dmg} puntos de daño a {objetivo.nombre}!')
        objetivo.hp -= dmg

class Cura:
    nombre = 'Cura'
    expresion = 'Elaris!'
    coste = 20
    objetivos = 'jugadores'
    def efecto(objetivo):
        recupera = tirada('6d6')
        progresivo(f'Cura recupera {recupera} puntos de vida a {objetivo.nombre}!')
        objetivo.hp -= recupera

class Ruleta:
    nombre = 'Ruleta'
    expresion = 'Azaria!'
    coste = 5
    objetivos = 'arena'
    def efecto(objetivo):
        cantidad = tirada('4d8')
        if random() < 0.5:
            objetivo.hp -= cantidad
            progresivo(f'La ruleta causa {cantidad} puntos de daño a {objetivo.nombre}')
        else:
            objetivo.hp += cantidad
            progresivo(f'La ruleta recupera {cantidad} puntos de vida a {objetivo.nombre}')
