"""joshuaInvadersMain.py
This will be used exclusively to run the game.

"""

import simpleGE, pygame, json, gameSprites
#Custom Events
PAUSED = pygame.event.custom_type()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__(self)
        pygame.mixer.music.load("music file")
        self.setImage("image file")
        self.waveNumber = 1

        # put sprites here
        self.player = gameSprites.Player(self)

        self.tempInstances = []
        self.sprites = []
        # make sounds here

    def removeInstance(self, instance):
        for sprite in self.sprites:
            if sprite == instance:
                self.sprites.remove(instance)

    def createInstance(self, instance):
        self.sprites.append(instance)

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

    def update(self):
        isPlaying = pygame.mixer.music.get_busy()
        if not isPlaying:
            pygame.mixer.music.play()



def main():
    events = pygame.event.get()
    print(PAUSED)


if __name__ == "__main__":
    main()
