import pygame
import math
import random

class Perro:
    def __init__(self, animacion="derecha"):
        self.frames_derecha = []
        self.frames_diagonal_derecha = []
        self.frame_actual = 0
        self.tiempo_animacion = 0
        self.ajustar_animacion = 10  # Velocidad de animación

        # Cargar imagen con sprites
        sprite_sheet = pygame.image.load("assets/dog/sprite_newdog_snif.png").convert_alpha()
        for i in range(3):  # 3 frames para la animación derecha
            frame = sprite_sheet.subsurface(pygame.Rect(i * 256, 0, 256, 256))
            frame_escalado = pygame.transform.scale(frame, (256, 256))
            self.frames_derecha.append(frame_escalado)

        # Cargar sprites diagonales hacia arriba (derecha)
        sprite_diagonal = pygame.image.load("assets/dog/sprite_newdog_laughing.png").convert_alpha()
        for i in range(2):  # 2 frames para la animación diagonal
            frame = sprite_diagonal.subsurface(pygame.Rect(i * 256, 0, 256, 256))
            frame_escalado = pygame.transform.scale(frame, (256, 256))
            self.frames_diagonal_derecha.append(frame_escalado)

        # Establecer la animación inicial según el parámetro
        self.animacion = animacion  # Puede ser "derecha" o "diagonal_derecha"
        self.image = self.frames_derecha[0]  # Asignar el primer frame de la animación derecha
        self.rect = self.image.get_rect()
        self.rect.x = 350  # Cambia la posición según necesites
        self.rect.y = 500

    def actualizar_animacion(self):
        self.tiempo_animacion += 1
        if self.tiempo_animacion >= self.ajustar_animacion:
            self.tiempo_animacion = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.frames_derecha if self.animacion == "derecha" else self.frames_diagonal_derecha)
            if self.animacion == "derecha":
                self.image = self.frames_derecha[self.frame_actual]
            else:
                self.image = self.frames_diagonal_derecha[self.frame_actual]

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

        

