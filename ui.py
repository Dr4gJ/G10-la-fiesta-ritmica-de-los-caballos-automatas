"""Dibujo (PERSONA 1: sprites/animación del caballo; PERSONA 2: pista y HUD;
PERSONA 3: beat y feedback). Solo LEE el estado, no lo modifica.
Versión inicial con rectángulos; reemplazar por sprites después.
"""
import pygame

ANCHO, ALTO = 900, 600
MARGEN_X = 80
COLOR_FONDO = (30, 120, 50)
COLORES_FEEDBACK = {"E": (255, 215, 0), "B": (120, 220, 120), "M": (240, 160, 60), "F": (230, 60, 60)}
TEXTO_FEEDBACK = {"E": "¡Excelente!", "B": "Bueno", "M": "Malo", "F": "Fallo"}


def x_de_posicion(pos, largo):
    """Casillero -> x en pantalla. TODO (P2): interpolar para movimiento suave."""
    ancho_pista = ANCHO - 2 * MARGEN_X - 60
    return MARGEN_X + ancho_pista * pos / largo


def dibujar_pista(pantalla, caballos, largo):
    pantalla.fill(COLOR_FONDO)
    carril_h = 70
    for i in range(largo + 1):
        x = x_de_posicion(i, largo)
        pygame.draw.line(pantalla, (255, 255, 255), (x, 100), (x, 100 + carril_h * len(caballos)), 1)
    pygame.draw.line(pantalla, (255, 255, 255), (x_de_posicion(largo, largo), 100),
                     (x_de_posicion(largo, largo), 100 + carril_h * len(caballos)), 5)
    for i, c in enumerate(caballos):
        dibujar_caballo(pantalla, c, 100 + i * carril_h + 10, largo)


def dibujar_caballo(pantalla, caballo, y, largo):
    """TODO (P1): sprite según caballo.moore.estado y animación."""
    x = x_de_posicion(caballo.afd.posicion, largo)
    pygame.draw.rect(pantalla, caballo.color, (x, y, 50, 40))
    fuente = pygame.font.SysFont(None, 22)
    txt = f"{caballo.nombre}: {caballo.moore.nombre_estado}"
    pantalla.blit(fuente.render(txt, True, (255, 255, 255)), (x, y - 16))


def dibujar_hud(pantalla, jugador, largo):
    """TODO (P2): estado y metros del jugador."""
    fuente = pygame.font.SysFont(None, 28)
    txt = f"Estado: {jugador.moore.nombre_estado}  |  Casillero: {jugador.afd.posicion}/{largo}"
    pantalla.blit(fuente.render(txt, True, (255, 255, 255)), (20, 20))


def dibujar_beat(pantalla, beat, ahora):
    """TODO (P3): círculo que se achica hasta t_objetivo."""
    if beat is None:
        return
    restante = beat.t_objetivo - ahora
    radio = max(10, min(80, 10 + restante // 8))
    pygame.draw.circle(pantalla, (255, 255, 255), (ANCHO // 2, 520), radio, 3)
    fuente = pygame.font.SysFont(None, 36)
    pantalla.blit(fuente.render(beat.tecla, True, (255, 255, 255)), (ANCHO // 2 - 30, 508))


def dibujar_feedback(pantalla, precision):
    if precision is None:
        return
    fuente = pygame.font.SysFont(None, 48)
    img = fuente.render(TEXTO_FEEDBACK[precision], True, COLORES_FEEDBACK[precision])
    pantalla.blit(img, (ANCHO // 2 - img.get_width() // 2, 440))


def dibujar_texto_centrado(pantalla, texto, y, tam=48):
    fuente = pygame.font.SysFont(None, tam)
    img = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(img, (ANCHO // 2 - img.get_width() // 2, y))
