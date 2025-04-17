import pygame
from patos import Pato
from mano import DetectorMano  # Nuevo

class Juego:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()

        # Constantes
        self.SCREEN_WIDTH = 768
        self.SCREEN_HEIGHT = 720
        self.fps = 60
        self.timer = pygame.time.Clock()
        self.detector_mano = DetectorMano(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Configuración de la ventana
        pygame.display.set_caption("DUCK HUNT")
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Cargar fondo y elementos
        self.background = pygame.image.load("assets/bg/sprite_bg.png")
        self.clouds_up = pygame.image.load("assets/bg/sprite_bg_clouds1.png")
        self.clouds_down = pygame.image.load("assets/bg/sprite_bg_clouds2.png")
        self.ground = pygame.image.load("assets/bg/sprite_bg_ground.png")

        # Cargar sonidos
        pygame.mixer.music.load("assets/ui/MeltdownTheme.wav")
        pygame.mixer.music.set_volume(0.5)  # volumen entre 0.0 y 1.0
        pygame.mixer.music.play(-1)  # -1 para que se repita en loop

        self.sonido_disparo = pygame.mixer.Sound("assets/ui/disparo.mp3")
        self.sonido_disparo.set_volume(0.7)  # opcional

        self.sonido_pato = pygame.mixer.Sound("assets/duck/duck.mp3")
        self.sonido_pato.set_volume(0.7)  # opcional

        # Puntero
        self.puntero = pygame.image.load("assets/ui/sprite_aim.png").convert_alpha()
        pygame.mouse.set_visible(False)

        # Inicializar el pato
        self.patos = []
        self.nivel = 1
        self.patos_en_nivel = 5
        self.velocidad_patos = 2
        self.patos_mortos = 0
        self.running = True
        
        # Variables para el temporizador
        self.tiempo_limite = 10  # Tiempo límite en segundos
        self.tiempo_restante = self.tiempo_limite * 1000  # Tiempo en milisegundos

        # Variables para el temporizador de aparición de patos
        self.tiempo_entre_patos = 1500  # Tiempo entre cada pato en milisegundos
        self.tiempo_ultimo_pato = pygame.time.get_ticks()  # Última vez que se generó un pato

        # Generar los patos para el nivel actual
        self.generar_patos()

    def generar_patos(self):
        """Generar patos por nivel"""
        # Solo añadimos un pato a la lista en cada intervalo
        if len(self.patos) < self.patos_en_nivel:
            pato = Pato()  # Crear un pato
            pato.velocidad = self.velocidad_patos  # Ajustar la velocidad
            self.patos.append(pato)

    def siguiente_nivel(self):
        """Aumentar nivel y ajustar la dificultad"""
        self.nivel += 1
        self.patos_en_nivel += 2  # Agregar más patos
        self.velocidad_patos += 0.5  # Incrementar velocidad de los patos
        self.patos_mortos = 0  # Reiniciar contador de patos muertos
        self.tiempo_restante = self.tiempo_limite * 1000  # Reiniciar tiempo
        self.generar_patos()  # Crear nuevos patos para el siguiente nivel

    def manejar_eventos(self):
        """Manejar los eventos de cierre de ventana y clics"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.detector_mano.actualizar()
                cursor_pos = self.detector_mano.cursor
                disparo = self.detector_mano.disparo
                if disparo:
                    for pato in self.patos:
                        if pato.rect.collidepoint(cursor_pos):
                            distancia = ((pato.rect.centerx - cursor_pos[0])**2 + (pato.rect.centery - cursor_pos[1])**2)**0.5
                            if distancia < 50 and not pato.muerto:
                                pato.muerto = True
                                pato.frame_actual = 0
                                pato.tiempo_animacion = 0
                                pato.vel_caida = 0
                                break
                # mouse_pos = pygame.mouse.get_pos()
                # self.sonido_disparo.play()
                # for pato in self.patos:
                #     # Aquí verificamos si el clic está dentro del área de colisión del pato
                #     # Hacemos un margen de tolerancia para hacer el clic más preciso
                #     if pato.rect.collidepoint(mouse_pos):
                #         # En lugar de matar el pato si se hace clic cerca de otro pato,
                #         # se puede aplicar una tolerancia para que no ocurran clics erróneos
                #         distancia = pato.rect.centerx - mouse_pos[0], pato.rect.centery - mouse_pos[1]
                #         distancia = (distancia[0]**2 + distancia[1]**2)**0.5  # Distancia euclidiana entre el clic y el centro del pato
                #         if distancia < 50:  # Ajusta esta distancia según el tamaño de los patos
                #             if not pato.muerto:
                #                 pato.muerto = True
                #                 pato.frame_actual = 0
                #                 pato.tiempo_animacion = 0
                #                 pato.vel_caida = 0
                #                 self.sonido_pato.play()
                #                 break  # Salir del bucle si el pato ha sido disparado


    def actualizar(self):
        """Actualizar la lógica de los patos y niveles"""
        # Decrementar el tiempo restante
        self.tiempo_restante -= 1000 / self.fps  # Reducir el tiempo restante

        self.patos_mortos = sum(1 for pato in self.patos if pato.muerto)

        if self.patos_mortos == len(self.patos):
            self.siguiente_nivel()  # Si todos los patos están muertos, siguiente nivel

        # Comprobar si ha pasado suficiente tiempo para generar un nuevo pato
        if pygame.time.get_ticks() - self.tiempo_ultimo_pato > self.tiempo_entre_patos:
            self.generar_patos()
            self.tiempo_ultimo_pato = pygame.time.get_ticks()  # Actualizar el tiempo del último pato generado

        for pato in self.patos:
            pato.mover()
            pato.actualizar_animacion()

        # Verificar si el tiempo se ha agotado
        if self.tiempo_restante <= 0:
            print("¡Tiempo agotado! Has perdido.")
            self.running = False

    def dibujar(self):
        """Dibujar los elementos en la pantalla"""
        self.SCREEN.blit(self.background, [0, 0])
        self.SCREEN.blit(self.clouds_up, [0, 0])
        self.SCREEN.blit(self.clouds_down, [0, 0])
        # Dibujar todos los patos
        for pato in self.patos:
            pato.dibujar(self.SCREEN)
            
        self.SCREEN.blit(self.ground, [0, 0])

        # Dibujar puntero (mouse)
        mouse_position = pygame.mouse.get_pos()
        puntero_rect = self.puntero.get_rect()
        puntero_centrado = (mouse_position[0] - puntero_rect.width // 2, mouse_position[1] - puntero_rect.height // 2)
        #self.SCREEN.blit(self.puntero, puntero_centrado)
        self.SCREEN.blit(self.puntero, self.detector_mano.cursor)

        # Mostrar el nivel actual
        font = pygame.font.SysFont(None, 36)
        texto_nivel = font.render(f"Nivel: {self.nivel}", True, (0, 0, 0))
        self.SCREEN.blit(texto_nivel, (10, 10))

        # Mostrar el tiempo restante
        tiempo_texto = font.render(f"Tiempo: {int(self.tiempo_restante / 1000)}", True, (0, 0, 0))
        self.SCREEN.blit(tiempo_texto, (self.SCREEN_WIDTH - 150, 10))

    def ejecutar(self):
        """Ejecutar el ciclo principal del juego"""
        while self.running:
            self.manejar_eventos()  # Manejar los eventos
            self.actualizar()  # Actualizar el estado de los patos
            self.dibujar()  # Dibujar la escena
            pygame.display.flip()  # Actualizar la pantalla
            self.timer.tick(self.fps)  # Controlar los FPS
        self.detector_mano.cerrar()
        pygame.quit()

