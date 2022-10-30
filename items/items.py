# Jerarquía de herencia:

# Item
# ├─ Pocion
# │  ├─ PocionHP
# │  └─ PocionMP
# └─ Equipo
#    ├─ Escudo
#    ├─ Arma
#    │  ├─ Espada
#    │  ├─ Arco
#    │  └─ Baston
#    └─ Amuleto
#       ├─ AmuletoHP
#       ├─ AmuletoMP
#       └─ AmuletoDFS

from compartido.utils import progresivo

class Item:
    '''Todos los items tienen peso'''
    def __init__(self, peso):
        self.peso = peso

    def __repr__(self):
        return self.__class__.__name__  # Nombre de clase

    def __str__(self):
        return self.__repr__()


class Pocion(Item):
    '''Todas las pociones recuperan algún stat como hp o mp'''
    def __init__(self, recupera):
        self.recupera = recupera
        super().__init__(1)     # Todas las pociones pesan 1

    def efecto(self, objetivo):
        print('ERROR! Todas las pociones tienen que tener un efecto!')



class PocionHP(Pocion):

    def efecto(self, personaje):
        progresivo(f'{personaje.nombre} recupera {self.recupera}HP...')
        personaje.hp += self.recupera


class PocionMP(Pocion):

    def efecto(self, personaje):
        progresivo(f'{personaje.nombre} recupera {self.recupera}MP...')
        personaje.mp += self.recupera




class Equipo(Item):
    '''Los equipos aumentan atk, hp_max, etc'''
    def __init__(self, tipo, peso):
        self.tipo = tipo
        super().__init__(peso)

    def equipar(self, personaje):
        print('ERROR! Todos los equipos tienen que tener un efecto al equiparse!')

    def desequipar(self, personaje):
        print('ERROR! Todos los equipos tienen que tener un efecto al desequiparse!')


class Arma(Equipo):
    '''Todas sobreescriben el atk del pj y lo restauran al desequiparse'''
    def __init__(self, atk, bonus, peso):
        self.atk = atk
        self.bonus = bonus
        super().__init__('arma', peso)

    def equipar(self, personaje):
        personaje.atk = self.atk    # Todas las armas actualizan el atk del pj

    def desequipar(self, personaje):
        personaje.atk = personaje.atk_base


class Espada(Arma):
    '''El classic. Fuerte.'''
    def __init__(self, bonus):
        super().__init__('3d6', bonus, 5)


class Arco(Arma):
    '''No tan fuerte pero incrementa dfs'''
    def __init__(self, bonus):
        super().__init__('3d4', bonus, 3)

    def equipar(self, personaje):
        personaje.dfs += 0.1
        personaje.dfs_base += 0.1
        super().equipar(personaje)

    def desequipar(self, personaje):
        personaje.dfs -= 0.1
        personaje.dfs_base -= 0.1
        super().desequipar(personaje)


class Baston(Arma):
    '''Débil pero incrementa el mp'''
    def __init__(self, bonus):
        super().__init__('2d4', bonus, 3)

    def equipar(self, personaje):
        personaje.mp += self.bonus
        personaje.mp_max += self.bonus
        super().equipar(personaje)

    def desequipar(self, personaje):
        personaje.mp -= self.bonus
        personaje.mp_max -= self.bonus
        super().desequipar(personaje)


class Escudo(Equipo):
    '''Aumenta dfs'''
    def __init__(self, bonus):
        self.bonus = bonus
        super().__init__('escudo', 3)

    def equipar(self, personaje):
        personaje.dfs += self.bonus
        personaje.dfs_base += self.bonus

    def desequipar(self, personaje):
        personaje.dfs -= self.bonus
        personaje.dfs_base -= self.bonus


# Amuletos

class Amuleto(Equipo):
    '''Aumentan algún stat'''
    def __init__(self, bonus):
        self.bonus = bonus
        super().__init__('amuleto', 1)

class AmuletoHP(Amuleto):
    def equipar(self, personaje):
        personaje.hp     += self.bonus
        personaje.hp_max += self.bonus

    def desequipar(self, personaje):
        personaje.hp     -= self.bonus
        personaje.hp_max -= self.bonus

class AmuletoMP(Amuleto):
    def equipar(self, personaje):
        personaje.mp     += self.bonus
        personaje.mp_max += self.bonus

    def desequipar(self, personaje):
        personaje.mp     -= self.bonus
        personaje.mp_max -= self.bonus

class AmuletoDFS(Amuleto):
    def equipar(self, personaje):
        personaje.dfs += self.bonus
        personaje.dfs_base += self.bonus

    def desequipar(self, personaje):
        personaje.dfs -= self.bonus
        personaje.dfs_base -= self.bonus
