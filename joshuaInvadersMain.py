"""joshuaInvadersMain.py
Runs a type of space invaders game. I wanted to make it kind of like a game I played in my childhood called
Chicken Invaders.
"""

import simpleGE, pygame, json, gameSprites, random

# Constants for your convenience
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# Custom Events
PAUSED = pygame.event.custom_type()
SAVE = pygame.event.custom_type()
BACK = pygame.event.custom_type()
WIN = pygame.event.custom_type()
GAME_OVER = pygame.event.custom_type()
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.setImage("scenepark.png")

        # boolean variables
        self.doStart = False
        self.keepGoing = False
        self.paused = False
        self.starting = False
        self.win = False
        self.gameOver = False
        self.menuStart = False

        # Numbers
        self.enemyNum = 0
        self.waveNum = 0
        self.lives = 3
        self.laserSize = 0
        self.power = 0
        self.maxPower = 5
        self.score = 0

        # screen adaptability
        self.width = SCREEN_WIDTH
        self.widthRatio = SCREEN_WIDTH / 1080
        self.height = SCREEN_HEIGHT
        self.heightRatio = SCREEN_HEIGHT / 720

        # timers
        self.timerContinue = simpleGE.Timer()
        self.timerContinue.totalTime = 1
        self.invincibilityTimer = simpleGE.Timer()
        self.timersndbullet = simpleGE.Timer()
        self.timersndbullet.totalTime = 4
        self.timersndbullet.start()

        # font and size
        self.font = pygame.font.Font("freesansbold.ttf", round(20*self.heightRatio))
        self.font2 = pygame.font.Font("freesansbold.ttf", round(40*self.heightRatio))
        self.lblDefSize = (150*self.widthRatio, 30*self.heightRatio)
        self.lblDefSize2 = (300*self.widthRatio, 60*self.heightRatio)
        self.screenCenter = (self.width/2, self.height/2)

        # buttons
        self.btnStart = simpleGE.Button()
        self.btnStart.text = "Start Game"
        self.btnStart.font = self.font
        self.btnStart.center = (self.width/2, 640*self.heightRatio)
        self.btnStart.size = self.lblDefSize

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.font = self.font
        self.btnQuit.center = (360*self.widthRatio, 640*self.heightRatio)
        self.btnQuit.size = self.lblDefSize

        self.btnStartOver = simpleGE.Button()
        self.btnStartOver.text = "Start Over"
        self.btnStartOver.font = self.font
        self.btnStartOver.center = self.btnStart.center
        self.btnStartOver.size = self.lblDefSize

        self.btnContinue = simpleGE.Button()
        self.btnContinue.text = "Continue"
        self.btnContinue.font = self.font
        self.btnContinue.center = self.btnStart.center
        self.btnContinue.size = self.lblDefSize
        # labels
        self.lblm_instructions = simpleGE.MultiLabel()
        self.lblm_instructions.textLines = ["Shoot Joshuas and avoid touching bullets and Joshua.",
                                            "Move your cursor around to move Sunny.",
                                            "Use the Left Mouse Button to shoot laser balls.",
                                            "Steaks give lives. Falling laser balls",
                                            "make your laser balls larger and do more damage.",
                                            "Your cursor will be hidden and automatically",
                                            "move to the Start Game button ",
                                            "when Start Game is clicked."
                                            ]
        self.lblm_instructions.font = self.font
        self.lblm_instructions.center = self.screenCenter
        self.lblm_instructions.size = (600*self.widthRatio, 320*self.heightRatio)

        # end labels
        self.lblGameOver = simpleGE.Label()
        self.lblGameOver.text = "Game Over"
        self.lblGameOver.font = self.font2
        #self.lblGameOver.clearBack = True
        self.lblGameOver.center = self.screenCenter
        self.lblGameOver.size = self.lblDefSize2

        self.lblWin = simpleGE.Label()
        self.lblWin.text = "You Win"
        self.lblWin.font = self.font2
        #self.lblWin.clearBack = True
        self.lblWin.center = self.screenCenter
        self.lblWin.size = self.lblDefSize2

        self.lblPaused = simpleGE.Label()
        self.lblPaused.text = "Paused"
        self.lblPaused.font = self.font2
        self.lblPaused.center = self.screenCenter
        self.lblPaused.size = self.lblDefSize2

        # stats labels
        self.lblLives = simpleGE.Label()
        self.lblLives.text = f"Lives: {self.lives}"
        self.lblLives.font = self.font
        self.lblLives.center = (100*self.widthRatio, 640*self.heightRatio)
        self.lblLives.size = self.lblDefSize

        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Score: {self.score}"
        self.lblScore.font = self.font
        self.lblScore.center = (100*self.widthRatio, 600*self.heightRatio)
        self.lblScore.size = self.lblDefSize

        self.lblPower = simpleGE.Label()
        self.lblPower.text = f"Power: {self.power}"
        self.lblPower.font = self.font
        self.lblPower.center = (980*self.widthRatio, 640*self.heightRatio)
        self.lblPower.size = self.lblDefSize

        # lists
        self.lstStats = [self.lblLives, self.lblScore, self.lblPower]
        self.lstStart = [self.btnStart, self.btnQuit, self.lblm_instructions]
        self.lstGameOver = [self.btnQuit, self.btnStartOver, self.lblGameOver]
        self.lstWin = [self.lblWin, self.btnQuit, self.btnStartOver]
        self.lstPause = [self.btnContinue, self.btnQuit,]

        # sprites
        self.player = gameSprites.Player(self)
        self.player.setSize(60*self.widthRatio, 60*self.heightRatio)
        self.joshua = gameSprites.Joshua(self)
        self.life = gameSprites.Life(self)
        self.powerUp = gameSprites.PowerUp(self)

        # groups
        self.grpPowerUp = pygame.sprite.Group()
        self.grpLaser = pygame.sprite.Group()
        self.grpPlayer = pygame.sprite.GroupSingle()
        self.grpEnemy = pygame.sprite.Group()
        self.grpBullet = pygame.sprite.Group()
        self.grpLblWave = pygame.sprite.GroupSingle()
        self.grpMenu = pygame.sprite.Group()
        self.grpMisc = pygame.sprite.Group()
        self.grpLblStats = pygame.sprite.Group()

        # sounds, music, and volume
        pygame.mixer.music.load("neverlikedyoursmile.mp3")
        pygame.mixer.music.set_volume(0.4)
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
        # random constants for convenience

    # LOOP METHODS
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
        self.playerProcesses()

        for group in self.groups:
            group.clear(self.screen, self.background)
            group.update()
        for group in self.groups:
            group.draw(self.screen)
        pygame.display.flip()

    def __menuLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keepGoing = False
                self.stop()
            self.doEvents(event)
            self.processEvent(event)
        self.menuProcess()
        for group in self.groups:
            group.clear(self.screen, self.background)
            group.update()
        for group in self.groups:
            group.draw(self.screen)
        pygame.display.flip()

    def __gameOverLoop(self):
        if self.menuStart:
            for group in self.groups:
                for item in group:
                    item.remove(group)
            for item in self.lstGameOver:
                item.add(self.grpMenu)
            self.groups = [self.grpMenu]
            self.screen.blit(self.background, (0, 0))
            self.menuStart = False
            pygame.mouse.set_visible(True)
        self.__menuLoop()

    def __winLoop(self):
        if self.menuStart:
            for group in self.groups:
                for item in group:
                    item.remove(group)
            for item in self.lstWin:
                item.add(self.grpMenu)
            self.groups = [self.grpMenu]
            self.screen.blit(self.background, (0, 0))
            self.menuStart = False
            pygame.mouse.set_visible(True)
        self.__menuLoop()

    def start(self):
        """ sets up the sprite groups
            begins the main loop
        """
        self.clock = pygame.time.Clock()
        for item in self.lstStart:
            item.add(self.grpMenu)
        self.groups = [self.grpMenu]
        self.screen.blit(self.background, (0, 0))

        self.keepGoing = True

        while self.keepGoing:
            self.gameSequence()
        pygame.quit()

    def gameSequence(self):
        """This tells how the game should run using the game's boolean variables.

        """
        if not self.doStart:
            self.__menuLoop()
        else:
            if self.starting:
                self.enemyNum = 0
                self.waveNum = 0
                self.lives = 3
                self.laserSize = 0
                self.power = 0
                self.score = 0
                pygame.mouse.set_visible(False)
                pygame.mouse.set_pos(self.width/2, 640*self.heightRatio)
                self.player.position = (self.width/2, 640*self.heightRatio)
                self.player.add(self.grpPlayer)
                for label in self.lstStats:
                    label.add(self.grpLblStats)
                self.groups = [self.grpLaser, self.grpPowerUp, self.grpBullet, self.grpEnemy, self.grpPlayer,
                               self.grpLblWave, self.grpLblStats, self.grpMenu]

                self.screen.blit(self.background, (0, 0))
                self.starting = False
            if not self.gameOver and not self.win:
                self.__mainLoop()
            elif self.gameOver:
                self.__gameOverLoop()
            elif self.win:
                self.__winLoop()

    def menuProcess(self):
        if self.btnStart.clicked:
            self.doStart = True
            self.starting = True
            self.btnStart.clicked = False
            for item in self.lstStart:
                item.remove(self.grpMenu)
        elif self.btnStartOver.clicked:
            self.starting = True
            self.btnStartOver.clicked = False
            self.gameOver = False
            self.win = False
            for item in self.lstGameOver:
                item.remove(self.grpMenu)
            for item in self.lstWin:
                item.remove(self.grpMenu)
        elif self.btnQuit.clicked:
            self.doStart = False
            self.stop()

    def pauseGame(self):
        # temporary just so I remember
        self.paused = True
        for item in self.lstPause:
            item.add(self.grpMenu)
        pygame.mouse.set_visible(True)
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
            if self.btnContinue.clicked:
                for item in self.lstPause:
                    item.remove(self.grpMenu)
                self.paused = False
            # quit button
            elif self.btnQuit.clicked:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                self.paused = False

    def saveGame(self):
        # This is scrap (for now)
        pass

    def doEvents(self, event):
        if event.type == PAUSED:
            self.pauseGame()
        if event.type == SAVE:
            self.saveGame()
        if event.type == pygame.QUIT:
            self.saveGame()
            self.stop()
        if event.type == WIN:
            self.win = True
            self.menuStart = True
        elif event.type == GAME_OVER:
            self.gameOver = True
            self.menuStart = True

    def wave1(self):
        self.enemyNum = 17
        for i in range(self.enemyNum):
            for j in range(3):
                self.joshua = gameSprites.Joshua(self)
                self.joshua.setSize(self.widthRatio * 60, self.heightRatio * 60)
                self.joshua.position = (1000 / self.enemyNum * (i + 1) * self.widthRatio,
                                        (80 + 80 * j) * self.heightRatio)
                self.joshua.add(self.grpEnemy)
        self.enemyNum = 3 * self.enemyNum

    def nextWave(self):
        if self.enemyNum == 0:
            self.waveNum += 1
            if self.waveNum == 1:
                self.wave1()
            elif self.waveNum == 2:
                self.wave1()
            elif self.waveNum == 3:
                self.wave1()
            else:
                pygame.event.post(pygame.event.Event(WIN))

    def loseLife(self):
        self.lives -= 1
        self.player.position = (self.width/2, 640*self.heightRatio)
        pygame.mouse.set_pos(self.width/2, 640*self.heightRatio)
        for bullet in self.grpBullet:
            lower = self.width/2-200*self.widthRatio
            upper = self.width/2+200*self.widthRatio
            if lower <= bullet.x <= upper:
                bullet.remove(self.grpBullet)

    def process(self):
        self.nextWave()
        for enemy in self.grpEnemy:
            if enemy.hp <= 0:
                self.score += 1
                if enemy.dropPowerUp():
                    rand = random.randint(1, 2)
                    if rand == 1:
                        self.powerUp = gameSprites.PowerUp(self)
                        self.powerUp.setImage("sepsisLaser.png")
                        self.powerUp.setSize(50*self.widthRatio, 50*self.heightRatio)
                        self.powerUp.x = enemy.x
                        self.powerUp.y = enemy.y
                        self.powerUp.add(self.grpPowerUp)
                    elif rand == 2:
                        self.life = gameSprites.Life(self)
                        self.life.setImage("Steak.png")
                        self.life.setSize(50*self.widthRatio, 50*self.heightRatio)
                        self.life.x = enemy.x
                        self.life.y = enemy.y
                        self.life.add(self.grpPowerUp)
                self.enemyNum -= 1
                enemy.remove(self.grpEnemy)
            if enemy.shoots() and len(self.grpBullet) <= 100:
                if self.timersndbullet.getTimeLeft() <= 0:
                    self.timersndbullet.start()
                    self.sndbullet.play()
                self.bullet = gameSprites.Bullet(self)
                self.bullet.setImage("boolet.png")
                self.bullet.setSize(25*self.widthRatio, 25*self.heightRatio)
                self.bullet.moveSpeed = 6
                self.bullet.setAngle(180)
                self.bullet.position = enemy.position

                self.bullet.add(self.grpBullet)
            if enemy.collidesWith(self.player):
                self.score -= 1
                self.sndinlys.play()
                self.loseLife()
        for powerup in self.grpPowerUp:
            powerup.drop()
            if powerup.collidesWith(self.player):
                self.score += 1
                self.sndpowerup.play()
                if type(powerup) == type(self.powerUp):
                    if self.power < self.maxPower:
                        self.power += 1
                        self.laserSize += 5
                elif type(powerup) == type(self.life):
                    self.lives += 1
                powerup.remove(self.grpPowerUp)
            elif powerup.checkBounds():
                powerup.remove(self.grpPowerUp)
        for bullet in self.grpBullet:
            bullet.moveDown()
            if bullet.checkBounds():
                bullet.remove(self.grpBullet)
            if bullet.collidesWith(self.player):
                self.score -= 1
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

    def playerProcesses(self):
        if self.isKeyPressed(pygame.K_p):
            pygame.event.post(pygame.event.Event(PAUSED))
        self.player.moveSprite()
        if self.lives <= 0:
            pygame.event.post(pygame.event.Event(GAME_OVER))

    def update(self):
        isPlaying = pygame.mixer.music.get_busy()
        if not isPlaying:
            pygame.mixer.music.play()
        self.lblLives.text = f"Lives: {self.lives}"
        self.lblScore.text = f"Score: {self.score}"
        self.lblPower.text = f"Power: {self.power}"


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
