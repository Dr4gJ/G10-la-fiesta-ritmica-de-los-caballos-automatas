"""Generación de beats (teclas pedidas). PERSONA 3."""
import random
from dataclasses import dataclass

TECLAS = ("LEFT", "UP", "RIGHT", "DOWN")  # nombres; juego.py los mapea a pygame.K_*


@dataclass
class Beat:
    tecla: str
    t_creacion: int
    t_objetivo: int          # ms desde el inicio de la carrera
    resuelto: bool = False


def generar_beat(t_creacion, t_objetivo, rng=random):
    return Beat(tecla=rng.choice(TECLAS),
                t_creacion=t_creacion,
                t_objetivo=t_objetivo)

# TODO (Persona 3): dificultad (intervalo variable), anillo que se achica, etc.
