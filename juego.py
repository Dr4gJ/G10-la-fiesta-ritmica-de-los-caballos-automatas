import pygame
import os
import random
import ui
from beats import generar_beat
from caballo import Caballo
from precision import evaluar, UMBRAL_M

NOMBRE_JUEGO = "¡La Fiesta Rítmica de los Caballos Autómatas!"
LARGO_PISTA = 10
INTERVALO_MS = 1000          # tiempo entre beats
VENTANA_MS = UMBRAL_M        # pasado este tiempo sin tecla -> Fallo
TECLAS_PYGAME = {"LEFT": pygame.K_LEFT, "UP": pygame.K_UP,
                "RIGHT": pygame.K_RIGHT, "DOWN": pygame.K_DOWN}

RUTA_ASSETS = os.path.join(os.path.dirname(__file__), "assets")
RUTA_MUSICA = os.path.join(RUTA_ASSETS, "musica_carreritmica.mp3")


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


def cargar_sonido(nombre_base):
    """Carga un sonido buscando extensiones comunes (.wav, .mp3, .ogg) en assets."""
    for ext in (".wav", ".mp3", ".ogg"):
        p = os.path.join(RUTA_ASSETS, f"{nombre_base}{ext}")
        if os.path.exists(p):
            return pygame.mixer.Sound(p)
    return None


def reproducir_musica():
    """Reinicia y reproduce la música de fondo desde el segundo 0, deteniendo efectos previos."""
    pygame.mixer.stop()  # Detiene sonidos que hayan quedado sonando (victoria, derrota, etc.)
    if os.path.exists(RUTA_MUSICA):
        pygame.mixer.music.load(RUTA_MUSICA)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)


def iniciar_partida():
    """Genera nueva carrera y configura la cuenta regresiva de 3 segundos."""
    nuevos_caballos = nueva_carrera()
    t_inicio_carrera = pygame.time.get_ticks() + 3000
    primer_beat = generar_beat(t_inicio_carrera, t_inicio_carrera + INTERVALO_MS)
    return nuevos_caballos, nuevos_caballos[0], t_inicio_carrera, primer_beat


def clave_desempate(c):
    """Criterio de desempate por velocidad del último movimiento."""
    paso = c.ultimo_movimiento
    return -1 if paso == "R" else int(paso)


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ui.ANCHO, ui.ALTO))
    pygame.display.set_caption(NOMBRE_JUEGO)
    reloj = pygame.time.Clock()

    pygame.mixer.init()
    snd_victoria = cargar_sonido("victoria")
    snd_derrota = cargar_sonido("caballo_derrotado")
    snd_easter_egg = cargar_sonido("easter_egg_derrota")

    reproducir_musica()

    caballos, jugador, t_carrera, beat = iniciar_partida()
    ganador = None
    sonido_fin_reproducido = False
    corriendo = True

    while corriendo:
        ahora = pygame.time.get_ticks()
        precision = None

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_r and ganador:
                caballos, jugador, t_carrera, beat = iniciar_partida()
                ganador = None
                sonido_fin_reproducido = False
                reproducir_musica()
            elif ev.type == pygame.KEYDOWN and not ganador and ahora >= t_carrera and beat:
                if abs(ahora - beat.t_objetivo) <= VENTANA_MS or ahora < beat.t_objetivo:
                    ok = ev.key == TECLAS_PYGAME[beat.tecla]
                    precision = evaluar(ahora, beat.t_objetivo, ok)

        # Solo generar beats y evaluar fallos si la carrera ya arrancó
        if not ganador and ahora >= t_carrera and beat and precision is None and ahora > beat.t_objetivo + VENTANA_MS:
            precision = "F"                   # no ingresó a tiempo

        if precision:
            ronda(caballos, precision)
            beat = generar_beat(ahora, ahora + INTERVALO_MS)
            llegaron = [c for c in caballos if c.llego]
            if llegaron:
                ganador = max(llegaron, key=clave_desempate)
                pygame.mixer.music.pause()
                if not sonido_fin_reproducido:
                    sonido_fin_reproducido = True
                    if not ganador.bot:
                        if snd_victoria:
                            snd_victoria.play()
                    else:
                        # 15% de probabilidad de que el caballo se enoje (easter egg)
                        if random.random() < 0.15 and snd_easter_egg:
                            snd_easter_egg.play()
                        elif snd_derrota:
                            snd_derrota.play()

        ui.dibujar_pista(pantalla, caballos, LARGO_PISTA)
        ui.dibujar_hud(pantalla, jugador, LARGO_PISTA)
        if ganador:
            fondo = (30, 130, 60) if not ganador.bot else (150, 30, 30)   # verde si ganás, rojo si no
            ui.dibujar_cartel(pantalla, f"¡Ganó {ganador.nombre}!  (R para reiniciar)", 300, fondo)
        elif ahora < t_carrera:
            segundos_restantes = int((t_carrera - ahora) / 1000) + 1
            ui.dibujar_cuenta_regresiva(pantalla, segundos_restantes)
        else:
            ui.dibujar_beat(pantalla, beat, ahora)
        ui.dibujar_feedback(pantalla, jugador.ultima_precision)

        pygame.display.flip()
        reloj.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
