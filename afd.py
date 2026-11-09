"""AFD control de posición del caballo
Estados q0..q{largo}; final = q{largo}.
Entrada: salida de autómata de Moore (0, 1, 2, 3, 'R').
"""
from automata.fa.dfa import DFA

SIMBOLOS = ("R", "0", "1", "2", "3")


class AFD:
    def __init__(self, largo = 8):
        self.largo = largo
        estados = {f"q{i}" for i in range(largo + 1)}
        transiciones = {f"q{p}" : {s: f"q{self._delta(p, s)}" for s in SIMBOLOS}
                        for p in range(largo + 1)
                        }

        self.dfa = DFA(
            states = estados,
            input_symbols = set(SIMBOLOS),
            transitions = transiciones,
            initial_state = "q0",
            final_states = {f"q{largo}"}
        )

        self.reset()

    def reset(self):
        self._estado = self.dfa.initial_state
        self.historial = ""

    @property
    def estado(self):
        return self._estado

    @property
    def posicion(self):
        return int(self._estado[1:])

    def aceptado(self):
        "Evalua si la secuencia de entradas llego al estado final"
        return self.dfa.accepts_input(self.historial)

    def _delta(self, pos, simbolo):
        if pos == self.largo:
            return pos
        if simbolo == "R":
            return max(0, pos - 1)
        return min(self.largo, pos + int(simbolo))

    def paso(self, simbolo): 
        simbolo_str = str(simbolo)
        if simbolo_str not in self.dfa.input_symbols:
            raise ValueError(f"Simbolo invalido: {simbolo!r}")

        self.historial += simbolo_str
        self._estado = self.dfa.transitions[self._estado][simbolo_str]
        return self.posicion

    def tabla(self):
        "Devuelve la tabla de transiciones generada en el DFA"
        return dict(self.dfa.transitions)