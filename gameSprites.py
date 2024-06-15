"""gameSprites.py
Holds game assets.
"""

import pygame, simpleGE, math, random


class Sound(simpleGE.Sound):
    def __init__(self, file):
        self.sound = pygame.mixer.Sound(file)

    def volume(self, value):
        if type(value) == float:
            self.sound.set_volume(value)
        else:
            self.sound.set_volume(0.5)


# Not used in current version
class Path(object):
    def __init__(self):
        super().__init__()
        self.points = ((0, 0), (1, 1))
        #path parameter
        self.t = 0.0

    def bezier(self, t, points):
        n = len(points)
        xSum = points[0][0]*math.pow(1-t, n)
        ySum = points[0][1]*math.pow(1-t, n)
        for i in range(1, n):
            x_i = points[i][0]*math.pow(1-t, n-i)*math.pow(t, i)*math.comb(n, i)
            xSum += x_i
            y_i = points[i][1]*math.pow(1-t, n-i)*math.pow(t, i)*math.comb(n, i)
            ySum += y_i
        p = (xSum, ySum)
        return p


class Sprite(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.hitboxCenter = self.rect.center
        self.__hitbox = self.rect
        self.hitbox = self.rect

    @property
    def hitbox(self):
        return self.__hitbox
    @hitbox.setter
    def hitbox(self, value):
        self.__hitbox = value


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
        self.setSize(60, 60)
        self.position = (50, 50)
        self.damage = 1
        self.hp = 3
        self.path = Path()
        #
        self.dropChance = 0.1
        self.perTickShootChance = 0.25

        self.timer = simpleGE.Timer()
        self.timer.totalTime = 1
        self.timer.start()

    def doDamage(self, damage):
        self.hp -= damage

    def dropPowerUp(self):
        rand = random.random()
        if rand < self.dropChance:
            return True
        else:
            return False

    def shoots(self):
        if self.timer.getTimeLeft() <= 0:
            rand = random.random()
            if rand < self.dropChance:
                self.timer.totalTime = random.random()*0.5 + 0.5
                self.timer.start()
                return True
            else:
                self.timer.totalTime = random.random()*0.5 + 0.5
                self.timer.start()
        else:
            return False


class Player(Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("INLYSSunny.png")
        self.setSize(60, 60)
        self.shotTimer = simpleGE.Timer()
        self.shotTimer.totalTime = 0.2
        self.shotTimer.start()
        self.boundAction = self.STOP
    def moveSprite(self):
        pos = pygame.mouse.get_pos()
        self.position = pos

    def canShoot(self):
        if self.shotTimer.getTimeLeft() <= 0:
            self.shotTimer.start()
            return True
        else:
            return False


class MovingObject(Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("INLYSSunny.png")
        self.setSize(4, 4)
        self.value = 1
        self.moveSpeed = 3

    def reset(self):
        # move to where drop comes f
        self.x = 50
        self.y = 50


class PowerUp(MovingObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("sepsisLaser.png")
        self.setSize(50, 50)
        self.dropSpeed = 3

    def drop(self):
        self.y += self.dropSpeed

class Life(PowerUp):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Steak.png")
        self.setSize(50, 50)

class Bullet(MovingObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.damage = 1
        self.setImage("INLYSSunny.png")
        self.setSize(25, 25)
        self.moveSpeed = 10

    def moveUp(self):
        self.y -= self.moveSpeed

    def moveDown(self):
        self.y += self.moveSpeed



