import pygame
import sprites
import pathlib

ANCHO, ALTO = 900, 600
MARGEN_X = 80
INICIO_X, FIN_X = 170, ANCHO - 60
COLOR_FONDO = (30, 120, 50)
COLORES_FEEDBACK = {"E": (5, 235, 5), "B": (120, 220, 120), "M": (240, 160, 60), "F": (230, 60, 60)}
TEXTO_FEEDBACK = {"E": "¡Excelente!", "B": "Bueno", "M": "Malo", "F": "Fallo"}
VECTOR_FLECHAS = { # para dibujar las flechas
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

_fondo_img = None

def _fondo():
    global _fondo_img
    if _fondo_img is None:
        ruta = pathlib.Path(__file__).parent / "assets" / "fondo.png"
        try:
            img = pygame.image.load(ruta).convert()
            _fondo_img = pygame.transform.smoothscale(img, (ANCHO, ALTO))
        except (FileNotFoundError, pygame.error):
            _fondo_img = pygame.Surface((ANCHO, ALTO))
            _fondo_img.fill(COLOR_FONDO)
    return _fondo_img

def _profundidad(caballos):
    """[(caballo, alto, y_pie)] de atrás hacia adelante; el jugador queda último."""
    orden = [c for c in caballos if c.bot] + [c for c in caballos if not c.bot]
    n = len(orden)
    res = []
    for i, c in enumerate(orden):
        t = i / (n - 1) if n > 1 else 1      # 0 = fondo, 1 = frente
        alto = int(64 + 64 * t)               # 64 (bot del fondo) .. 128 (jugador)
        y_pie = int(260 + 140 * t)            # 260 .. 400
        res.append((c, alto, y_pie))
    return res


def x_de_posicion(pos, largo):
    return INICIO_X + (FIN_X - INICIO_X) * pos / largo


def dibujar_pista(pantalla, caballos, largo):
    pantalla.blit(_fondo(), (0, 0))
    x_meta = int(x_de_posicion(largo, largo))
    pygame.draw.line(pantalla, (255, 255, 255), (x_meta, 200), (x_meta, 430), 4)
    for c, alto, y_pie in _profundidad(caballos):
        dibujar_caballo(pantalla, c, alto, y_pie, largo)

COLOR_ETIQUETA_JUGADOR = (20, 50, 170)   # azul oscuro
COLOR_ETIQUETA_BOT = (40, 40, 40)        # gris oscuro


_fuentes = {}


def _fuente(tam):
    if tam not in _fuentes:
        _fuentes[tam] = pygame.font.SysFont(None, tam)
    return _fuentes[tam]


def _etiqueta(pantalla, texto, x, y, fondo, borde=None, tam=22, pad=(12, 6), centrado=False):
    img = _fuente(tam).render(texto, True, (255, 255, 255))
    rect = img.get_rect(midtop=(x, y)) if centrado else img.get_rect(topleft=(x, y))
    rect = rect.inflate(*pad)
    pygame.draw.rect(pantalla, fondo, rect, border_radius=8)
    if borde:
        pygame.draw.rect(pantalla, borde, rect, 2, border_radius=8)
    pantalla.blit(img, img.get_rect(center=rect.center))

def dibujar_caballo(pantalla, caballo, alto, y_pie, largo):
    color = caballo.color if caballo.bot else None
    img = sprites.sprite(caballo.moore.estado, color, alto,
                         desfase=hash(caballo.nombre) % 300)
    x = int(x_de_posicion(caballo.afd.posicion, largo)) - img.get_width()  # nariz en x
    y = y_pie - img.get_height()
    pantalla.blit(img, (x, y))

    txt = f"{caballo.nombre}: {caballo.moore.nombre_estado}"
    if caballo.bot:
        _etiqueta(pantalla, txt, x, y - 22, COLOR_ETIQUETA_BOT)
    else:
        _etiqueta(pantalla, txt, x, y - 22, COLOR_ETIQUETA_JUGADOR, borde=(255, 215, 0))
    

def dibujar_cartel(pantalla, texto, y, fondo):
    _etiqueta(pantalla, texto, ANCHO // 2, y, fondo, borde=(255, 255, 255),
              tam=48, pad=(40, 24), centrado=True)

def dibujar_hud(pantalla, jugador, largo):
    txt = f"Estado: {jugador.moore.nombre_estado}  |  Casillero: {jugador.afd.posicion}/{largo}"
    _etiqueta(pantalla, txt, 20, 20, COLOR_ETIQUETA_JUGADOR,
              borde=(255, 215, 0), tam=28, pad=(16, 10))


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

def dibujar_cuenta_regresiva(pantalla, numero):
    """Muestra un número grande o mensaje para la cuenta regresiva antes de empezar."""
    fuente = pygame.font.SysFont(None, 120)
    texto = str(numero) if numero > 0 else "¡YA!"
    color = (255, 215, 0) if numero > 0 else (50, 255, 50)
    
    img = fuente.render(texto, True, color)
    sombra = fuente.render(texto, True, (0, 0, 0))
    x = ANCHO // 2 - img.get_width() // 2
    y = 200
    pantalla.blit(sombra, (x + 4, y + 4))
    pantalla.blit(img, (x, y))

def dibujar_texto_centrado(pantalla, texto, y, tam=48):
    fuente = pygame.font.SysFont(None, tam)
    img = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(img, (ANCHO // 2 - img.get_width() // 2, y))
