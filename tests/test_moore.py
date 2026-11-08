import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from moore import Moore, TRANSICION, SALIDA


def test_inicio_quieto():
    m = Moore()
    assert m.estado == "q0" and m.salida == 0


def test_perdido_y_recuperacion():
    m = Moore()
    assert m.step("F") == "R"      # q0 --F--> q4
    assert m.step("B") == 0        # q4 --B--> q0
    assert m.step("E") == 2        # q0 --E--> q2


def test_galopando_se_mantiene():
    m = Moore(); m.estado = "q3"
    assert m.step("E") == 3 and m.step("B") == 3


# TODO (P1): un test por cada una de las 20 transiciones de la tabla del informe
