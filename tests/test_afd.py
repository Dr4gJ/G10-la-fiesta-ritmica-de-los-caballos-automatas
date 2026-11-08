import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from afd import AFD

# Tabla del informe (filas q0..q8; columnas R, 0, 1, 2, 3)
INFORME = [
    [0, 0, 1, 2, 3], [0, 1, 2, 3, 4], [1, 2, 3, 4, 5], [2, 3, 4, 5, 6],
    [3, 4, 5, 6, 7], [4, 5, 6, 7, 8], [5, 6, 7, 8, 8], [6, 7, 8, 8, 8],
    [8, 8, 8, 8, 8],
]


def test_tabla_igual_al_informe():
    t = AFD(8).tabla()
    for p, fila in enumerate(INFORME):
        for s, destino in zip(["R", 0, 1, 2, 3], fila):
            assert t[f"q{p}"][s] == f"q{destino}", (p, s)


def test_meta_absorbente_y_aceptacion():
    a = AFD(8)
    for s in (3, 3, 2):
        a.step(s)
    assert a.aceptado() and a.step("R") == 8


def test_largo_parametrizable():
    a = AFD(12); a.step(3)
    assert a.estado == "q3" and not a.aceptado()
