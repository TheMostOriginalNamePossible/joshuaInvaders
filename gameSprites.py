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



class FallingObject(Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("INLYSSunny.png")
        self.setSize(4, 4)
        self.value = 1
        self.speed = 3

    def reset(self, scene, placeholder1, placeholder2):
        # move to where drop comes f
        self.__init__(scene)
        self.y = 10

        # y is random number between min and max speed
        self.dy = self.speed

    def checkBounds(self):
        if self.top > self.screenHeight:
            return True
        else:
            return False


class PowerUp(FallingObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("INLYSSunny.png")
        self.setSize(25, 25)

    def reset(self, scene, xDrop, yDrop):
        # tells where it drops from
        self.__init__(scene)
        self.x = xDrop
        self.y = yDrop

        # tells the speed at which it falls
        self.dy = self.speed


class Bullet(FallingObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("INLYSSunny.png")
        self.setSize(25, 25)

    def reset(self, scene, xShot, yShot):
        # tells where to shoot from
        super().__init__(scene)
        self.x = xShot
        self.y = yShot

        # moves the laser
        self.dy = -self.speed

    def process(self):
        if self.checkBounds():
            del self
