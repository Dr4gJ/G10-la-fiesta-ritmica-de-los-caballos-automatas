"""Define timings e intervalos de los beats"""

UMBRAL_E = 35    # |error| <= E ms  -> Excelente
UMBRAL_B = 80    # <= B ms        -> Bueno
UMBRAL_M = 140   # <= M ms        -> Malo
                 # más que eso o tecla incorrecta -> Fallo


def evaluar(t_input, t_objetivo, tecla_ok=True):
    """Devuelve 'F', 'M', 'B' o 'E'."""
    if not tecla_ok:
        return "F"
    error = abs(t_input - t_objetivo)
    if error <= UMBRAL_E:
        return "E"
    if error <= UMBRAL_B:
        return "B"
    if error <= UMBRAL_M:
        return "M"
    return "F"
