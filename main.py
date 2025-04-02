# Lo hice por desparche en un dia, para probar algunas mecanicas basicas, nada serio ni oficial, pero esta divertido

import pygame
import random
import math

from Personajes.persona import *
pygame.init()



# LISTAS
obstaculos = []
obstaculomalosL = []
trayectoria = []
fondo = []

# MODIFICABLES
l1, l2, l3, l4, l5, l6 = 60, 100, 25, 60, 10, 60
Ancho, Alto = 1440, 720

# ESTÁTICOS
Ventana = pygame.display.set_mode([Ancho, Alto])
Personaje = Jugador(400, 300)
suelorojo, contador_tiempo1, contador_tiempo2 = 0, 0, 0
limite_spawn = random.randint(l1, l2)
limite_spawn1 = random.randint(l1,l2)
Jugandoando = True
reloj = pygame.time.Clock()

# Variables para el tiempo y estado del juego
tiempo_inicio = None
tiempo_transcurrido = 0
perdiste = False

def objetoMasCercano(): 
    if not obstaculos:
        return None
    return min(obstaculos, key=lambda obj: math.dist((Personaje.x, Personaje.y), (obj.x, obj.y)))

def calcularAngulo(personaje, objetivo):
    dx = objetivo.x - personaje.x
    dy = objetivo.y - personaje.y
    return math.atan2(dy, dx)

def Las_Teclas(tec):
    global tiempo_inicio
    if tec[pygame.K_SPACE]:
        objetivo = objetoMasCercano()
        if objetivo:
            disH = math.sqrt((objetivo.x - Personaje.x)**2 + (objetivo.y - Personaje.y)**2)
            if disH >= 100:
                angulo = calcularAngulo(Personaje, objetivo)
                Personaje.columpiarse(angulo)
                dibujarTrayectoria(Ventana, (Personaje.x + 10, Personaje.y + 10), (objetivo.x, objetivo.y))

            else:
                return None


def dibujarTrayectoria(ventana, inicio, fin):
    pygame.draw.line(ventana, (255, 0, 0), inicio, fin, 3)

def detectar_colision():
    global Jugandoando, perdiste, suelorojo
    for obstaculo in obstaculomalosL:
        if Personaje.rect.colliderect(obstaculo.rect):
            perdiste = True
            return True
    if tiempo_transcurrido >= 10 and Personaje.y + Personaje.alto >= Personaje.suelo:
        perdiste = True
        return True

    return False

while Jugandoando:
    reloj.tick(60)
    Ventana.fill("black")
    if tiempo_transcurrido >= 60:
        Personaje.color = ("green")
    Teclas = pygame.key.get_pressed()


    if tiempo_inicio is None:
            tiempo_inicio = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Jugandoando = False
        if perdiste and evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            Personaje.x, Personaje.y = 400, 300
            perdiste = False
            tiempo_transcurrido = 0
            tiempo_inicio = None
            pygame.draw.rect(Ventana, (0, 0, 0), (0, Personaje.suelo, Ancho, 18))
            obstaculomalosL.clear()
            obstaculos.clear()
            Personaje.actualizar_rect()

    if perdiste:
        fuente = pygame.font.SysFont(None, 55)
        pygame.draw.rect(Ventana, (0, 0, 0), (0, Personaje.suelo, Ancho, 18))
        suelorojo = 0
        texto = fuente.render(f"sobreviviste un total de {tiempo_transcurrido}s kjjjjj (dale enter)", True, (255, 255, 255))
        Ventana.blit(texto, (Ancho // 2 - 450, Alto // 2))
        pygame.display.update()
        continue

    contador_tiempo1 += 1
    if contador_tiempo1 > limite_spawn1:
        obstaculos.append(Obstaculo(Ancho, Alto))
        contador_tiempo1 = 0
        limite_spawn1 = random.randint(l1, l2)

    contador_tiempo2 += 1
    if tiempo_transcurrido <= 30:
        if contador_tiempo2 > limite_spawn:
            obstaculomalosL.append(ObstaculoMalo(Ancho, Alto))
            contador_tiempo2 = 0
            limite_spawn = random.randint(l1, l2)
    elif tiempo_transcurrido > 30:
        if contador_tiempo2 > limite_spawn:
            obstaculomalosL.append(ObstaculoMalo(Ancho, Alto))
            contador_tiempo2 = 0
            limite_spawn = random.randint(l3, l4)
    elif tiempo_transcurrido > 60:
        if contador_tiempo2 > limite_spawn:
            obstaculomalosL.append(ObstaculoMalo(Ancho, Alto))
            contador_tiempo2 = 0
            limite_spawn = random.randint(l5, l6)

    for obstaculo in obstaculos[:]:
        obstaculo.mover()
        obstaculo.dibujar(Ventana)
        if obstaculo.x + obstaculo.tamaño < 0:
            obstaculos.remove(obstaculo)

    for obstaculo in obstaculomalosL[:]:
        obstaculo.mover()
        obstaculo.dibujar(Ventana, False)
        if obstaculo.x + obstaculo.tamaño < 0:
            obstaculomalosL.remove(obstaculo)

    if tiempo_transcurrido >= 9:
        pygame.draw.rect(Ventana, (255, 0, 0), (0, Personaje.suelo, Ancho, 18))

    if tiempo_inicio:
        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        fuente = pygame.font.SysFont(None, 40)
        tiempo_texto = fuente.render(f"Tiempo: {tiempo_transcurrido}s", True, (255, 255, 255))
        Ventana.blit(tiempo_texto, (Ancho - 200, 20))



    if detectar_colision():
        pygame.time.delay(1000)
        continue

    Personaje.mover(Teclas)
    Personaje.dibujar(Ventana)
    Las_Teclas(Teclas)
    pygame.display.update()

pygame.quit()