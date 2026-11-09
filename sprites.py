import pathlib
import pygame

ASSETS = pathlib.Path(__file__).parent / "assets"
PERIODO_MS = {"q0": 700, "q1": 400, "q2": 250, "q3": 120, "q4": 300}
PIXEL_ART = True   # True: escalado nítido. False: suavizado (para dibujos HD)

_orig = {}    # (estado, cuadro) -> Surface original
_cache = {}   # (estado, cuadro, color, alto) -> Surface escalada


def _original(estado, cuadro):
    clave = (estado, cuadro)
    if clave not in _orig:
        ruta = ASSETS / f"caballo_{estado}_{cuadro}.png"
        _orig[clave] = pygame.image.load(ruta).convert_alpha()
    return _orig[clave]


def _escalar(img, alto):
    ancho = round(img.get_width() * alto / img.get_height())
    f = pygame.transform.scale if PIXEL_ART else pygame.transform.smoothscale
    return f(img, (ancho, alto))


INTENSIDAD = 0.5 

def _tintar(img, color):
    capa = img.copy()
    capa.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)  # silueta negra, conserva alfa
    capa.fill((*color, 0), special_flags=pygame.BLEND_RGBA_ADD)      # silueta del color elegido
    capa.set_alpha(int(255 * INTENSIDAD))
    salida = img.copy()
    salida.blit(capa, (0, 0))
    return salida


def sprite(estado, color, alto, ahora=None, desfase=0):
    """Cuadro actual del caballo, escalado a `alto` píxeles de alto."""
    ahora = (pygame.time.get_ticks() if ahora is None else ahora) + desfase
    cuadro = (ahora // PERIODO_MS[estado]) % 2 + 1
    clave = (estado, cuadro, color, alto)
    if clave not in _cache:
        img = _escalar(_original(estado, cuadro), alto)
        if color is not None:
            img = _tintar(img, color)
        _cache[clave] = img
    return _cache[clave]