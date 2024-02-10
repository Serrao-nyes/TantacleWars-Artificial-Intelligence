import pygame  # Importa il modulo pygame per la grafica
from pygame.locals import *  # Importa costanti pygame
import random  # Importa il modulo random per la generazione di numeri casuali
import math  # Importa il modulo math per le operazioni matematiche
import pickle  # Importa il modulo pickle per la serializzazione
import time  # Importa il modulo time per la gestione del tempo
from levelClasses import *  # Importa le classi di livello dal modulo levelClasses

# Definizione dei colori come costanti
GREEN = (47, 171, 51)
RED = (200, 0, 0)
GRAY = (55, 55, 55)
WHITE = (255, 255, 255)
WARMYELLOW = (255, 255, 85)

# Classe che rappresenta una singola cellula nel gioco
class Cell(object):
    def __init__(self, x, y, value=20, color=GREEN):
        # Inizializza la posizione, il valore, il colore e altre proprietà della cellula
        self.x, self.y = x, y
        self.color = color  # verde di default
        self.radius = 23  # Raggio della cellula
        self.outerRadius = self.radius + 8  # Raggio esterno
        self.value = value  # Valore della cellula
        self.name = "ATT"  # Nome della cellula
        self.state = None  # Stato della cellula
        self.d = dict()  # Dizionario per dati aggiuntivi
        self.getNeedle = False  # Viene iniettato?
        self.injectTime = 0  # Tempo di iniezione
        self.fakeNeedle = False  # Ago finto

    # Metodo per disegnare la cellula sulla superficie di gioco
    def drawCell(self, surface):
        center = (self.x, self.y)
        color = WHITE if not self.getNeedle else GREEN
        pygame.draw.circle(surface, color, center, self.outerRadius, 3)
        pygame.draw.circle(surface, self.color, center, self.radius, 0)
        # Effetto di gradiente
        pygame.draw.circle(surface, (255, 255, 255), center, self.radius, 2)
        self.drawValue(surface)
        if self.value >= 50:
            # Disegno aggiuntivo per celle di valore elevato
            for i in range(8):
                size = random.randint(2, 6)
                self.drawSideCircle(surface, i, size)

    # Metodo per disegnare cerchi laterali attorno alla cellula
    def drawSideCircle(self, surface, ang, radius):
        angle = ang * math.pi / 4
        cx, cy = int(round(self.x + self.outerRadius * math.cos(angle))), \
                int(round(self.y + self.outerRadius * math.sin(angle)))
        pygame.draw.circle(surface, self.color, (cx, cy), radius, 0)

    # Metodo per disegnare il valore della cellula
    def drawValue(self, surface):
        my_font = pygame.font.SysFont("", 21, True)
        textObj = my_font.render("%d" % self.value, True, (255, 255, 255))
        if len(str(self.value)) == 2:
            surface.blit(textObj, (self.x - 8, self.y - 10.5))
        else:
            surface.blit(textObj, (self.x - 5, self.y - 10.5))

    # Metodo per calcolare la distanza in unità di catena tra la cellula e un punto target
    def findDistanceInChainUnits(self, targetx, targety):
        geoDistance = ((targetx - self.x) ** 2 + (targety - self.y) ** 2) ** 0.5
        dotNumber = geoDistance / (3 * 2)  # Diametro della cellula
        valueNeed = dotNumber / 2
        return valueNeed

    # Metodo per trovare tutte le alleati della cellula nell'elenco di tutte le celle
    def findAllies(self, allCellList):
        self.alliesList = []
        embList = []
        allyAvg = 0
        for cell in allCellList:
            if cell.color == self.color:
                if cell.name == "ATT" and cell.x != self.x:
                    self.alliesList.append((cell.value, cell.name, cell))
                else:
                    embList.append((cell.value, cell.name, cell))
                allyAvg += cell.value
        self.alliesList = sorted(embList) + sorted(self.alliesList)
        if len(self.alliesList) != 0:
            return float(allyAvg) / len(self.alliesList)
        else:
            return 0  # Forza la cellula a essere in modalità difensiva

    # Metodo per trovare nemici entro una certa distanza dalla cellula
    def findEnemiesWithinDistance(self, allCellList):
        self.enemiesList = []
        grayList = []
        enemyAvg = 0
        for cell in allCellList:
            if cell.color != self.color:
                valueNeed = self.findDistanceInChainUnits(cell.x, cell.y)
                if self.value - valueNeed > 10:
                    if cell.color == GRAY:
                        grayList.append((cell.value, cell.color, cell))
                    elif cell.name == "ATT":
                        enemyAvg += cell.value
                        self.enemiesList.append((cell.value + valueNeed, cell.color, cell))
        self.grayList = list(grayList)
        self.allOtherList = list(reversed(sorted(grayList))) + sorted(self.enemiesList)
        if len(self.enemiesList) != 0:
            return float(enemyAvg) / len(self.enemiesList)
        else:
            return 100  # Forza la cellula a essere in modalità difensiva

    # Metodo per determinare lo stato della cellula (Attacco/Difesa) in base alla situazione circostante
    def think(self, environment, animateCount):
        enemyAvg = self.findEnemiesWithinDistance(environment)
        allyAvg = self.findAllies(environment)
        count = animateCount
        if self.value < 15:
            self.state = "Defense"
        elif self.value >= 15:
            if self.value + 5 >= enemyAvg:
                self.state = "Attack"
            elif self.value + allyAvg >= enemyAvg * 3. / 2:
                self.state = "Attack"
            else:
                self.state = "Defense"

    # Metodo per aggiornare la cellula
    def update(self, environment, animateCount):
        self.think(environment, animateCount)

    # Metodo per generare un hash della cellula (usato per l'identificazione univoca)
    def __hash__(self):
        hashable = (self.x, self.y)
        return hash(hashable)

