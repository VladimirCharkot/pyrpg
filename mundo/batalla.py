from random import choice
from compartido.utils import progresivo, menu, menu_numerico, getch
from compartido.excepciones import *

class Grupo:
    '''
    Representa a un grupo de personajes
    Se inicializa con una lista de Personajes y una Arena
    '''

    def __init__(self, personajes, arena):
        self.personajes = personajes
        self.arena = arena

    def __str__(self):
        nombres = []    # Juntamos los nombres en una lista
        for p in self.personajes:
            nombres.append(str(p))
        return ', '.join(nombres)

    def todos_vivos(self):
        vivos = True
        for p in self.personajes:   # Reducción booleana
            vivos = vivos and p.vivo()
        return vivos

    def vivos(self):
        vs = []
        for p in self.personajes:
            if p.vivo():
                vs.append(p)
        return vs

    def acciones(self):
        vs = self.vivos()   # Lista de personajes vivos
        if vs:              # Pueden estar todos muertos
            for p in vs:    # Cada personaje su accion
                self.accion(p)

    def accion(self, personaje):
        if not self.arena.batalla_sigue():
            return
        try:
            personaje.accion(self.arena)
        except AccionInconclusa:
            self.accion(personaje)
        except AtaqueFallido as e:
            if not self.arena.silenciosa:
                progresivo(str(e))
        except HuidaFallida:
            if not self.arena.silenciosa:
                progresivo(f'{personaje} falló huída')

    def status(self):
        for p in self.personajes:
            print(p.strstatus())

    def menu(self):
        objetivos_posibles = []     # Construimos el menu
        for j in self.personajes:
            objetivos_posibles.append({'texto' : j.strstatus(), 'valor' : j})
        return objetivos_posibles

    def elegir(self):
        eleccion = menu_numerico(self.menu())
        if eleccion:
            return eleccion
        raise AccionInconclusa()

    def random(self):
        '''Devuelve un personaje *vivo* al azar'''
        return choice(self.vivos())

    def drop(self):
        items = []  # Acumulamos el drop de cada personaje
        for p in self.personajes:
            if not(p.vivo()):
                items.extend(p.drop())
        return items

class Arena:
    '''
    Representa el espacio de batalla
    Enfrenta a dos grupos de personajes, jugadores y enemigos.
    '''

    def __init__(self):
        self.desilenciar()
        self.manejar_huida()

    def no_manejar_huida(self):
        self.gestionar_huida = False
        return self     # Method chaining

    def manejar_huida(self):
        self.gestionar_huida = True
        return self     # Method chaining

    def silenciar(self):
        self.silenciosa = True
        return self     # Method chaining

    def desilenciar(self):
        self.silenciosa = False
        return self     # Method chaining

    def con_jugadores(self, js):
        self.jugadores = Grupo(js, self)
        return self     # Method chaining

    def con_enemigos(self, es):
        self.enemigos = Grupo(es, self)
        return self     # Method chaining

    # Devuelve True mientras haya al menos uno vivo en cada bando
    def batalla_sigue(self):
        '''Devuelve True si ambos Grupos tienen al menos un personaje vivo'''
        return self.jugadores.vivos() and self.enemigos.vivos()

    def batallar(self):
        '''Llama a _batallar, ataja Excepción Huida'''
        try:
            self._batallar()
        except Huida as e:
            print(e)
            if not self.gestionar_huida:
                raise e

    def _batallar(self):
        '''Enfrenta dos grupos en ronda de acciones'''
        js = self.jugadores
        es = self.enemigos
        if not js or not es:
            raise ArenaIncompleta()
        if not self.silenciosa:
            self.status()               # Mostramos el status al comenzar...
        while self.batalla_sigue():
            js.acciones()
            es.acciones()
            if not(js.vivos()):
                raise JugadorPierde()
            if not self.silenciosa:
                getch()                 # Pausa
                self.status()           # ...y luego de cada ronda de acciones
        self.desenlace()

    def adversarios(self, personaje):
        '''Dado un personaje, devuelve su grupo adversario'''
        if personaje in self.jugadores.personajes:
            return self.enemigos
        return self.jugadores

    def aliados(self, personaje):
        '''Dado un personaje, devuelve su grupo'''
        if personaje in self.jugadores.personajes:
            return self.jugadores
        return self.enemigos

    # Status de la batalla
    def status(self):
        '''Borra la pantalla y printea status de los personajes'''
        # Pequeño hack... la secuencia \033c limpia la consola
        progresivo(f"\033c === {self.jugadores} vs {self.enemigos} ===")
        self.jugadores.status()
        print('---')
        self.enemigos.status()
        progresivo('')

    def desenlace(self):
        '''Muestra un texto de desenlace y si es preciso, dropea'''
        if self.jugadores.vivos():
            progresivo('Victoria!')
            self.drop()

    def drop(self):
        '''Recolecta el drop de los enemigos y se los ofrece al usuario'''
        for item in self.enemigos.drop():
            progresivo(f'Obtenido {item}. Quién lo toma?')
            quien = self.jugadores.menu() + [{'texto' : 'Descartar', 'valor' : None}]
            j = menu_numerico(quien, volver=False)
            if j:
                j.dar(item)

    def elegir(self):
        '''Ofrece un menú para elegir un personaje (vivo)'''
        objetivos_posibles = self.jugadores.menu() + self.enemigos.menu()
        eleccion = menu_numerico(objetivos_posibles)
        if eleccion:
            return eleccion
        raise AccionInconclusa()

    def random(self):
        '''Devuelve un personaje *vivo* al azar'''
        return choice(self.jugadores.vivos() + self.enemigos.vivos())
