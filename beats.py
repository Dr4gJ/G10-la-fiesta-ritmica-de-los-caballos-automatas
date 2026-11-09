"""Generación de beats"""
import random
from dataclasses import dataclass

TECLAS = ("LEFT", "UP", "RIGHT", "DOWN")

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

# TODO (P3): intervalos de beat variabls