"""gameSprites.py
Holds game assets. A bit of a misnomer.
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


class LblWave(simpleGE.MultiLabel):
    pass

class LblLives(simpleGE.Label):

    pass

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
        self.perTickShootChance = 0.01

        self.timer = simpleGE.Timer()
        self.timer.totalTime = 5
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
        rand = random.random()
        if rand <= self.perTickShootChance and self.timer.getTimeLeft() <= 0:
            self.timer.start()
            return True
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

    def moveSprite(self):
        pos = pygame.mouse.get_pos()
        if pos == (0, 0):
            self.heightRatio = self.screenHeight / 1080
            self.position = (self.screenWidth/2, self.screenHeight - 80*self.heightRatio)
        else:
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



