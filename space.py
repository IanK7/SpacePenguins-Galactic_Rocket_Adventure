from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *
import time


# Constants
FPS = 30
SCREENWIDTH = 800
SCREENHEIGHT = 512
PIPEGAPSIZE = 170
BASEY = SCREENHEIGHT * 0.9
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# sprites
PLAYERS_LIST = (
    # penguin sprites
    (
        'assets/sprites/spacep.png',
        'assets/sprites/spacepfire.png',
        'assets/sprites/spacep.png',
    ),

    (
        'assets/sprites/spacepR.png',
        'assets/sprites/spacepRfire.png',
        'assets/sprites/spacepR.png',
    ),

    (
        'assets/sprites/spacepB.png',
        'assets/sprites/spacepBfire.png',
        'assets/sprites/spacepB.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/Background-space.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/meteor.png',
    'assets/sprites/meteor.png',
)

try:
    xrange
except NameError:
    xrange = range


# scroll background function
def scrollBackground(background, x, y):
    rel_x = x % background.get_rect().width
    SCREEN.blit(background, (rel_x - background.get_rect().width, y))
    if rel_x < SCREENWIDTH:
        SCREEN.blit(background, (rel_x, y))


# main function
def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Space Penguin: Galactic Rocket Adventure')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/game over.png').convert_alpha()
    # Pause Sprite
    IMAGES['pause'] = pygame.image.load('assets/sprites/pause.png').convert_alpha()
    # message sprite for start screen
    IMAGES['message'] = pygame.image.load('assets/sprites/start1.png').convert_alpha()
    IMAGES['message1'] = pygame.image.load('assets/sprites/message1.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    #gio
    #powerup sprites
    IMAGES['powershield'] = pygame.image.load('assets/sprites/power_shield.png')
    IMAGES['powershield'] = pygame.transform.scale(IMAGES['powershield'], (60, 50))
    IMAGES['life'] = pygame.image.load('assets/sprites/squidpedo_00.png')
    IMAGES['life'] = pygame.transform.scale(IMAGES['life'], (60, 50))

    IMAGES['a'] = (
        pygame.transform.scale(pygame.image.load('assets/sprites/power_shield.png'), (60, 50)),
        pygame.transform.scale(pygame.image.load('assets/sprites/squidpedo_00.png'), (60, 50))
    )

    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    # Load the background music
    pygame.mixer.music.load("assets/audio/ambient.wav")

    # Start playing the background music
    pygame.mixer.music.play(loops=-1)

    # Adjust the volume
    pygame.mixer.music.set_volume(0.25)

    SOUNDS['die'] = pygame.mixer.Sound('assets/audio/fail' + soundExt)
    SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/fail' + soundExt)
    SOUNDS['point'] = pygame.mixer.Sound('assets/audio/success' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/spaceship' + soundExt)

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.flip(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hitmask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )
        #gio
        HITMASKS['powershield'] = (getHitmask(IMAGES['powershield']))
        HITMASKS['life'] = (getHitmask(IMAGES['life']))
        

        movementInfo = showStartAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)


# start menu
def showStartAnimation():
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0


    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * -0.25)

    messagea = int((SCREENWIDTH - IMAGES['message1'].get_width()))
    messageb = int(SCREENHEIGHT * 0.6)

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                SOUNDS['wing'].play()
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'playerIndexGen': playerIndexGen,
                }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0))
        SCREEN.blit(IMAGES['player'][playerIndex], (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['message1'], (messagea, messageb))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# main game function
def mainGame(movementInfo, player=None):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 10, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 10 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    #gio
    newPowerUp = getRandomPowerup()
    powerups = [
        {'x': SCREENWIDTH, 'y': newPowerUp[0]['y'], 'type': newPowerUp[0]['type']} 
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    dt = FPSCLOCK.tick(FPS) / 1000
    pipeVelX = -128 * dt

    # player velocity, max velocity, downward acceleration, acceleration on flap
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerRot = 50
    playerVelRot = 3
    playerRotThr = 20
    playerFlapAcc = -9
    playerFlapped = False
    background_x = 0
    background_speed = 70 * dt
    paused = False
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    in_use = None
    start = 0
    end = 0      

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS['wing'].play()
            if event.type == KEYDOWN and event.key == K_b:
                paused = not paused
                # Display Pause when paused
                if paused:
                    SCREEN.blit(IMAGES['pause'], (195, 150))
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                while paused:
                    for event in pygame.event.get():
                        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                            pygame.quit()
                            sys.exit()
                        if event.type == KEYDOWN and event.key == K_SPACE:
                            paused = not paused
                            break

        # scroll the background
        background_x -= background_speed
        scrollBackground(IMAGES['background'], background_x, 0)

        # reset the x position of the background when it goes off the screen
        if background_x <= -IMAGES['background'].get_width():
            background_x = 0

        #gio
        powerUse = powerCrash({'x': playerx, 'y': playery, 'index': playerIndex}, powerups)
        in_use = usePowerUp(powerUse, powerups, in_use)
        print(in_use)
        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex}, upperPipes, lowerPipes)
        if in_use == 'shield':
            if end == 0:
                start = score
                end = start + 2
            if score >= end:
                in_use = None
                start = 0
                end = 0
        elif in_use == 'life':
            score += 2
            in_use = None
        elif in_use == None and  crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot
            }
        elif score % 4 == 0:
            in_use = None

        
        
        # check for score
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDS['point'].play()

        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # rotate the player
        if playerRot > -90:
            playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerRot = 50

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        #gio
        for p in powerups:
            p['x'] += pipeVelX

        if 3 > len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5 and score % 5 == 0:
            newPowerUp = getRandomPowerup()
            powerups.append(newPowerUp[0])

         # remove first pipe if its out of the screen
        if len(powerups) > 1 and powerups[0]['x'] < -IMAGES['pipe'][0].get_width():
            powerups.pop(0)

        # add new pipe when first pipe is about to touch left of screen
        if 3 > len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if len(upperPipes) > 0 and upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        #gio
        for p in powerups:
            SCREEN.blit(IMAGES[p['type']], (p['x'], p['y']))

        # print score so player overlaps the score
        showScore(score)

        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot

        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# game over function
