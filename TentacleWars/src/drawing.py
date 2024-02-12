#!/usr/bin/env python

# Import delle librerie necessarie
import pygame
from pygame.locals import *
from sys import exit
from random import *
from math import pi

# Inizializzazione di Pygame
pygame.init()

# Creazione della finestra di gioco
screen = pygame.display.set_mode((640, 480), 0, 32)

# Lista per memorizzare i punti del tracciato del mouse
points = []

# Ciclo principale del gioco
while True:

    # Gestione degli eventi
    for event in pygame.event.get():
        if event.type == QUIT:
            # Se l'evento è di uscita, esce dal programma
            exit()
        if event.type == KEYDOWN:
            # Se il tasto premuto è una qualsiasi tastiera, cancella i punti memorizzati e riempie lo schermo di bianco
            points = []
            screen.fill((255, 255, 255))
        if event.type == MOUSEBUTTONDOWN:
            # Se viene premuto il pulsante del mouse, disegna un rettangolo, un cerchio e traccia la traiettoria del mouse
            screen.fill((255, 255, 255))
            # Disegna un rettangolo con colori casuali
            rc = (randint(0, 255), randint(0, 255), randint(0, 255))
            rp = (randint(0, 639), randint(0, 479))
            rs = (639 - randint(rp[0], 639), 479 - randint(rp[1], 479))
            pygame.draw.rect(screen, rc, Rect(rp, rs))
            # Disegna un cerchio con colori casuali
            rc = (randint(0, 255), randint(0, 255), randint(0, 255))
            rp = (randint(0, 639), randint(0, 479))
            rr = randint(1, 200)
            pygame.draw.circle(screen, rc, rp, rr)
            # Ottiene la posizione corrente del mouse
            x, y = pygame.mouse.get_pos()
            # Aggiunge la posizione corrente alla lista dei punti
            points.append((x, y))
            # Disegna l'arco in base alla posizione del mouse
            angle = (x / 639.) * pi * 2.
            pygame.draw.arc(screen, (0, 0, 0), (0, 0, 639, 479), 0, angle, 3)
            # Disegna un'ellisse in base alla posizione del mouse
            pygame.draw.ellipse(screen, (0, 255, 0), (0, 0, x, y))
            # Disegna linee dal bordo della finestra alla posizione del mouse
            pygame.draw.line(screen, (0, 0, 255), (0, 0), (x, y))
            pygame.draw.line(screen, (255, 0, 0), (640, 480), (x, y))
            # Disegna una serie di linee connettendo i punti del tracciato del mouse
            if len(points) > 1:
                pygame.draw.lines(screen, (155, 155, 0), False, points, 2)
            # Disegna un cerchio per ogni punto nella lista dei punti
            for p in points:
                pygame.draw.circle(screen, (155, 155, 155), p, 3)

    # Aggiornamento della schermata
    pygame.display.update()
