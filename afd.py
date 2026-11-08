"""AFD de la meta. PERSONA 2.

Pura: NO importa pygame. Estados q0..q{largo}; final = q{largo}.
Entrada: salida de la Moore (0, 1, 2, 3, 'R').
Regla (equivale a la tabla del informe): pos + avance, tope en la meta;
'R' retrocede 1 sin bajar de 0; la meta es absorbente.
"""

SIMBOLOS = ("R", 0, 1, 2, 3)


class AFD:
    def __init__(self, largo=8):
        self.largo = largo
        self.pos = 0

    def reset(self):
        self.pos = 0

    @property
    def estado(self):
        return f"q{self.pos}"

    @property
    def posicion(self):
        return self.pos

    def aceptado(self):
        return self.pos == self.largo

    def _delta(self, pos, simbolo):
        if simbolo not in SIMBOLOS:
            raise ValueError(f"Símbolo inválido: {simbolo!r}")
        if pos == self.largo:
            return pos
        if simbolo == "R":
            return max(0, pos - 1)
        return min(self.largo, pos + simbolo)

    def step(self, simbolo):
        self.pos = self._delta(self.pos, simbolo)
        return self.pos

    def tabla(self):
        """{estado: {simbolo: estado}} para comparar con el informe."""
        return {
            f"q{p}": {s: f"q{self._delta(p, s)}" for s in SIMBOLOS}
            for p in range(self.largo + 1)
        }
