"""sprites.py
Holds sprite classes. Put sprite classes in here.
(For szhoe) Make sure you put a little comment on stuff you change or add
"""

import pygame, simpleGE, math

class Path(object):
    def __init__(self, scene):
        super().__init__(scene)
        self.points = ((0.0, 0.0), (1.0, 1.0))
        #path parameter
        self.__parameter = 0.0

        self.parameter = 0.0

    @property
    def parameter(self):
        return self.__parameter

    @parameter.setter
    def parameter(self, parameter):
        if type(parameter) == float and 0.0 <= parameter <= 1.0:
            self.parameter = parameter
        else:
            self.parameter = 0.0

    def bezier(self, t, points) -> float:
        """De Casteljau's algorithm."""
        n = len(points)
        Px = []
        Py = []

        for i in range(1, n):
            xSum = points[i][0]*math.pow()
            ySum = points[i][0]*(1-t)**(n-i)

        for j in range(1, n):
            for k in range(n - j):
                beta[k] = beta[k] * (1 - t) + beta[k + 1] * t
        return beta[0]

class Sprite(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)

        # hitbox coefficient private attributes

        self.__topHitboxC = 1
        self.__bottomHitboxC = 1
        self.__leftHitboxC = 1
        self.__rightHitboxC = 1

        # hitbox coefficient properties

        self.topHitboxC = 1
        self.bottomHitboxC = 1
        self.leftHitboxC = 1
        self.rightHitboxC = 1

        # sets hitbox

        self.setHitbox()


    @property
    def topHitboxC(self):
        return self.__topHitboxC

    @topHitboxC.setter
    def topHitboxC(self, c):
        if type(c) == float and 0 <= c:
            self.__topHitboxC = c
        else:
            self.__topHitboxC = 1

    @property
    def bottomHitboxC(self):
        return self.__bottomHitboxC

    @bottomHitboxC.setter
    def bottomHitboxC(self, c):
        if type(c) == float and 0 <= c:
            self.__bottomHitboxC = c
        else:
            self.__bottomHitboxC = 1

    @property
    def leftHitboxC(self):
        return self.__leftHitboxC

    @leftHitboxC.setter
    def leftHitboxC(self, c):
        if type(c) == float and 0 <= c:
            self.__leftHitboxC = c
        else:
            self.__leftHitboxC = 1

    @property
    def rightHitboxC(self):
        return self.__rightHitboxC

    @rightHitboxC.setter
    def rightHitboxC(self, c):
        if type(c) == float and 0 <= c:
            self.__rightHitboxC = c
        else:
            self.__rightHitboxC = 1

    def setHitbox(self):
        self.top = self.top*self.topHitboxC
        self.bottom = self.bottom*self.bottomHitboxC
        self.left = self.left*self.leftHitboxC
        self.right = self.right*self.rightHitboxC

    def checkBounds(self):
        if self.bottom > self.screenHeight:
            return True
        elif self.top < 0:
            return True
        elif self.right < 0:
            return True
        elif self.left > self.screenWidth:
            return True
        else:
            return False


class Joshua(Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Joshua.png")
        self.setSize(80, 80)

        self.setHitbox()

class Player(Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.bottomHitboxC = 0.5
        self.topHitboxC = 0.5
        self.leftHitboxC = 0.5
        self.rightHitboxC = 0.5
        self.setImage("INLYSSunny.png")
        self.setSize(60, 60)
        self.setHitbox()

    def moveSprite(self):
        pos = pygame.mouse.get_pos()
        self.x = pos[0]
        self.y = pos[1]

    def xGetPos(self):
        return self.x

    def yGetPos(self):
        return self.y

    def process(self):
        self.moveSprite()



class MovingObject(Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("INLYSSunny.png")
        self.setSize(4, 4)
        self.value = 1
        self.ySpeed = 3

    def reset(self):
        # move to where drop comes f
        self.x = 50
        self.y = 50


    def checkBounds(self):
        if self.bottom > self.screenHeight:
            return True
        elif self.top < 0:
            return True
        elif self.right < 0:
            return True
        elif self.left > self.screenWidth:
            return True
        else:
            return False


class PowerUp(MovingObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("INLYSSunny.png")
        self.setSize(25, 25)

    def drop(self):
        pass



class Bullet(MovingObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.damage = 1
        self.setImage("INLYSSunny.png")
        self.setSize(25, 25)
        self.ySpeed = 10


    def move(self):
        self.dy = -self.ySpeed

    def stop(self):
        pass



