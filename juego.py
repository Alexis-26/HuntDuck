import pygame
from patos import Pato
from mano import DetectorMano
import time
 # version disparo automatico
class Juego:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 768, 720
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("DUCK HUNT")

        self.fps = 60
        self.timer = pygame.time.Clock()
        self.running = True

        self.detector_mano = DetectorMano(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Cargar imágenes
        self.background = pygame.image.load("assets/bg/sprite_bg.png")
        self.clouds_up = pygame.image.load("assets/bg/sprite_bg_clouds1.png")
        self.clouds_down = pygame.image.load("assets/bg/sprite_bg_clouds2.png")
        self.ground = pygame.image.load("assets/bg/sprite_bg_ground.png")
        self.puntero = pygame.image.load("assets/ui/sprite_aim.png").convert_alpha()
        pygame.mouse.set_visible(False)

        # Cargar sonidos
        pygame.mixer.music.load("assets/ui/MeltdownTheme.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.sonido_disparo = pygame.mixer.Sound("assets/ui/disparo.mp3")
        self.sonido_disparo.set_volume(0.7)
        self.sonido_pato = pygame.mixer.Sound("assets/duck/duck.mp3")
        self.sonido_pato.set_volume(0.7)

        # Variables del juego
        self.nivel = 1
        self.patos_en_nivel = 5
        self.velocidad_patos = 5
        self.patos = []
        self.patos_mortos = 0
        self.tiempo_limite = 30 * 1000  # ms
        self.tiempo_restante = self.tiempo_limite
        self.tiempo_entre_patos = 1500
        self.tiempo_ultimo_pato = pygame.time.get_ticks()
        # Guardar el tiempo de inicio del juego
        self.tiempo_inicio = pygame.time.get_ticks()

        self.generar_patos()

    def generar_patos(self):
        if len(self.patos) < self.patos_en_nivel:
            pato = Pato()
            pato.velocidad = self.velocidad_patos
            self.patos.append(pato)

    def siguiente_nivel(self):
        self.nivel += 1
        self.patos_en_nivel += 2
        self.velocidad_patos += 0.5
        self.patos = []
        self.patos_mortos = 0
        self.tiempo_restante = self.tiempo_limite
        self.tiempo_inicio = pygame.time.get_ticks()  # 🔥 Reinicia el tiempo base aquí
        self.generar_patos()

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def actualizar(self):
        # Calcular el tiempo transcurrido desde el inicio del juego
        tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_inicio
        self.tiempo_restante = max(0, self.tiempo_limite - tiempo_transcurrido)

        self.detector_mano.actualizar()
        cursor_pos = self.detector_mano.cursor

        # Detectar el contacto del cursor con los patos
        for pato in self.patos:
            if pato.rect.collidepoint(cursor_pos) and not pato.muerto:
                distancia = ((pato.rect.centerx - cursor_pos[0])**2 + (pato.rect.centery - cursor_pos[1])**2)**0.5
                if distancia < 20:  # Si el cursor está lo suficientemente cerca
                    pato.muerto = True
                    pato.frame_actual = 0
                    pato.tiempo_animacion = 0
                    pato.vel_caida = 0
                    self.sonido_pato.play()  # Suena el pato al ser disparado
                    self.sonido_disparo.play()  # Sonido de disparo
                    break  # Solo dispara a un pato por actualización

        self.patos_mortos = sum(1 for p in self.patos if p.muerto)
        if self.patos_mortos == len(self.patos):
            self.siguiente_nivel()

        if pygame.time.get_ticks() - self.tiempo_ultimo_pato > self.tiempo_entre_patos:
            self.generar_patos()
            self.tiempo_ultimo_pato = pygame.time.get_ticks()

        for pato in self.patos:
            pato.mover()
            pato.actualizar_animacion()

        if self.tiempo_restante <= 0:
            print("¡Tiempo agotado! Has perdido.")
            self.running = False

    def dibujar(self):
        self.SCREEN.blit(self.background, (0, 0))
        self.SCREEN.blit(self.clouds_up, (0, 0))
        self.SCREEN.blit(self.clouds_down, (0, 0))

        for pato in self.patos:
            pato.dibujar(self.SCREEN)

        self.SCREEN.blit(self.ground, (0, 0))

        # Dibujar el puntero en la pantalla
        puntero_rect = self.puntero.get_rect(center=self.detector_mano.cursor)
        self.SCREEN.blit(self.puntero, puntero_rect.topleft)

        font = pygame.font.SysFont(None, 36)
        self.SCREEN.blit(font.render(f"Nivel: {self.nivel}", True, (0, 0, 0)), (10, 10))
        self.SCREEN.blit(font.render(f"Tiempo: {int(self.tiempo_restante / 1000)}", True, (0, 0, 0)), (self.SCREEN_WIDTH - 150, 10))

    def ejecutar(self):
        while self.running:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            pygame.display.flip()
            self.timer.tick(self.fps)

        self.detector_mano.cerrar()
        pygame.quit()

# Version dos mecanicas de disparo y apuntado
# class Juego:
#     def __init__(self):
#         pygame.init()
#         self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 768, 720
#         self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
#         pygame.display.set_caption("DUCK HUNT")

#         self.fps = 60
#         self.timer = pygame.time.Clock()
#         self.running = True

#         self.detector_mano = DetectorMano(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

#         # Cargar imágenes
#         self.background = pygame.image.load("assets/bg/sprite_bg.png")
#         self.clouds_up = pygame.image.load("assets/bg/sprite_bg_clouds1.png")
#         self.clouds_down = pygame.image.load("assets/bg/sprite_bg_clouds2.png")
#         self.ground = pygame.image.load("assets/bg/sprite_bg_ground.png")
#         self.puntero = pygame.image.load("assets/ui/sprite_aim.png").convert_alpha()
#         pygame.mouse.set_visible(False)

#         # Cargar sonidos
#         pygame.mixer.music.load("assets/ui/MeltdownTheme.wav")
#         pygame.mixer.music.set_volume(0.5)
#         pygame.mixer.music.play(-1)

#         self.sonido_disparo = pygame.mixer.Sound("assets/ui/disparo.mp3")
#         self.sonido_disparo.set_volume(0.7)
#         self.sonido_pato = pygame.mixer.Sound("assets/duck/duck.mp3")
#         self.sonido_pato.set_volume(0.7)

#         # Variables del juego
#         self.nivel = 1
#         self.patos_en_nivel = 5
#         self.velocidad_patos = 3
#         self.patos = []
#         self.patos_mortos = 0
#         self.tiempo_limite = 30 * 1000  # ms
#         self.tiempo_restante = self.tiempo_limite
#         self.tiempo_entre_patos = 1500
#         self.tiempo_ultimo_pato = pygame.time.get_ticks()

#         self.ultimo_disparo = 0
#         self.tiempo_disparo = 0.4  # 400 ms

#         self.tiempo_ultimo_disparo = 0
#         self.cooldown_disparo = 0.5  # medio segundo entre disparos


#         self.generar_patos()

#     def generar_patos(self):
#         if len(self.patos) < self.patos_en_nivel:
#             pato = Pato()
#             pato.velocidad = self.velocidad_patos
#             self.patos.append(pato)

#     def siguiente_nivel(self):
#         self.nivel += 1
#         self.patos_en_nivel += 2
#         self.velocidad_patos += 0.5
#         self.patos = []
#         self.patos_mortos = 0
#         self.tiempo_restante = self.tiempo_limite
#         self.generar_patos()

#     def manejar_eventos(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False

#     def actualizar(self):
#         self.tiempo_restante -= 1000 / self.fps
#         self.detector_mano.actualizar()
#         cursor_pos = self.detector_mano.cursor

#         if self.detector_mano.disparo:
#             self.sonido_disparo.play()
#             for pato in self.patos:
#                 if pato.rect.collidepoint(cursor_pos) and not pato.muerto:
#                     distancia = ((pato.rect.centerx - cursor_pos[0])**2 + (pato.rect.centery - cursor_pos[1])**2)**0.5
#                     if distancia < 100:
#                         ahora = time.time()
#                         if ahora - self.ultimo_disparo < self.tiempo_disparo:
#                             if ahora - self.tiempo_ultimo_disparo > self.cooldown_disparo:
#                                 pato.muerto = True
#                                 pato.frame_actual = 0
#                                 pato.tiempo_animacion = 0
#                                 pato.vel_caida = 0
#                                 self.sonido_pato.play()
#                                 break
#                             self.ultimo_disparo = 0  # reinicia el doble toque
#                         self.ultimo_disparo = ahora

#         self.patos_mortos = sum(1 for p in self.patos if p.muerto)
#         if self.patos_mortos == len(self.patos):
#             self.siguiente_nivel()

#         if pygame.time.get_ticks() - self.tiempo_ultimo_pato > self.tiempo_entre_patos:
#             self.generar_patos()
#             self.tiempo_ultimo_pato = pygame.time.get_ticks()

#         for pato in self.patos:
#             pato.mover()
#             pato.actualizar_animacion()

#         if self.tiempo_restante <= 0:
#             print("¡Tiempo agotado! Has perdido.")
#             self.running = False

#     def dibujar(self):
#         self.SCREEN.blit(self.background, (0, 0))
#         self.SCREEN.blit(self.clouds_up, (0, 0))
#         self.SCREEN.blit(self.clouds_down, (0, 0))

#         for pato in self.patos:
#             pato.dibujar(self.SCREEN)

#         self.SCREEN.blit(self.ground, (0, 0))
#         # self.SCREEN.blit(self.puntero, self.detector_mano.cursor)
#         # Ajustar la posición del puntero para centrarlo en el cursor
#         puntero_rect = self.puntero.get_rect(center=self.detector_mano.cursor)
#         self.SCREEN.blit(self.puntero, puntero_rect.topleft)

#         font = pygame.font.SysFont(None, 36)
#         self.SCREEN.blit(font.render(f"Nivel: {self.nivel}", True, (0, 0, 0)), (10, 10))
#         self.SCREEN.blit(font.render(f"Tiempo: {int(self.tiempo_restante / 1000)}", True, (0, 0, 0)), (self.SCREEN_WIDTH - 150, 10))

#     def ejecutar(self):
#         while self.running:
#             self.manejar_eventos()
#             self.actualizar()
#             self.dibujar()
#             pygame.display.flip()
#             self.timer.tick(self.fps)

#         self.detector_mano.cerrar()
#         pygame.quit()

