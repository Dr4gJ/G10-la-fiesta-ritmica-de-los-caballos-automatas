import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from precision import evaluar


def test_umbrales():
    assert evaluar(1000, 1000) == "E"
    assert evaluar(1100, 1000) == "B"
    assert evaluar(1250, 1000) == "M"
    assert evaluar(1400, 1000) == "F"
    assert evaluar(1000, 1000, tecla_ok=False) == "F"
