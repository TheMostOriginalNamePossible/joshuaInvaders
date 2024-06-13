"""joshuaInvadersMain.py
This will be used exclusively to run the game.

"""

import simpleGE, pygame, json, gameSprites, random

# Constants for your convenience
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Custom Events
PAUSED = pygame.event.custom_type()
CONTINUE = pygame.event.custom_type()
SAVE = pygame.event.custom_type()
BACK = pygame.event.custom_type()
WIN = pygame.event.custom_type()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.setImage("scenepark.png")
        # bool
        self.doStart = False
        self.keepGoing = False
        self.paused = False
        self.starting = False
        self.win = False
        self.gameOver = False
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
        self.timerContinue.totalTime = 3
        self.invincibilityTimer = simpleGE.Timer()
        self.timersndbullet = simpleGE.Timer()
        self.timersndbullet.totalTime = 4
        self.timersndbullet.start()

        # LABEL STUFF

        # menu stuff
        self.btnStart = simpleGE.Button()
        self.btnStart.text = "Start Game"
        self.btnStart.font = pygame.font.Font("freesansbold.ttf", round(20*self.heightRatio))
        self.btnStart.center = (self.width/2, 640*self.heightRatio)
        self.btnStart.size = (150*self.widthRatio, 30*self.heightRatio)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.font = pygame.font.Font("freesansbold.ttf", round(20 * self.heightRatio))
        self.btnQuit.center = (160*self.widthRatio, 640*self.heightRatio)
        self.btnQuit.size = (150*self.widthRatio, 30*self.heightRatio)

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
        self.lblm_instructions.font = pygame.font.Font("freesansbold.ttf", round(20*self.heightRatio))
        self.lblm_instructions.center = (self.width/2, self.height/2)
        self.lblm_instructions.size = (600*self.widthRatio, 320*self.heightRatio)

        self.menuItems = [self.btnStart, self.btnQuit, self.lblm_instructions]

        # stats labels
        self.lblLives = simpleGE.Label()
        self.lblLives.text = f"Lives: {self.lives}"
        self.lblLives.font = pygame.font.Font("freesansbold.ttf", round(20*self.heightRatio))
        self.lblLives.center = (100*self.widthRatio, 640*self.heightRatio)
        self.lblLives.size = (150*self.widthRatio, 30*self.heightRatio)

        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Score: {self.score}"
        self.lblScore.font = pygame.font.Font("freesansbold.ttf", round(20*self.heightRatio))
        self.lblScore.center = (100*self.widthRatio, 600*self.heightRatio)
        self.lblScore.size = (150 * self.widthRatio, 30 * self.heightRatio)
        self.stats = [self.lblLives, self.lblScore]
        # game over

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
        self.playerControls()
        self.process()
        for group in self.groups:
            group.clear(self.screen, self.background)
            group.update()
        for group in self.groups:
            group.draw(self.screen)
        pygame.display.flip()

    def __startMenuLoop(self):
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
        pass
    def __winLoop(self):
        pass
    # START
    def start(self):
        """ sets up the sprite groups
            begins the main loop
        """
        self.doStart = False
        self.starting = False
        self.gameOver = False

        for item in self.menuItems:
            item.add(self.grpMenu)
        self.groups = [self.grpMenu]
        self.screen.blit(self.background, (0, 0))
        self.keepGoing = True

        self.clock = pygame.time.Clock()
        self.keepGoing = True

        while self.keepGoing:
            self.gameSequence()
        pygame.quit()
    def gameSequence(self):
        """This tells how the game should run using the game's boolean variables.

        """
        if not self.doStart:
            self.__startMenuLoop()
        else:
            if self.starting:
                pygame.mouse.set_visible(False)
                pygame.mouse.set_pos(self.width/2, 640*self.heightRatio)
                self.player.add(self.grpPlayer)
                for label in self.stats:
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
            for item in self.menuItems:
                item.remove(self.grpMenu)
        elif self.btnQuit.clicked:
            self.doStart = False
            self.stop()

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

    def wave1(self):
        self.enemyNum = 17
        for i in range(self.enemyNum):
            for j in range(3):
                self.joshua = gameSprites.Joshua(self)
                self.joshua.setSize(round(self.widthRatio * 60), round(self.heightRatio * 60))
                self.joshua.position = (round((1080 - 80) / self.enemyNum * (i + 1) * self.widthRatio),
                                        round((80 + 80 * j) * self.heightRatio))
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
        pygame.mouse.set_pos(self.player.x, self.player.y)
        for bullet in self.grpBullet:
            lower = self.width/2-200*self.widthRatio
            upper = self.width/2+200*self.widthRatio
            if lower <= bullet.x <= upper:
                bullet.remove(self.grpBullet)

    def process(self):
        if self.isKeyPressed(pygame.K_p):
            pygame.event.post(pygame.event.Event(PAUSED))
        self.nextWave()
        self.lblLives.text = f"Lives: {self.lives}"
        self.lblScore.text = f"Score: {self.score}"
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
