"""sprites.py
Holds sprite classes. Put sprite classes in here.
(For szhoe) Make sure you put a little comment on stuff you change or add
"""

import pygame, simpleGE


class Player(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("INLYSSunny.png")

        # hitbox coefficient private attributes

        self.__topHitboxC = 1
        self.__bottomHitboxC = 1
        self.__leftHitboxC = 1
        self.__rightHitboxC = 1

        # hitbox coefficient properties

        self.tophitboxC = 0.8
        self.bottomHitboxC = 0.8
        self.leftHitboxC = 0.8
        self.rightHitboxC = 0.8

        # hitbox coefficients

        self.xDim = 100
        self.yDim = 100
        self.setSize(100, 100)
        self.speed = 5

    @property
    def topHitboxC(self):
        return self.__topHitboxC

    @topHitboxC.setter
    def topHitboxC(self, c):
        if type(c) == float and 0 <= c <= 1:
            self.__topHitboxC = c
        else:
            self.__topHitboxC = 1

    @property
    def bottomHitboxC(self):
        return self.__bottomHitboxC

    @bottomHitboxC.setter
    def bottomHitboxC(self, c):
        if type(c) == float and 0 <= c <= 1:
            self.__bottomHitboxC = c
        else:
            self.__bottomHitboxC = 1



    @property
    def leftHitboxC(self):
        return self.__leftHitboxC

    @leftHitboxC.setter
    def leftHitboxC(self, c):
        if type(c) == float and 0 <= c <= 1:
            self.__leftHitboxC = c
        else:
            self.__leftHitboxC = 1

    @property
    def rightHitboxC(self):
        return self.__rightHitboxC

    @rightHitboxC.setter
    def rightHitboxC(self, c):
        if type(c) == float and 0 <= c <= 1:
            self.__rightHitboxC = c
        else:
            self.__rightHitboxC = 1
