import pygame
import math
import random

class Perro:
    def __init__(self):
        self.frames_derecha = []
        self.frames_izquierda = []
        self.frames_diagonal_derecha = []
        self.frames_diagonal_izquierda = []
        self.frame_actual = 0
        self.tiempo_animacion = 0
        self.ajustar_animacion = 1  # Velocidad de animación: menor = más rápida

        # Cargar imagen con sprites
        sprite_sheet = pygame.image.load("assets/duck/sprite_newduck_right.png").convert_alpha()
        # Dividir en frames
        for i in range(3):  # 3 frames
            frame = sprite_sheet.subsurface(pygame.Rect(i * 128, 0, 128, 128))
            frame_escalado = pygame.transform.scale(frame, (64, 64))  # aquí haces el pato más pequeño
            self.frames_derecha.append(frame_escalado)
        # Voltear los frames para la izquierda
        self.frames_izquierda = [pygame.transform.flip(frame, True, False) for frame in self.frames_derecha]

        # Cargar sprites diagonales hacia arriba (derecha)
        sprite_diagonal = pygame.image.load("assets/duck/sprite_newduck_up.png").convert_alpha()
        # Dividir en frames
        for i in range(3):
            frame = sprite_diagonal.subsurface(pygame.Rect(i * 128, 0, 128, 128))
            frame_escalado = pygame.transform.scale(frame, (64, 64))  # aquí haces el pato más pequeño
            self.frames_diagonal_derecha.append(frame_escalado)
        # Generar versiones volteadas hacia la izquierda
        self.frames_diagonal_izquierda = [pygame.transform.flip(frame, True, False) for frame in self.frames_diagonal_derecha]

        # Cargar sprite de pato muerto
        sprite_muerto = pygame.image.load("assets/duck/sprite_newduck_death.png").convert_alpha()
        for i in range(4):  # 4 frames
            frame = sprite_muerto.subsurface(pygame.Rect(i * 128, 0, 128, 128))
            frame_escalado = pygame.transform.scale(frame, (64, 64))  # aquí haces el pato más pequeño
            self.frames_muerto.append(frame_escalado)
        
        self.image = self.frames_derecha[0]
        self.rect = self.image.get_rect()
        self.ZONA_TIERRA_Y = 540
        self.rect.x = random.randint(0, 768 - self.rect.width)
        self.rect.y = 540  # Inicio desde zona de tierra

        self.velocidad = 3  # Velocidad de movimiento
        self.direccion = "derecha"  # Dirección inicial
        self.nuevo_destino()  # Definir un destino aleatorio al inicio

        self.vel_caida = 0
        self.gravedad = 0.5


    def nuevo_destino(self):
        # Escoge una posición aleatoria dentro de los límites de la pantalla
        self.destino_x = random.randint(0, 768 - self.rect.width)
        self.destino_y = random.randint(0, 300)

    def mover(self):
        if self.muerto:
            self.caer()
            return
        dx = self.destino_x - self.rect.x
        dy = self.destino_y - self.rect.y
        distancia = math.hypot(dx, dy)

        if distancia < 5:
            self.nuevo_destino()
        else:
            dx, dy = dx / distancia, dy / distancia
            self.rect.x += dx * self.velocidad
            self.rect.y += dy * self.velocidad

        # Cambiar la dirección dependiendo de la posición
        if dx < 0:
            self.direccion = "izquierda"
        else:
            self.direccion = "derecha"
        
        self.subiendo = dy < 0  # Si el movimiento en Y es negativo, está subiendo

    def caer(self):
        self.vel_caida += self.gravedad
        self.rect.y += self.vel_caida

        # Cambia la animación mientras cae
        self.tiempo_animacion += 1
        if self.tiempo_animacion >= self.ajustar_animacion:
            self.tiempo_animacion = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.frames_muerto)
            self.image = self.frames_muerto[self.frame_actual]

    def actualizar_animacion(self):
        self.tiempo_animacion += 1
        if self.tiempo_animacion >= self.ajustar_animacion:
            self.tiempo_animacion = 0
            self.frame_actual += 1

            if self.muerto:
                if self.frame_actual >= len(self.frames_muerto):
                    self.frame_actual = len(self.frames_muerto) - 1  # Mantén el último frame
                self.image = self.frames_muerto[self.frame_actual]
            else:
                self.frame_actual = self.frame_actual % len(self.frames_derecha)

                # Selección de sprite según dirección y si sube
                if self.subiendo:
                    if self.direccion == "derecha":
                        self.image = self.frames_diagonal_derecha[self.frame_actual]
                    else:
                        self.image = self.frames_diagonal_izquierda[self.frame_actual]
                else:
                    if self.direccion == "derecha":
                        self.image = self.frames_derecha[self.frame_actual]
                    else:
                        self.image = self.frames_izquierda[self.frame_actual]


    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)
        pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 2) 

