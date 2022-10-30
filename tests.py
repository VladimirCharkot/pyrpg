from items.hechizos import *
from items.items import *
from items.mochila import *
from personajes.jugador import *
from personajes.clases import *
from personajes.enemigos import *
from mundo.mapa import *
from mundo.batalla import *

# Probamos algunas cosas de mochila
mochila = Mochila(30)
mochila.guardar(PocionHP(20))
mochila.guardar(PocionMP(40))

assert len(mochila.items) == 2
assert mochila.tiene(PocionHP)
assert not mochila.tiene(Equipo)


# Probamos algunas cosas de Guerrero
guerrero = PJGuerrero('Guerrerín', 120, '2d6', Espada(5))

guerrero.hp = -10
assert guerrero.hp == 0

guerrero.hp = 130
assert guerrero.hp == 120

assert 3 + 5 < guerrero.danio() < 3 * 6 + 5


# Probamos algunas cosas de Mago
mago = PJMago('Maguín', 120, 90, [BolaDeFuego, PicosDeHielo, Cura, Ruleta])
mago.equipar(mochila)

# Verificar que al lanzar un hechizo descuente el mp correspondiente
# Verificar que no pueda lanzar un hechizo para el cual no tiene mp suficiente
# Verficar que los hechizos surten efecto
# Pensar más tests

# Simulamos una batalla entre un mago y un guerrero + un lobo
enemigo_mago = PNJMago('Magonio', 130, 80, [BolaDeFuego, PicosDeHielo])
enemigo_guerrero = PNJGuerrero('Guerronio', 120, '2d6', Baston(3))
lobo = Lobo()

try:
    Arena().con_jugadores([enemigo_guerrero, lobo]).con_enemigos([enemigo_mago]).silenciar().batallar()
except JugadorPierde:
    print('Ganó Magonio')
    assert not(enemigo_guerrero.vivo() or lobo.vivo())
    assert enemigo_mago.vivo()
else:
    print('Ganó Guerreronio y Lobo')
    assert not(enemigo_mago.vivo())
    assert enemigo_guerrero.vivo() or lobo.vivo()

# Corremos una batalla contra el usuario con un hongo
hongo = Hongo()

try:
    Arena().con_jugadores([mago, guerrero]).con_enemigos([hongo]).batallar()
except JugadorPierde:
    print('Ganó el hongo')
    assert hongo.vivo()
    assert not mago.vivo()
else:
    print('Ganó usuario')
    assert mago.vivo()
    assert not hongo.vivo()
