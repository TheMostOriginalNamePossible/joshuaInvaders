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

        self.lasers = []
        self.sprites = [self.player]
        # make sounds here

    def removeInstance(self, instance):
        pygame.sprite.Sprite.kill(instance)

    def createInstance(self, instance):
        self.sprites.append(instance)
        self.mainSprites = pygame.sprite.OrderedUpdates(instance)
        self.groups.append(self.mainSprites)




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
            self.createInstance(self.laser)
        if self.laser.checkBounds():
            self.removeInstance(self.laser)








    def update(self):
        isPlaying = pygame.mixer.music.get_busy()
        if not isPlaying:
            pygame.mixer.music.play()


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
