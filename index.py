from personajes.jugador import *
from items.hechizos import *
from mundo.mapa import aventura

jugador = PJMago('Learthal', 120, 210, [BolaDeFuego, PicosDeHielo, Ruleta])

aventura('Hogar', jugador)
