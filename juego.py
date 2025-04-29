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
        self.mostrar_inicio = True
        self.mostrar_final = False

        self.detector_mano = DetectorMano(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Cargar imágenes
        self.background = pygame.image.load("assets/bg/sprite_bg.png")
        self.clouds_up = pygame.image.load("assets/bg/sprite_bg_clouds1.png")
        self.clouds_down = pygame.image.load("assets/bg/sprite_bg_clouds2.png")
        self.ground = pygame.image.load("assets/bg/sprite_bg_ground.png")
        self.puntero = pygame.image.load("assets/ui/sprite_aim.png").convert_alpha()
        #pygame.mouse.set_visible(False)

        # Fuentes
        self.font_menu = pygame.font.Font("assets\Retro Gaming.ttf", size=30)
        self.font_titulo = pygame.font.Font("assets\Retro Gaming.ttf", size=60)
        self.cazadores = pygame.image.load("assets/cazadores.png").convert_alpha()
        self.de = pygame.image.load("assets/de.png").convert_alpha()
        self.rostros = pygame.image.load("assets/rostros.png").convert_alpha()
        self.game = pygame.image.load("assets/game.png").convert_alpha()
        self.over = pygame.image.load("assets/over.png").convert_alpha()

        # Botones
        # Crear el texto del botón
        self.texto_jugar = self.font_menu.render("Jugar", True, "#FFFFFF")  # Texto blanco
        self.texto_jugar_sombra = self.font_menu.render("Jugar", True, "#000000")  # Sombra negra

        # Obtener el rectángulo del texto
        self.rect_texto_jugar = self.texto_jugar.get_rect()
        self.rect_texto_jugar.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100)  # Centrado abajo

        self.texto_salir = self.font_menu.render("Salir", True, "#FFFFFF")  # Texto blanco
        self.texto_salir_sombra = self.font_menu.render("Salir", True, "#000000")  # Sombra negra

        # Obtener el rectángulo del texto
        self.rect_texto_salir = self.texto_salir.get_rect()
        self.rect_texto_salir.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100)  # Centrado abajo

        # Crear el rectángulo del botón más grande que el texto
        self.boton_jugar = self.rect_texto_jugar.inflate(40, 20)  # Más ancho y más alto
        self.boton_salir = self.rect_texto_salir.inflate(40, 20)  # Más ancho y más alto

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

        self.patos_inicio = [Pato() for _ in range(5)]  # Crea 5 patos
        self.generar_patos()

    def pantalla_inicio(self):
        self.SCREEN.blit(self.background, (0, 0))
        self.SCREEN.blit(self.clouds_up, (0, 0))
        self.SCREEN.blit(self.clouds_down, (0, 0))
        self.SCREEN.blit(self.ground, (0, 0))
        # Dibujar patos
        for pato in self.patos_inicio:
            pato.mover()
            pato.actualizar_animacion()
            pato.chequear_tierra()
            pato.dibujar(self.SCREEN)

        # Obtener el rectángulo del sprite/texto
        rect_cazadores = self.cazadores.get_rect()
        rect_de = self.de.get_rect()
        rect_rostros = self.rostros.get_rect()
        # Centrar el rectángulo en la pantalla
        rect_cazadores.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        rect_de.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        rect_rostros.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        # Opcional: Si quieres moverlo un poco hacia arriba o abajo
        rect_cazadores.y -= 200  # por ejemplo, mover 100 píxeles hacia arriba
        rect_de.y -= 100  # por ejemplo, mover 100 píxeles hacia arriba
        rect_rostros.y -= 0  # por ejemplo, mover 100 píxeles hacia arriba
        # Dibujarlo
        self.SCREEN.blit(self.cazadores, rect_cazadores)
        self.SCREEN.blit(self.de, rect_de)
        self.SCREEN.blit(self.rostros, rect_rostros)

        # Dibujar el botón (fondo)
        pygame.draw.rect(self.SCREEN, "#FB6222", self.boton_jugar, border_radius=10)  # Botón blanco

        # Dibujar la sombra del texto
        self.SCREEN.blit(self.texto_jugar_sombra, (self.rect_texto_jugar.x + 2, self.rect_texto_jugar.y + 2))

        # Dibujar el texto encima
        self.SCREEN.blit(self.texto_jugar, self.rect_texto_jugar.topleft)
        pygame.display.update()

    def pantalla_final(self):
        self.SCREEN.blit(self.background, (0, 0))
        self.SCREEN.blit(self.clouds_up, (0, 0))
        self.SCREEN.blit(self.clouds_down, (0, 0))
        self.SCREEN.blit(self.ground, (0, 0))
        # Dibujar perro

        # Obtener el rectángulo del sprite/texto
        rect_game = self.game.get_rect()
        rect_over = self.over.get_rect()
        # Centrar el rectángulo en la pantalla
        rect_game.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        rect_over.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        # Opcional: Si quieres moverlo un poco hacia arriba o abajo
        rect_game.y -= 200  # por ejemplo, mover 100 píxeles hacia arriba
        rect_over.y -= 100  # por ejemplo, mover 100 píxeles hacia arriba
    
        # Dibujarlo
        self.SCREEN.blit(self.game, rect_game)
        self.SCREEN.blit(self.over, rect_over)

        # Dibujar el botón (fondo)
        pygame.draw.rect(self.SCREEN, "#FB6222", self.boton_salir, border_radius=10)  # Botón blanco

        # Dibujar la sombra del texto
        self.SCREEN.blit(self.texto_salir_sombra, (self.rect_texto_salir.x + 2, self.rect_texto_salir.y + 2))

        # Dibujar el texto encima
        self.SCREEN.blit(self.texto_salir, self.rect_texto_salir.topleft)
        pygame.display.update()

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mostrar_inicio and self.boton_jugar.collidepoint(event.pos):
                    self.mostrar_inicio = False
                    self.mostrar_final = False
                    self.tiempo_inicio = pygame.time.get_ticks()
                elif self.mostrar_final and self.boton_salir.collidepoint(event.pos):
                    self.mostrar_final = False
                    self.mostrar_inicio = True
                    self.resetear_juego()


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
            self.mostrar_final = True

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

    def resetear_juego(self):
        self.nivel = 1
        self.patos_en_nivel = 5
        self.velocidad_patos = 5
        self.patos = []
        self.patos_mortos = 0
        self.tiempo_restante = self.tiempo_limite
        self.tiempo_inicio = pygame.time.get_ticks()
        self.generar_patos()


    def ejecutar(self):
        while self.running:
            self.manejar_eventos()
            if self.mostrar_inicio:
                self.pantalla_inicio()

            elif self.mostrar_final:
                self.pantalla_final()

            else:
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

