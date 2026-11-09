"""Dibujo (PERSONA 1: sprites/animación del caballo; PERSONA 2: pista y HUD;
PERSONA 3: beat y feedback). Solo LEE el estado, no lo modifica.
Versión inicial con rectángulos; reemplazar por sprites después.
"""
import pygame

ANCHO, ALTO = 900, 600
MARGEN_X = 80
COLOR_FONDO = (30, 120, 50)
COLORES_FEEDBACK = {"E": (5, 235, 5), "B": (120, 220, 120), "M": (240, 160, 60), "F": (230, 60, 60)}
TEXTO_FEEDBACK = {"E": "¡Excelente!", "B": "Bueno", "M": "Malo", "F": "Fallo"}
VECTOR_FLECHAS = {  # direcciones usadas para dibujar la flecha del botón
    "UP": {
        "puntos": lambda cx, cy: [(cx, cy - 18), (cx - 14, cy + 8), (cx + 14, cy + 8)],
        "rect": lambda cx, cy: (cx - 5, cy + 6, 10, 12)
    },
    "DOWN": {
        "puntos": lambda cx, cy: [(cx, cy + 18), (cx - 14, cy - 8), (cx + 14, cy - 8)],
        "rect": lambda cx, cy: (cx - 5, cy - 18, 10, 12)
    },
    "LEFT": {
        "puntos": lambda cx, cy: [(cx - 18, cy), (cx + 8, cy - 14), (cx + 8, cy + 14)],
        "rect": lambda cx, cy: (cx + 6, cy - 5, 12, 10)
    },
    "RIGHT": {
        "puntos": lambda cx, cy: [(cx + 18, cy), (cx - 8, cy - 14), (cx - 8, cy + 14)],
        "rect": lambda cx, cy: (cx - 18, cy - 5, 12, 10)
    }
}


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
    """círculo que se achica hasta t_objetivo."""
    if beat is None:
        return

    centro = (ANCHO // 2, 520)
    radio_objetivo = 35  # radio circulo interno
    
    # Calcular el progreso temporal entre 0.0 (nació) y 1.0 (llegó al objetivo)
    tiempo_total = beat.t_objetivo - beat.t_creacion
    transcurrido = ahora - beat.t_creacion
    
    if tiempo_total > 0:
        progreso = max(0.0, min(1.0, transcurrido / tiempo_total))
    else:
        progreso = 1.0

    radio_inicial = 100
    radio_actual = int(radio_inicial - (radio_inicial - radio_objetivo) * progreso)

    pygame.draw.circle(pantalla, (200, 200, 200), centro, radio_actual, 3) # circulo exterior
    
    pygame.draw.circle(pantalla, (50, 50, 50), centro, radio_objetivo) # circulo central con tecla
    pygame.draw.circle(pantalla, (255, 255, 255), centro, radio_objetivo, 2)

    cx, cy = centro
    cfg = VECTOR_FLECHAS[beat.tecla]
    color_flecha = (255, 255, 255)
    pygame.draw.polygon(pantalla, color_flecha, cfg["puntos"](cx, cy))
    pygame.draw.rect(pantalla, color_flecha, cfg["rect"](cx, cy))

def dibujar_feedback(pantalla, precision):
    if precision is None:
        return
    fuente = pygame.font.SysFont(None, 48)
    img = fuente.render(TEXTO_FEEDBACK[precision], True, COLORES_FEEDBACK[precision])
    sombra = fuente.render(TEXTO_FEEDBACK[precision], True, (0, 0, 0))

    x = ANCHO // 2 - img.get_width() // 2
    y = 440
    pantalla.blit(sombra, (x + 2, y + 2))
    pantalla.blit(img, (x, y))

def dibujar_texto_centrado(pantalla, texto, y, tam=48):
    fuente = pygame.font.SysFont(None, tam)
    img = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(img, (ANCHO // 2 - img.get_width() // 2, y))
