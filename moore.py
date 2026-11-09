"""Máquina de Moore del caballo. PERSONA 1.

Pura: NO importa pygame ni usa tiempo. Entrada: 'F','M','B','E'.
Salida (función g del estado): 0, 1, 2, 3 o 'R'.
"""

from automata.fa.dfa import DFA

ENTRADAS = ("F", "M", "B", "E")

NOMBRES = {
    "q0": "Quieto",
    "q1": "Caminando",
    "q2": "Trotando",
    "q3": "Galopando",
    "q4": "Perdido",
}

# f: Q x ΣE -> Q  (copiada de la tabla del informe; VERIFICAR contra JFLAP)
TRANSICION = {
    "q0": {"F": "q4", "M": "q0", "B": "q1", "E": "q2"},
    "q1": {"F": "q0", "M": "q0", "B": "q1", "E": "q2"},
    "q2": {"F": "q1", "M": "q1", "B": "q2", "E": "q3"},
    "q3": {"F": "q2", "M": "q2", "B": "q3", "E": "q3"},
    "q4": {"F": "q4", "M": "q4", "B": "q0", "E": "q1"},
}

# g: Q -> ΣS
SALIDA = {"q0": 0, "q1": 1, "q2": 2, "q3": 3, "q4": "R"}


class Moore:
    def __init__(self):
        self.dfa = DFA(
            states = set(NOMBRES.keys()),
            input_symbols = set(ENTRADAS),
            transitions = TRANSICION,
            initial_state = "q0",
            final_states = set(NOMBRES.keys())
        )
        self.reset()

    def reset(self): 
        self.estado = self.dfa.initial_state
        self.historial = ""

    @property
    def nombre_estado(self):
        "Devuelve el nombre del estado actual"
        return NOMBRES[self.estado]

    @property
    def salida(self):
        "Salida g(q) del estado actual"
        return SALIDA[self.estado]

    def paso(self, entrada): 
        "'F'|'M'|'B'|'E'| mediante automata-lib y devuelve la salida del nuevo estado"
        if entrada not in self.dfa.input_symbols:
            raise ValueError(f"Entrada invalida: {entrada!r}")

        self.historial += entrada
        self.estado = self.dfa.read_input(self.historial)
        return self.salida

    # TODO (Persona 1): lo que haga falta para animar (ej. velocidad de frames por estado)
