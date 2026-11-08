# Carrera de caballos - Autómatas (TFI Fundamentos Teóricos de Informática)

    pip install -r requirements.txt
    python main.py        # jugar
    pytest                # tests

## Contrato de interfaces (NO cambiar sin avisar al grupo)
- Precisión: str `'F' | 'M' | 'B' | 'E'`
- `Moore.step(precision) -> 0|1|2|3|'R'`   (también `.estado`, `.nombre_estado`, `.reset()`)
- `AFD.step(salida) -> int` (casillero)    (también `.aceptado()`, `.posicion`, `.reset()`)
- `precision.evaluar(t_input_ms, t_objetivo_ms, tecla_ok) -> precisión`
- `Caballo.jugar(precision)` encadena Moore -> AFD
- Los autómatas NO importan pygame.

## Reparto
- P1: moore.py, sprites/animación del caballo (ui.dibujar_caballo), tests/test_moore.py
- P2: afd.py, pista y HUD (ui.dibujar_pista / dibujar_hud), tests/test_afd.py
- P3: precision.py, beats.py, ui.dibujar_beat / dibujar_feedback, tests/test_precision.py
- P4: juego.py, main.py, menú, cuenta regresiva, bots, pantalla de ganador
