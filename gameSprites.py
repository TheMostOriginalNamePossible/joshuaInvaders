"""sprites.py
Holds sprite classes. Put sprite classes in here.
(For szhoe) Make sure you put a little comment on stuff you change or add
"""

import pygame, simpleGE


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





class Player(Sprite):
    def __init__(self, scene):
        super().__init__(scene)

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
        self.y = 10

        # y is random number between min and max speed
        self.dy = self.ySpeed

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

    def reset(self):
        # tells where it drops from
        self.x = 0
        self.y = 0

        # tells the speed at which it falls
        self.dy = self.ySpeed


class Bullet(MovingObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("INLYSSunny.png")
        self.setSize(25, 25)

    def reset(self):
        # tells where to shoot from
        self.x = 0
        self.y = 0

        # moves the laser
        self.dy = -self.ySpeed

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


