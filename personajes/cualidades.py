from random import random, randint
from compartido.excepciones import Huida, AtaqueFallido
from compartido.utils import *
from items.dinero import *
from items.mochila import Mochila

class Criatura:
    '''
    Representa toda criatura viva
    Recibe nombre, hp (puntos de vida) y mp (puntos de magia). HP y MP son privados y se acceden mediante getters y setters, para que nunca bajen de cero o superen el máximo.
    '''

    def __init__(self, nombre, hp, mp):
        self.nombre = nombre
        self.hp_max = hp
        self.hp = hp
        self.mp_max = mp
        self.mp = mp

    def vivo(self):
        return self.hp > 0

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp):
        if hp < 0:
            self._hp = 0
        elif hp > self.hp_max:
            self._hp = self.hp_max
        else:
            self._hp = hp

    @property
    def mp(self):
        return self._mp

    @mp.setter
    def mp(self, mp):
        if mp < 0:
            self._mp = 0
        elif mp > self.mp_max:
            self._mp = self.mp_max
        else:
            self._mp = mp


class Equipadora:
    '''
    Representa personajes que pueden cargar equipo
    Crea en el objeto un diccionario con los espacios para el equipo y un atributo Dinero. Trabaja con los Equipos.
    '''

    def __init__(self):
        # Usamos un diccionario para poder acceder a las posiciones mediante strings que vengan de los items mismos, de manera que cada item pueda indicar qué espacio ocupa
        self._equipo = {
            'mochila'   : None,
            'arma'      : None,
            'escudo'    : None,
            'amuleto'   : None,
        }
        self.dinero = Dinero(0)


    def equipar(self, item):
        '''Instala el item en el espacio adecuado según su tipo
        Devuelve False si el espacio ya está ocupado y True si se logra equipar'''
        if self._equipo[item.tipo]:
            return False
        item.equipar(self)  # Llamamos a la acción equipar del item
                            # y le pasamos este personaje como argumento
        self._equipo[item.tipo] = item
        return True

    def desequipar(self, item):
        item.desequipar(self)   # Llamamos a la acción desequipar del item
                                # y le pasamos este personaje como argumento
        self._equipo[item.tipo] = None
        return item

    def que_equipado(self, tipo):
        '''Devuelve el item equipado en ese espacio'''
        return self._equipo[tipo]

    # Atajos:

    @property
    def mochila(self):
        return self._equipo['mochila']

    @property
    def arma(self):
        return self._equipo['arma']

    @property
    def escudo(self):
        return self._equipo['escudo']

    @property
    def amuleto(self):
        return self._equipo['amuleto']




class Batalladora:
    '''
    Representa personajes que pueden batallar
    Crea en el objeto los atributos atk, dfs y dmg y los métodos atacar, defender, guir y danio, todos relacionados con la batalla. Asume que el objeto va a tener nombre y hp!
    '''

    def __init__(self, atk, dfs):
        self.atk = atk
        self.atk_base = atk
        self.dfs = dfs
        self.dfs_base = dfs

    def atacar(self, enemigo):
        if random() < enemigo.dfs:
            raise AtaqueFallido(f'{self.nombre} falla ataque a {enemigo.nombre}')
        dmg = self.danio()
        enemigo.hp -= dmg
        progresivo(f'{self.nombre} ataca a {enemigo.nombre} causando {dmg} puntos de daño')
        self.dfs = self.dfs_base    # Luego de atacar perdemos dfs acumulada
        return dmg

    def defender(self):
        if self.dfs < self.dfs_base:    # Restaura la dfs perdida
            self.dfs = self.dfs_base
        self.dfs += random() * 0.2      # Y la incrementa

    def huir(self):
        if random() > 0.5:  # 50% probabilidad de lograr huir
            self.dfs -= 0.3 # Un fallo en la huída nos baja la dfs
        raise Huida(f'{self.nombre} huye')

    def danio(self):
        return tirada(self.atk)
