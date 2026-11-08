"""Un caballo = una Moore + un AFD. Une los dos autómatas (sin pygame)."""
import random
from moore import Moore
from afd import AFD


class Caballo:
    def __init__(self, nombre, color, largo=8, bot=False, habilidad=0.5):
        self.nombre = nombre
        self.color = color
        self.bot = bot
        self.habilidad = habilidad   # 0..1, solo para bots
        self.moore = Moore()
        self.afd = AFD(largo)
        self.ultima_precision = None

    def jugar(self, precision):
        """precision -> Moore -> AFD. Devuelve metros (salida de la Moore)."""
        self.ultima_precision = precision
        salida = self.moore.step(precision)
        self.afd.step(salida)
        return salida

    def precision_bot(self, rng=random):
        h = self.habilidad
        r = rng.random()
        pesos = [("E", h * 0.5), ("B", 0.3), ("M", 0.25), ("F", (1 - h) * 0.3)]
        total = sum(p for _, p in pesos)
        acum = 0
        for letra, p in pesos:
            acum += p / total
            if r <= acum:
                return letra
        return "M"

    @property
    def llego(self):
        return self.afd.aceptado()

    def reset(self):
        self.moore.reset()
        self.afd.reset()
        self.ultima_precision = None
