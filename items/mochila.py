# from items import Equipo
from compartido.utils import menu_numerico

class Mochila:
    '''Guarda items, con un límite de peso'''
    def __init__(self, peso_maximo):
        self.items = []
        self.peso_maximo = peso_maximo
        self.tipo = 'mochila'

    def __repr__(self):
        return f'Mochila({self.peso_actual()}/{self.peso_maximo})'

    def __str__(self):
        return self.__repr__()

    def equipar(self, jugador):
        pass

    def desequipar(self, jugador):
        pass

    def peso_actual(self):
        total = 0
        for item in self.items:
            total += item.peso
        return total

    def guardar(self, item):
        if self.peso_actual() + item.peso > self.peso_maximo:
            print('No se puede guardar item! Excede peso máximo de la mochila!')
            return False
        self.items.append(item)
        return True

    def extraer(self):
        items = []
        for item in self.items:
            items.append({'texto' : str(item), 'valor' : item})
        item = menu_numerico(items)
        if item:
            self.items.remove(item)
        return item

    def tomar(self, claseitem):
        for item in self.items:
            if isinstance(item, claseitem):
                self.items.remove(item)
                return item

    def tiene(self, claseitem):
        for item in self.items:
            if isinstance(item, claseitem):
                return True
        return False
