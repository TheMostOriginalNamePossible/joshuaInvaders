"""joshuaInvadersMain.py
This will be used exclusively to run the game.

"""

import simpleGE, pygame, json, gameSprites, random

# Constants for your convenience
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# Custom Events
PAUSED = pygame.event.custom_type()
CONTINUE = pygame.event.custom_type()
SAVE = pygame.event.custom_type()
BACK = pygame.event.custom_type()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mixer.music.load("neverlikedyoursmile.mp3")
        pygame.mixer.music.set_volume(0.4)
        self.setImage("scenepark.png")
        self.paused = False
        # timers
        self.timerContinue = simpleGE.Timer()
        self.timerContinue.totalTime = 3
        self.invincibilityTimer = simpleGE.Timer()
        self.timersndbullet = simpleGE.Timer()
        self.timersndbullet.totalTime = 4
        self.timersndbullet.start()
        # screen adaptability
        self.width = SCREEN_WIDTH
        self.widthRatio = SCREEN_WIDTH/1080
        self.height = SCREEN_HEIGHT
        self.heightRatio = SCREEN_HEIGHT/720
        # some details
        self.enemyNum = 0
        self.waveNum = 0
        self.lives = 3
        self.laserSize = 0
        self.power = 0
        self.maxPower = 5

        # sprites
        self.player = gameSprites.Player(self)
        self.player.setSize(60*self.widthRatio, 60*self.heightRatio)
        self.joshua = gameSprites.Joshua(self)
        self.misc = []

        # groups
        self.grpPowerUp = pygame.sprite.Group()
        self.grpLaser = pygame.sprite.Group()
        self.grpPlayer = pygame.sprite.GroupSingle()
        self.grpEnemy = pygame.sprite.Group()
        self.grpBullet = pygame.sprite.Group()
        self.grpLblWave = pygame.sprite.GroupSingle()
        self.grpLblMenu = pygame.sprite.Group()
        self.grpMisc = pygame.sprite.Group()

        # sounds

        self.sndlaser = gameSprites.Sound("minecraftBowSound.mp3")
        self.sndlaser.volume(0.4)
        self.sndbullet = gameSprites.Sound("P226_9mm.mp3")
        self.sndbullet.volume(1.0)
        self.sndpowerup = gameSprites.Sound("eatingsound.mp3")
        self.sndpowerup.volume(0.4)
        self.sndinlys = gameSprites.Sound("inlys.mp3")
        self.sndinlys.volume(0.4)
        self.sndhurt = gameSprites.Sound("steveHurt.mp3")
        self.sndhurt.volume(0.6)
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
        self.playerControls()
        self.process()
        for group in self.groups:
            group.clear(self.screen, self.background)
            group.update()
        for group in self.groups:
            group.draw(self.screen)
        pygame.display.flip()

    def start(self):
        """ sets up the sprite groups
            begins the main loop
        """
        pygame.mouse.set_visible(False)
        self.playerSpriteUp = pygame.sprite.OrderedUpdates(self.player)
        self.grpPlayer.add(self.playerSpriteUp)
        self.miscSpriteUp = pygame.sprite.OrderedUpdates(self.misc)
        self.grpMisc.add(self.miscSpriteUp)

        self.groups = [self.grpLaser, self.grpPowerUp, self.grpBullet, self.grpEnemy, self.grpPlayer,
                       self.grpLblWave]

        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.keepGoing = True
        while self.keepGoing:
            self.__mainLoop()
        pygame.quit()

    def pauseGame(self):
        # temporary just so I remember
        self.paused = True
        while self.paused:
            for group in self.groups:
                group.clear(self.screen, self.background)
                group.update()
            for group in self.groups:
                group.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.paused = False
                self.doEvents(event)
                self.processEvent(event)

            pygame.display.flip()
            # continue button
            if self.isKeyPressed(pygame.K_c):
                pygame.event.post(pygame.event.Event(CONTINUE))
                #self.continueTimer.start = time.time()
                self.paused = False
                # save button
            elif self.isKeyPressed(pygame.K_s):
                pygame.event.post(pygame.event.Event(SAVE))
                # quit button
            elif self.isKeyPressed(pygame.K_q):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                self.paused = False

    def quitGame(self):
        # temporary just so I remember
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        pass

    def saveGame(self):
        # placeholder to figure out how save games work
        pass

    def doEvents(self, event):
        if event.type == PAUSED:
            self.pauseGame()

        if event.type == pygame.QUIT:
            self.saveGame()
            self.stop()

    def nextWave(self):
        if self.enemyNum == 0:
            self.waveNum += 1
            if self.waveNum == 1:
                self.enemyNum = 17
                for i in range(self.enemyNum):
                    for j in range(3):
                        self.joshua = gameSprites.Joshua(self)
                        self.joshua.setSize(round(self.widthRatio*60), round(self.heightRatio*60))
                        self.joshua.position = (round((1080-80)/self.enemyNum*(i+1)*self.widthRatio),
                                                round((80+80*j)*self.heightRatio))
                        self.joshua.add(self.grpEnemy)
                self.enemyNum = 3*self.enemyNum
            elif self.waveNum == 2:
                pass
            elif self.waveNum == 3:
                pass

    def loseLife(self):
        self.lives -= 1
        self.player.position = (round(self.width / 2), self.height - 80*self.heightRatio)
        pygame.mouse.set_pos(self.player.x, self.player.y)
        for bullet in self.grpBullet:
            l = round(self.width/2)-round(200*self.widthRatio)
            u = round(self.width/2)+round(200*self.widthRatio)
            if l <= bullet.x <= u:
                bullet.remove(self.grpBullet)

    def process(self):
        if self.isKeyPressed(pygame.K_p):
            pygame.event.post(pygame.event.Event(PAUSED))
        self.nextWave()
        for enemy in self.grpEnemy:
            if enemy.hp <= 0:
                if enemy.dropPowerUp():
                    self.powerUp = gameSprites.PowerUp(self)
                    self.powerUp.setImage("sepsisLaser.png")
                    self.powerUp.setSize(50*self.widthRatio, 50*self.heightRatio)
                    self.powerUp.x = enemy.x
                    self.powerUp.y = enemy.y
                    self.powerUp.add(self.grpPowerUp)
                self.enemyNum -= 1
                enemy.remove(self.grpEnemy)
            if enemy.shoots() and len(self.grpBullet) <= 10:
                if self.timersndbullet.getTimeLeft() <= 0:
                    self.timersndbullet.start()
                    self.sndbullet.play()
                self.bullet = gameSprites.Bullet(self)
                self.bullet.setImage("boolet.png")
                self.bullet.setSize(30*self.widthRatio, 30*self.heightRatio)
                self.bullet.moveSpeed = 6
                self.bullet.setAngle(180)
                self.bullet.position = enemy.position
                self.bullet.add(self.grpBullet)
            if enemy.collidesWith(self.player):
                self.sndinlys.play()
                self.loseLife()
        for powerup in self.grpPowerUp:
            powerup.drop()
            if powerup.collidesWith(self.player):
                self.sndpowerup.play()
                if self.power < self.maxPower:
                    self.power += 1
                    self.laserSize += 5
                powerup.remove(self.grpPowerUp)
            elif powerup.checkBounds():
                powerup.remove(self.grpPowerUp)
        for bullet in self.grpBullet:
            bullet.moveDown()
            if bullet.checkBounds():
                bullet.remove(self.grpBullet)
            if bullet.collidesWith(self.player):
                self.sndinlys.play()
                bullet.remove(self.grpBullet)
                self.loseLife()
        if self.player.mouseDown and self.player.canShoot():
            self.sndlaser.play()
            self.laser = gameSprites.Bullet(self)
            self.laser.setImage("sepsisLaser.png")
            self.laser.setSize((25+self.laserSize)*self.widthRatio, (25+self.laserSize)*self.heightRatio)
            self.laser.damage += self.power
            self.laser.x = self.player.x
            self.laser.y = self.player.y
            self.laser.add(self.grpLaser)

        for laser in self.grpLaser:
            laser.moveUp()
            if laser.checkBounds():
                laser.remove(self.grpLaser)
            else:
                for enemy in self.grpEnemy:
                    if laser.collidesWith(enemy):
                        self.sndhurt.play()
                        laser.remove(self.grpLaser)
                        enemy.doDamage(laser.damage)


    def playerControls(self):
        if self.isKeyPressed(pygame.K_p):
            pygame.event.post(pygame.event.Event(PAUSED))
        self.player.moveSprite()

    def update(self):
        isPlaying = pygame.mixer.music.get_busy()
        if not isPlaying:
            pygame.mixer.music.play()


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