# Classe che rappresenta una cellula speciale "Embracer"
class Embracer(Cell):
    def __init__(self, x, y, value, color=(47, 171, 51)):
        super(Embracer, self).__init__(x, y, value, color)
        self.name = "EMB"
        self.increaseCount = 0
        self.moveJudge = False

    # Metodo per disegnare la cellula "Embracer"
    def drawCell(self, surface):
        center = (x, y) = (self.x, self.y)
        add = int(round(2 * self.radius / (3 ** 0.5)))

        pygame.draw.polygon(surface, (255, 255, 255), ((x, y - self.radius - 8), \
                                                       (x + add, y + self.radius - 8), \
                                                       (x - add, y + self.radius - 8)))
        pygame.draw.circle(surface, self.color, center, self.radius, 0)
        pygame.draw.circle(surface, (255, 255, 255), center, self.radius, 2)
        self.drawValue(surface)

    # Metodo per impostare il bersaglio e calcolare la velocità per il movimento
    def setTarget(self, targetx, targety, fps):
        distance = ((targetx - self.x) ** 2 + (targety - self.y) ** 2) ** 0.5
        acce = (distance * 2 / 3 ** 2) / fps  # Accelerazione. Completa in 3 secondi
        self.speed = int(round((2 * acce * distance) ** 0.5))
        self.speedx = int(round(((targetx - self.x) / distance) * self.speed))
        self.speedy = int(round(((targety - self.y) / distance) * self.speed))
        self.accex = ((targetx - self.x) / distance) * acce
        self.accey = ((targety - self.y) / distance) * acce

    # Metodo per muovere la cellula "Embracer"
    def move(self, targetx, targety, fps):
        distance = ((targetx - self.x) ** 2 + (targety - self.y) ** 2) ** 0.5
        self.setTarget(targetx, targety, fps)
        if self.moveJudge:
            self.x += self.speedx
            self.y += self.speedy
            if distance(targetx, targety, self.x, self.y, 0.5):
                self.speedx -= int(round(self.accex))
                self.speedy -= int(round(self.accey))
            else:
                self.moveJudge = False  # Si ferma
            self.sprite.rect.x = self.x
            self.sprite.rect.y = self.y

# Classe che rappresenta un livello del gioco
class Level_1(object):
    def __init__(self):
        # Inizializza le celle del livello
        self.c1 = Cell(300, 400, 2)
        self.c2 = Cell(500, 400, 2)
        self.c3 = Cell(630, 460, 100, (200, 0, 0))
        self.cellList = [self.c1, self.c2, self.c3]  # Lista di celle del livello

# Altre classi di livello con implementazioni simili


class Level_2(object):
    def __init__(self):
        self.c1 = Cell(600,400,5,(55,55,55))
        self.c2 = Cell(500,500,10)
        self.c3 = Cell(240,620,10,(200,0,0))
        self.cellList = [self.c1,self.c2,self.c3]


class Level_3(object):
    def __init__(self):
        self.c1 = Cell(100,400,5,(55,55,55))
        self.c2 = Cell(500,370,46)
        self.c3 = Cell(240,230,7,(200,0,0))
        self.c4 = Embracer(520,80,3,(200,0,0))
        self.c5 = Embracer(230,125,10,GREEN)
        self.c6 = Cell(650,600,40,(200,0,0))
        self.c7 = Cell(560,500,60)
        self.cellList = [self.c1,self.c2,self.c3,self.c4,self.c5,self.c6,self.c7]

class Level_4(object):
    def __init__(self):
        self.c1 = Cell(350,300,0,(55,55,55))
        self.c2 = Cell(500,370,30)
        self.c3 = Cell(240,230,15,(200,0,0))
        self.c4 = Cell(150,600,15,(200,0,0))
        self.c5 = Embracer(230,125,10,GREEN)
        self.c6 = Cell(450,180,15,(200,0,0))
        self.c7 = Cell(560,500,10,(55,55,55))
        self.cellList = [self.c1,self.c2,self.c3,self.c4,self.c5,self.c6,self.c7]

class Level_5(object):
    def __init__(self):
        self.cellList = []
        for x in range(150,650,150):
            if x%300 == 0:
                cell = Cell(x,x,30,GREEN)
            else:
                cell = Cell(x,x,25,GREEN)
            self.cellList.append(cell)
        for x in range(150,650,150):
            cell = Cell(x,750-x,22,(200,0,0))
            self.cellList.append(cell)

class Level_6(object):
    def __init__(self):
        self.c1 = Cell(250,150,12,GREEN)
        self.c2 = Cell(450,150,12,GREEN)
        self.c3 = Cell(150,int(round(150+100*math.sqrt(3))),12,GREEN)
        self.c4 = Cell(550,int(round(150+100*math.sqrt(3))),12,GREEN)
        self.c5 = Cell(250,int(round(150+200*math.sqrt(3))),12,GREEN)
        self.c6 = Cell(450,int(round(150+200*math.sqrt(3))),12,GREEN)
        self.c7 = Cell(350,320,60,RED)
        self.cellList = [self.c1,self.c2,self.c3,self.c4,self.c5,\
                         self.c6,self.c7]
