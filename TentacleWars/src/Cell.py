import pygame
from pygame.locals import *
import random
import math
import pickle
from languages.predicate import Predicate


GREEN = (47, 171, 51)
RED = (200, 0, 0)
GRAY = (55, 55, 55)
WHITE = (255, 255, 255)
WARMYELLOW = (255, 255, 85)


class avgDelta_Fact(Predicate):
    predicate_name="avgDelta_Fact"
    def __init__(self, index, value):
        self.index = index
        self.value = value

    def __str__(self):
        return f"avgDelta_Fact({self.index},\"{self.value}\")"


class Cell_Predicate(Predicate):
    predicate_name="cell"
    def __init__(self, x=None, y=None, value=None, color=None, lastValue=None, name=None, state=None, loss=None,
                 avgDelta=None, getNeedle=None, injectTime=None, fakeNeedle=None):
        Predicate.__init__(self,[("x"), ("y"), ("value"), ("color"), ("lastValue"), ("name"), ("state"), ("loss"), ("getNeedle"), ("injectTime"), ("fakeNeedle")])
        self.x = x
        self.y = y
        self.color = color  # green by default
        self.radius = 23
        self.outerRadius = self.radius + 8
        self.lastValue = lastValue
        self.value = value
        self.name = name
        self.state = state
        self.loss = loss
        self.avgDelta = avgDelta
        self.getNeedle = getNeedle  # being injected?
        self.injectTime = injectTime  # start counting the time during Injection from 0
        self.fakeNeedle = fakeNeedle  # needle left is 0

        # Get and Set For EMBASP using, Getting and Setting "Cell" predicate terms
    def get_x(self):
        return self.x

    def set_x(self, x):
            self.x = x

    def get_y(self, y):
        self.y = y

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_lastValue(self):
        return self.lastValue

    def set_lastValue(self, lastValue):
        self.lastValue = lastValue

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_loss(self):
        return self.loss

    def set_loss(self, loss):
        self.loss = loss


    def get_getNeedle(self):
        return self.getNeedle

    def set_getNeedle(self, getNeedle):
        self.getNeedle = getNeedle

    def get_injectTime(self):
        return self.injectTime

    def set_injectTime(self, injectTime):
        self.injectTime = injectTime

    def get_fakeNeedle(self):
        return self.fakeNeedle

    def set_fakeNeedle(self, fakeNeedle):
        self.fakeNeedle = fakeNeedle

    def __str__(self):
        return ("Cell(" + str(self.x) + "," + str(self.y) + "," + str(self.value) + str(self.color) + "," + str(
                self.lastValue) + "," + str(self.name) + "," + str(self.state) + "," + str(self.loss) + "," + str(
                self.avgDelta) + "," + str(self.getNeedle) + "," + str(self.injectTime) + "," + str(self.fakeNeedle)
                + ").")


