"""joshuaInvadersMain.py
This will be used exclusively to run the game.

"""

import simpleGE, pygame, json, gameSprites
#Custom Events
PAUSED = pygame.event.custom_type()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        pygame.mixer.music.load("neverlikedyoursmile.mp3")
        pygame.mixer.music.set_volume(0.0)
        self.setImage("scenepark.png")
        self.waveNumber = 1

        # put sprites here
        self.player = gameSprites.Player(self)
        self.laser = gameSprites.Bullet(self)
        self.joshua = gameSprites.Joshua(self)
        self.laserGroup = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.GroupSingle()
        self.enemyGroup = pygame.sprite.Group()
        # make sounds here

    def __mainLoop(self):
        """ manage all the main events
            automatically called by start
        """
        self.clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keepGoing = False
            self.doEvents(event)
            self.processEvent(event)

        self.update()
        self.process()
        for group in self.groups:
            group.clear(self.screen, self.background)
            group.update()
            group.draw(self.screen)

        pygame.display.flip()
    def start(self):
        """ sets up the sprite groups
            begins the main loop
        """
        self.playerSpriteUp = pygame.sprite.OrderedUpdates(self.player)
        self.playerGroup.add(self.playerSpriteUp)
        self.groups = [self.laserGroup, self.enemyGroup, self.playerGroup]

        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.keepGoing = True
        while self.keepGoing:
            self.__mainLoop()
        pygame.quit()

    def removeLaser(self, laser):
        laser.remove(self.laserGroup)

    def createLaser(self, laser):
        laser.add(self.laserGroup)


    def pauseGame(self):
        # temporary just so I remember
        pygame.event.post(pygame.event.Event(PAUSED))
        pass

    def quitGame(self):
        # temporary just so I remember
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        pass

    def saveGame(self):
        # placeholder to figure out how save games work
        pass

    def doEvents(self, event):
        # probably for game transitions like waves and stuff
        if event.type == PAUSED:
            self.pauseGame()
        if event.type == pygame.QUIT:
            self.saveGame()
            self.stop()

    def process(self):

        for event in pygame.event.get():
            self.doEvents(event)
        if self.player.mouseDown:
            self.laser = gameSprites.Bullet(self)
            self.laser.x = self.player.xGetPos()
            self.laser.y = self.player.yGetPos()
            self.laser.move()
            self.createLaser(self.laser)
        for laser in self.laserGroup:
            if laser.checkBounds():
                self.removeLaser(laser)
            else:
                for enemy in self.enemyGroup:
                    if laser.collidesWith(enemy):
                        enemy.damage(laser.damage)




    def update(self):
        isPlaying = pygame.mixer.music.get_busy()
        if not isPlaying:
            pygame.mixer.music.play()


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
