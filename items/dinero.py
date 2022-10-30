class Dinero:

    def __init__(self, cantidad):
        self.cantidad = cantidad

    def __add__(self, otro):
        return Dinero(self.cantidad + otro.cantidad)

    def __sub__(self, otro):
        return Dinero(self.cantidad - otro.cantidad)

    def __repr__(self):
        return f'{self.cantidad} monedas de plata'

    def __str__(self):
        return self.__repr__()