class Cell(object):
    def __init__(self, x, y, value=20, color=GREEN):
        self.x, self.y = x, y
        self.color = color  # green by default
        self.radius = 23
        self.outerRadius = self.radius + 8
        self.lastValue = self.value = value
        self.name = "ATT"
        self.state = None
        self.loss = 0
        self.avgDelta = []
        self.getNeedle = False  # being injected?
        self.injectTime = 0  # start counting the time during Injection from 0
        self.fakeNeedle = False  # needle left is 0
        self.Predicate = Cell_Predicate

    def drawCell(self, surface):
        center = (self.x, self.y)
        color = WHITE if not self.getNeedle else GREEN
        pygame.draw.circle(surface, color, center, self.outerRadius, 3)
        pygame.draw.circle(surface, self.color, center, self.radius, 0)
        ############# possibly a gradient effect ###############
        pygame.draw.circle(surface, (255, 255, 255), center, self.radius, 2)
        self.drawValue(surface)
        if self.value >= 50:
            # more fashion drawing for larger cell
            for i in range(8):
                size = random.randint(2, 6)
                self.drawSideCircle(surface, i, size)

    def __lt__(self, other):
        return True

    def drawSideCircle(self, surface, ang, radius):
        angle = ang * math.pi / 4
        cx, cy = int(round(self.x + self.outerRadius * math.cos(angle))), \
            int(round(self.y + self.outerRadius * math.sin(angle)))
        pygame.draw.circle(surface, self.color, (cx, cy), radius, 0)

    def drawValue(self, surface):
        my_font = pygame.font.SysFont("", 21, True)
        textObj = my_font.render("%d" % self.value, True, (255, 255, 255))
        if len(str(self.value)) == 2:
            surface.blit(textObj, (self.x - 8, self.y - 10.5))
        else:
            surface.blit(textObj, (self.x - 5, self.y - 10.5))

    def findDistanceInChainUnits(self, targetx, targety):

        geoDistance = ((targetx-self.x)**2+(targety-self.y)**2)**0.5
        dotNumber = geoDistance / (3 * 2)  # diameter
        valueNeed = dotNumber / 2
        print(valueNeed)
        return valueNeed
    #QUESTO METODO VIENE UTILIZZATO SOLO DALL'IA

    def findAllies(self, allCellList):
        # in game, allCellList should be self.cellList
        self.alliesList = []
        embList = []  # temporary list for EMB
        allyAvg = 0
        for cell in allCellList:
            if cell.color == self.color:  # possibly used for BLUE?
                if cell.name == "ATT" and cell.x != self.x:
                    self.alliesList.append((cell.value, cell.name, cell))
                else:
                    embList.append((cell.value, cell.name, cell))
                allyAvg += cell.value
        # EMB cells first, and then ATT cell, in cell value order
        self.alliesList = sorted(embList) + sorted(self.alliesList)
        if len(self.alliesList) != 0:
            return float(allyAvg) / len(self.alliesList)
        else:
            return 0  # force the cell to be in defense mode

    def findEnemiesWithinDistance(self, allCellList):
        """ return self.grayList and self.allOtherList as a tuple """
        # for AI use. 
        self.enemiesList = []
        grayList = []  # higher priority should be put in front
        enemyAvg = 0
        for cell in allCellList:
            if cell.color != self.color:
                valueNeed = self.findDistanceInChainUnits(cell.x, cell.y)
                if self.value - valueNeed > 10:
                    # that is, after reaching out tentacle, value left is 10
                    # gray (neutral) cell should be of priority
                    if cell.color == GRAY:
                        # ATTENTION! No longer cell.name for index 1
                        grayList.append((cell.value, cell.color, cell))
                    elif cell.name == "ATT":
                        # the heuristic here is that estimated distance
                        # to travel plus target's value
                        enemyAvg += cell.value
                        self.enemiesList.append((cell.value + valueNeed, \
                                                 cell.color, cell))
        self.grayList = list(grayList)  # just in case, so that no aliasing
        self.allOtherList = list(reversed(sorted(grayList))) + sorted(self.enemiesList)
        if len(self.enemiesList) != 0:
            return float(enemyAvg) / len(self.enemiesList)
        else:
            return 100  # force the cell to be in defense mode

    def findEmergencyCell(self):
        alliesList = self.alliesList
        for ((allyValue, allyName, ally)) in alliesList:
            # print "allyinfo:",ally.x,ally.y
            if ally.state == "Alert" and allyName == "ATT":
                return ally
        return None

    def think(self, environment, animateCount):
        # the thinking process refers to the AI
        #####################################################################
        #     Later possibly use value drop in time also to determin. For
        # instance, consider d(C.V.)/dt
        #####################################################################
        enemyAvg = self.findEnemiesWithinDistance(environment)
        allyAvg = self.findAllies(environment)
        count, lowKey, highKey = animateCount, 8, 16
        delta = self.lastValue - self.value  # loss of life in given time. Say 5.
        self.lastValue = self.value
        self.avgDelta.append(delta)
        if len(self.avgDelta) >= 15:
            self.loss = float(sum(self.avgDelta)) / 15
            self.avgDelta = []
            # print "loss",self.x,self.y,self.loss
        emergency = self.findEmergencyCell()
        # print "emergency:",emergency
        # print allyAvg,enemyAvg
        if animateCount < 100:
            self.state = "Defense"
        elif lowKey < self.value < highKey or 1.4 <= self.loss <= 1.5:
            # lose 6 value points per second
            self.state = "Defense"
        elif self.value <= lowKey or self.loss > 1.5:
            self.state = "Alert"
        elif self.value >= highKey:
            self.considerEmerg(emergency, allyAvg, enemyAvg)

    def considerEmerg(self, emergency, allyAvg, enemyAvg):
        lowKey, highKey = 5, 15
        if emergency != None:
            if self.value + 90 >= enemyAvg:
                self.state = "Attack and Assist"
            elif self.value + allyAvg >= enemyAvg * 3. / 2:
                self.state = "Attack and Assist"
            else:
                self.state = "Defense"
        else:
            if self.value + lowKey >= enemyAvg:
                self.state = "Attack"
            elif self.value + allyAvg >= enemyAvg * 3. / 2:
                self.state = "Attack"
            else:
                self.state = "Defense"

    def update(self, environment, animateCount):
        # update every aspect: camp, current mode, etc.
        # ONLY ENEMY CELL NEEDS TO UPDATE.
        self.think(environment, animateCount)
        # print self.x,self.y,self.state
        # change mode,find friends,find enemies

    def __hash__(self):
        hashable = (self.x, self.y)
        return hash(hashable)