def showGameOverScreen(crashInfo):
    """crashes the player down and shows gameover image"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    basex = crashInfo['basex']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
        SOUNDS['die'].play()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        showScore(score)

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx, playery))
        SCREEN.blit(IMAGES['gameover'], (
        SCREENWIDTH / 2 - IMAGES['gameover'].get_width() / 2, SCREENHEIGHT / 2 - IMAGES['gameover'].get_height() / 2))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


#
def playerShm(playerShm):
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
        playerShm['val'] += 1
    else:
        playerShm['val'] -= 1

#gio
def getRandomPowerup():
    gapY = 0
    pos = random.randrange(0, len(IMAGES['a']))
    gapY = random.randrange(120, 130)
    powerUpHeight = IMAGES['a'][pos].get_height()
    powerUpX = SCREENWIDTH

    if pos == 0:
        return [{'x': powerUpX, 'y': gapY + powerUpHeight, 'type': 'powershield'}]
    elif pos == 1:
        return [{'x': powerUpX, 'y': gapY + powerUpHeight, 'type': 'life'}]


def getRandomPipe():
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE},
    ]


def showScore(score):
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = 10

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, 10))
        Xoffset += IMAGES['numbers'][digit].get_width()

#gio
def powerCrash(player, pipe):
    if pipe:
        pipe_dict = pipe[0]
        pi = player['index']
        player['w'] = IMAGES['player'][0].get_width()
        player['h'] = IMAGES['player'][0].get_height()

        playerRect = pygame.Rect(player['x'], player['y'], player['w'], player['h'])
        pipeW = IMAGES[pipe_dict['type']].get_width()
        pipeH = IMAGES[pipe_dict['type']].get_height()

        # pipe rect
        pipeRect = pygame.Rect(pipe[0]['x'], pipe[0]['y'], pipeW, pipeH)

        # player and pipe hitmasks
        pHitMask = HITMASKS['player'][pi]
        pipeHitmask = HITMASKS[pipe_dict['type']]

        # check if bird collided with pipe
        pipeCollide = pixelCollision(playerRect, pipeRect, pHitMask, pipeHitmask)

        if pipeCollide:
            return [True, pipe_dict['type'], pipeRect] 
    else:
        return [False]
    
def usePowerUp(resultado, powerups,in_use):
    if resultado:
        if resultado[0] == True:
            if resultado[1] == 'powershield':
                powerups.pop(0)
                in_use = 'shield'
            elif resultado[1] == 'life':
                powerups.pop(0)
                in_use =  'life'
    return in_use   

def checkCrash(player, upperPipes, lowerPipes):
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'], player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]


def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False


def getHitmask(image):
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


if __name__ == '__main__':
    main()
