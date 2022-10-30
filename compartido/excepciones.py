class BatallaException(Exception):
    pass

class ArenaIncompleta(BatallaException):
    pass

class JugadorPierde(BatallaException):
    pass

class Huida(BatallaException):
    pass

class HuidaFallida(BatallaException):
    pass

class AccionInconclusa(BatallaException):
    pass

class NoMochila(BatallaException):
    pass

class MPInsuficiente(BatallaException):
    pass

class AtaqueFallido(BatallaException):
    pass
