import pygame
import ui
from beats import generar_beat
from caballo import Caballo
from precision import evaluar, UMBRAL_M

NOMBRE_JUEGO = "¡La Fiesta Rítmica de los Caballos Autómatas!"
LARGO_PISTA = 40
INTERVALO_MS = 1000          # tiempo entre beats
VENTANA_MS = UMBRAL_M        # pasado este tiempo sin tecla -> Fallo
TECLAS_PYGAME = {"LEFT": pygame.K_LEFT, "UP": pygame.K_UP,
                "RIGHT": pygame.K_RIGHT, "DOWN": pygame.K_DOWN}


def nueva_carrera():
    return [
        Caballo("Usuario", (0,0,0), LARGO_PISTA),
        Caballo("Bot 1", (149, 52, 235), LARGO_PISTA, bot=True, habilidad=0.4),
        Caballo("Bot 2", (255, 51, 187), LARGO_PISTA, bot=True, habilidad=0.6),
        Caballo("Bot 3", (51, 238, 255), LARGO_PISTA, bot=True, habilidad=0.7)
    ]


def ronda(caballos, precision_jugador):
    for c in caballos:
        c.jugar(precision_jugador if not c.bot else c.precision_bot())


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ui.ANCHO, ui.ALTO))
    pygame.display.set_caption(NOMBRE_JUEGO)
    reloj = pygame.time.Clock()

    caballos = nueva_carrera()
    jugador = caballos[0]
    t0 = pygame.time.get_ticks() + 2000 # TODO (P4): cuenta regresiva
    beat = generar_beat(t0, t0 + INTERVALO_MS) 
    ganador = None
    corriendo = True

    while corriendo:
        ahora = pygame.time.get_ticks()
        precision = None

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_r and ganador:
                caballos = nueva_carrera(); jugador = caballos[0]
                beat = generar_beat(pygame.time.get_ticks(), pygame.time.get_ticks() + 1000); ganador = None
            elif ev.type == pygame.KEYDOWN and not ganador and beat:
                if abs(ahora - beat.t_objetivo) <= VENTANA_MS or ahora < beat.t_objetivo:
                    ok = ev.key == TECLAS_PYGAME[beat.tecla]
                    precision = evaluar(ahora, beat.t_objetivo, ok)

        if not ganador and beat and precision is None and ahora > beat.t_objetivo + VENTANA_MS:
            precision = "F"                   # no ingresó a tiempo

        if precision:
            ronda(caballos, precision)
            beat = generar_beat(ahora, ahora + INTERVALO_MS)
            llegaron = [c for c in caballos if c.llego]
            if llegaron:
                ganador = llegaron[0]         # TODO (P4): desempate si llegan 2 a la vez

        ui.dibujar_pista(pantalla, caballos, LARGO_PISTA)
        ui.dibujar_hud(pantalla, jugador, LARGO_PISTA)
        if ganador:
            fondo = (30, 130, 60) if not ganador.bot else (150, 30, 30)   # verde si ganás, rojo si no
            ui.dibujar_cartel(pantalla, f"¡Ganó {ganador.nombre}!  (R para reiniciar)", 300, fondo)
        else:
            ui.dibujar_beat(pantalla, beat, ahora)
        ui.dibujar_feedback(pantalla, jugador.ultima_precision)

        pygame.display.flip()
        reloj.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
