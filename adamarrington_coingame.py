import simpleGE, pygame, random
JOSHUA_TIME = 2
TOTAL_TIME = 120


class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.center = (90, 30)
        self.scoreNum = 0
        self.text = f"Score: {self.scoreNum}"

    def addScore(self, value):
        self.scoreNum += value
        self.text = f"Score: {self.scoreNum}"


class LblTimer(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.center = (90, 65)
        self.timer = simpleGE.Timer()
        self.timer.totalTime = TOTAL_TIME
        self.text = f"Time: {self.timer.totalTime}"
        self.timer.start()


class Sound(simpleGE.Sound):
    def __init__(self, file):
        self.sound = pygame.mixer.Sound(file)

    def volume(self, value):
        if type(value) == float:
            self.sound.set_volume(value)
        else:
            self.sound.set_volume(0.5)


class Coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("steak.png")
        self.setSize(25, 25)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.value = 1
        self.reset()

    def reset(self):
        # move to top of screen
        self.y = 10

        # x is random number between 0 and screen width
        self.x = random.randint(0, self.screenWidth)

        # y is random number between min and max speed
        self.dy = random.randint(self.minSpeed, self.maxSpeed)

    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()


class Joshua(Coin):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Joshua.png")
        self.setSize(75, 75)
        self.minSpeed = 7
        self.maxSpeed = 9
        self.value = -1
        self.reset()


class Sunny(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)

        self.setImage("INLYSSunny.png")
        self.setSize(60, 60)
        self.position = (320, 400)
        self.__moveSpeedC = 5
        self.moveSpeed = self.__moveSpeedC
        self.boundAction = self.STOP

    def setStopLeft(self):
        if self.left+29 < 0:
            self.moveSpeed = 0
        else:
            self.moveSpeed = self.__moveSpeedC

    def setStopRight(self):
        if self.right-29 > self.screenWidth:
            self.moveSpeed = 0
        else:
            self.moveSpeed = self.__moveSpeedC

    def process(self):
        self.moveSpeed = self.__moveSpeedC
        if self.isKeyPressed(pygame.K_LEFT):
            self.setStopLeft()
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.setStopRight()
            self.x += self.moveSpeed


class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        pygame.mixer.music.load("neverlikedyoursmile.mp3")
        pygame.mixer.music.set_volume(0.2)
        self.setImage("scenepark.png")

        self.timer = simpleGE.Timer()
        self.timer.totalTime = TOTAL_TIME
        self.timerJ = simpleGE.Timer()
        self.timingJ = False
        self.timerJ.totalTime = JOSHUA_TIME

        self.lblTimer = LblTimer()
        self.lblScore = LblScore()

        self.sunny = Sunny(self)

        self.numJoshuas = 2
        self.joshuas = []
        for i in range(self.numJoshuas):
            self.joshuas.append(Joshua(self))

        self.numCoins = 10
        self.coins = []
        for i in range(self.numCoins):
            self.coins.append(Coin(self))

        self.sndcoin = Sound("eatingsound.mp3")
        self.sndcoin.volume(0.4)
        self.sndinlys = Sound("inlys.mp3")
        self.sndinlys.volume(0.3)

        self.sprites = [self.sunny, self.coins, self.joshuas, self.lblScore, self.lblTimer]

        pygame.mixer.music.play()

    def process(self):
        for coin in self.coins:
            if coin.collidesWith(self.sunny):
                coin.reset()
                self.sndcoin.play()
                self.lblScore.addScore(coin.value)
        for joshua in self.joshuas:
            if joshua.collidesWith(self.sunny):
                self.sndinlys.play()
                self.lblScore.addScore(joshua.value)
                self.sunny.setImage("INLYSSunnyP.png")
                self.sunny.setSize(60, 60)
                joshua.reset()
                self.timingJ = True
                self.timerJ.start()

        if self.timingJ:
            if 0 >= self.timerJ.getTimeLeft():
                self.sunny.setImage("INLYSSunny.png")
                self.sunny.setSize(60, 60)
                self.timingJ = False

    def update(self):
        isPlaying = pygame.mixer.music.get_busy()
        if not isPlaying:
            pygame.mixer.music.play()
        timeLeft = round(self.timer.getTimeLeft())
        self.lblTimer.text = f"Time: {timeLeft}"
        if self.timer.getTimeLeft() <= 0:
            self.stop()


class Instructions(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.s = False
        self.prevScore = 0
        self.setImage("scenepark.png")

        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = ["You are Sunny.",
                                     "Move with the left and right arrow keys.",
                                     "Collect as many steaks as possible.",
                                     "Avoid Joshua.",
                                     f"You have {TOTAL_TIME} seconds to collect steak",
                                     "",
                                     "Good Luck"
                                     ]
        self.directions.center = (320, 240)
        self.directions.size = (500, 250)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (100, 400)

        self.btnStart = simpleGE.Button()
        self.btnStart.text = "Play"
        self.btnStart.center = (540, 400)

        self.lblPrevScore = simpleGE.Label()
        self.lblPrevScore.text = f"Prev Score: 0"
        self.lblPrevScore.fgColor = (0x00, 0x00, 0x00)
        self.lblPrevScore.bgColor = (0xCC, 0xCC, 0xCC)
        self.lblPrevScore.center = (320, 400)

        self.sprites = [self.directions, self.btnStart, self.btnQuit, self.lblPrevScore]

    def process(self):
        if self.btnStart.clicked:
            self.s = True
            self.stop()

        if self.btnQuit.clicked:
            self.stop()


def main():
    playing = True
    lastScore = 0
    while playing:
        instructions = Instructions()
        instructions.prevScore = lastScore
        instructions.lblPrevScore.text = f"Prev Score: {lastScore}"
        instructions.start()
        if instructions.s:
            game = Game()
            game.start()
            lastScore = game.lblScore.scoreNum
        else:
            playing = False


if __name__ == "__main__":
    main()
