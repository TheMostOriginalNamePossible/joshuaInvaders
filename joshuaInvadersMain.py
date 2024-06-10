"""joshuaInvadersMain.py
This will be used exclusively to run the game.

"""

import simpleGE, sprites, pygame
PAUSED = pygame.event.custom_type()
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__(self)
        self.setImage("image file")
        self.waveNumber = 1
        self.player = self.sprites.Player
        self.sprites = []

    def pauseGame(self):
        # pauses the game (placeholder)
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



def main():

if __name__ == "__main__"
    main()