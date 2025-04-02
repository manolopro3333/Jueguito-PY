import pygame

import random
import math

class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.velocidad_x = 5
        self.velocidad_y = 0
        self.gravedad = 0.5
        self.suelo = 700
        self.color = (0, 0, 255)
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.columpiando = False  # Estado de columpiarse
        self.fuerza_columpio = 10  # Fuerza del columpio
        self.impulso = False  # Estado de impulso
        self.fuerza_impulso = 15  # Fuerza del impulso

    def actualizar_rect(self):
        self.rect.topleft = (self.x, self.y)

    def dibujar(self, ventana):
        self.rect.topleft = (self.x, self.y)
        pygame.draw.rect(ventana, self.color, self.rect)

    def mover(self, teclas):
        # Aplicar gravedad
        self.velocidad_y += self.gravedad
        self.y += self.velocidad_y
        # Limitar al suelo
        if self.y + self.alto >= self.suelo:
            self.y = self.suelo - self.alto
            self.velocidad_y = 0

        if self.x == 0:
            self.x = self.x

            
        # Si está columpiando, aplicar fuerza de columpio
        if self.columpiando and not self.y + self.alto >= self.suelo:
            self.x += self.velocidad_x
            self.y += self.velocidad_y

    def columpiarse(self, angulo):
        # Aplicar fuerza en la dirección del ángulo
        self.velocidad_x = self.fuerza_columpio * math.cos(angulo)
        self.velocidad_y = self.fuerza_columpio * math.sin(angulo)
        self.columpiando = True

class Obstaculo:
        def __init__(self, ancho_pantalla, alto_pantalla):
            self.x = ancho_pantalla
            self.y = random.randint(50, alto_pantalla // 2)
            self.tamaño = random.randint(20, 50)
            self.velocidad = 10
            self.tipo = random.choice(["cuadrado", "circulo"])
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

        def mover(self):
            self.x -= self.velocidad

        def dibujar(self, ventana):
            if self.tipo == "cuadrado":
                pygame.draw.rect(ventana, self.color, (self.x, self.y, self.tamaño, self.tamaño))
            else:
                pygame.draw.circle(ventana, self.color, (self.x, self.y), self.tamaño // 2)


class ObstaculoMalo:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.x = ancho_pantalla
        self.Yr = alto_pantalla
        self.y = random.randint(50, alto_pantalla)
        self.tamaño = random.randint(40, 60)  # Aumentar tamaño de hitbox
        self.velocidad = 10
        self.color = (255, 0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.tamaño, self.tamaño + 25)

    def mover(self):
        self.x -= self.velocidad
        self.rect.x = self.x

    def dibujar(self, ventana, piso):
        if piso:
            pygame.draw.rect(ventana, self.color, (self.x, self.Yr-100, self.tamaño, self.tamaño+25))
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.tamaño, self.tamaño+25))
