### Zeenat ###
### Game ###
### Core structure modified from pygamegame.py created by Lukas Peraza ###

import os
import sys
import random
import pygame
import math
from tkinter import *

#################################################
# Constants
#################################################

# assets folder
image_folder = os.path.join(os.path.dirname(__file__), 'images')
sound_folder = os.path.join(os.path.dirname(__file__), 'sounds')


# constants
WIDTH = 600
HEIGHT = 800
FPS = 60
TITLE = "Stack Jump"

BRICKW = 150
BRICKH = 75

# define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)

GOOGLEGREEN = (60, 186, 84)
GOOGLEYELLOW = (244, 194, 13)
GOOGLERED = (219, 50, 54)
GOOGLEBLUE = (72, 133, 237)

# define brick colors shere
COLORS = [GOOGLERED, GOOGLEBLUE, GOOGLEGREEN, GOOGLEYELLOW, ORANGE]

SCORE = 0
STREAK = 0

# speed is initialized at 3
# SPEED 3-6 is largely playable
SPEED = 3
MODE = "start"

ISPLAYINGSOUND = False
SECONDCHANCE = False

# pick your starting charater here
CHARACTER = "tiger"

NAME = "__________"

#################################################
# Initializations
#################################################

# initialize everything
pygame.mixer.init()  # for sound
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# set the title of the window
pygame.display.set_caption(TITLE)

# simmered the background music down a little
pygame.mixer.music.set_volume(0.2)

# change in-game fonts here
font_name = pygame.font.match_font('Showcard Gothic')

# load songs
startScreenSong = pygame.mixer.music.load(
    os.path.join(sound_folder, "jump-VH.mp3"))
jumpingSound1 = pygame.mixer.Sound(
    os.path.join(sound_folder, 'jumping_sound_1.ogg'))
jumpingSound2 = pygame.mixer.Sound(
    os.path.join(sound_folder, 'jumping_sound_2.ogg'))
gameOverSound = pygame.mixer.Sound(
    os.path.join(sound_folder, 'gameOverSound.ogg'))
streakSound = pygame.mixer.Sound(
    os.path.join(sound_folder, 'streaksoundend.ogg'))
meowSound = pygame.mixer.Sound(
    os.path.join(sound_folder, 'meow.ogg'))
purrSound = pygame.mixer.Sound(
    os.path.join(sound_folder, 'purr.ogg'))
reviveSound = pygame.mixer.Sound(
    os.path.join(sound_folder, 'revive.ogg'))

# load images
startScreenPic = pygame.image.load(os.path.join(
    image_folder, "startScreen.jpg")).convert()
characterScreenPic = pygame.image.load(os.path.join(
    image_folder, "characterScreen.png")).convert()
challengeScreenPic = pygame.image.load(os.path.join(
    image_folder, "challengeScreen.png")).convert()
helpScreenPic = pygame.image.load(os.path.join(
    image_folder, "help.png")).convert()
leaderboardPic = pygame.image.load(os.path.join(
    image_folder, "leaderboard.png")).convert()

#################################################
# Helper Functions
#################################################


def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))


# for random pick out of two things
def flipACoin():
    # flip a coin
    flip = random.randint(0, 1)
    if flip == 0:
        return "Heads"
    else:
        return "Tails"


def draw_text(surf, text, size, x, y, color):
    # selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    # True denotes the font to be anti-aliased
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_rectangle(surf, cx, cy, w, h, color=BLACK):
    return pygame.draw.rect(surf, color, (cx - w / 2, cy - h / 2, w, h))


def draw_triangle(surf, lx, ly, s, color=BLACK):
    point1 = (lx, ly)
    point2 = (lx + s / 2, ly - s)
    point3 = (lx + s, ly)
    return pygame.draw.polygon(surf, color, [point1, point2, point3])


def draw_triangle2(surf, lx, ly, s, color=BLACK):
    point1 = (lx, ly)
    point2 = (lx + s / 2, ly - 2 * s)
    point3 = (lx + s, ly)
    return pygame.draw.polygon(surf, color, [point1, point2, point3])


# modified from hw6
def draw_star(surf, cx, cy, diameter, numPoints, color=BLACK):
    r = diameter / 2
    innerCircleRatio = 0.382
    points = []
    pi = math.pi
    for point in range(numPoints):
        # find the angle of both the outer points and draw these points
        # formulas derived from Mr.Kosbie's clock example
        outerPointAngle = pi / 2 - (2 * pi) * (point / numPoints)
        outerPointX = cx + r * math.cos(outerPointAngle)
        outerPointY = cy - r * math.sin(outerPointAngle)
        # repeat with the innerPointAngle for points on the inner circle
        innerPointAngle = outerPointAngle - pi / numPoints
        innerPointX = cx + innerCircleRatio * r * math.cos(innerPointAngle)
        innerPointY = cy - innerCircleRatio * r * math.sin(innerPointAngle)
        # append all points into a list for easy accessibility and clarity
        outerCoordinates = (outerPointX, outerPointY)
        innerCoordinates = (innerPointX, innerPointY)
        points.append(outerCoordinates)
        points.append(innerCoordinates)
    return pygame.draw.polygon(surf, color, points)


def draw_circle(surf, cx, cy, r, color=BLACK):
    return pygame.draw.circle(surf, color, [cx, cy], r)

# taken from 112 website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# modified from 112 website
def writeToFile(path, contents):
    with open(path, "a") as f:
        f.write(contents)

# Close the main window
def close():
    pygame.quit()
    sys.exit()


#################################################
# Main Screens
#################################################

### create the main menu ###
def main_menu():
    global screen, rankingsPic

    menu_song = startScreenSong
    pygame.mixer.music.play(-1)

    startScreen = startScreenPic
    startScreen = pygame.transform.scale(startScreen, (WIDTH, HEIGHT), screen)

    screen.blit(startScreen, (0, 0))
    pygame.display.update()

    player = Player(150, 150, WIDTH // 2 - 75, HEIGHT // 2 - 80)
    player.draw()

    pygame.draw.rect(screen, WHITE, [WIDTH / 2 - 80, HEIGHT / 2 + 320, 160, 50], 2)
    draw_text(screen, "LEADERBOARD", 20, WIDTH / 2, HEIGHT / 2 + 335, WHITE)

    pygame.draw.rect(screen, WHITE, [WIDTH / 2 + 160, HEIGHT / 2 + 320, 80, 50], 2)
    draw_text(screen, "HELP", 20, WIDTH / 2 + 200, HEIGHT / 2 + 335, WHITE)

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break

            elif ev.key == pygame.K_SPACE:
                flip = flipACoin()
                if not ISPLAYINGSOUND:
                    if flip == "Heads":
                        purrSound.play()
                    else:
                        meowSound.play()

            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()

        elif ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if distance(pos, (300, 600)) <= 100:
                break
            elif distance(pos, (100, 600)) <= 75:
                characterScreen()
            elif distance(pos, (500, 600)) <= 75:
                challengeScreen()
            elif distance(pos, (300, 750)) <= 60:
                drawLeaderboard()
            elif distance(pos, (500, 750)) <= 40:
                helpScreen()

        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()

        else:
            draw_text(screen, "Press [SPACE] for",
                      15, WIDTH / 3, HEIGHT / 3 - 15, WHITE)
            draw_text(screen, "SURPRISE!", 25,
                      WIDTH / 3, HEIGHT / 3 + 25, WHITE)
        pygame.display.update()

    # pygame.mixer.music.stop()
    ready = pygame.mixer.Sound(os.path.join(sound_folder, 'getready.ogg'))
    ready.play()

    screen.fill(BLACK)
    draw_text(screen, "GET READY!", 40, WIDTH / 2, HEIGHT / 2, WHITE)
    pygame.display.update()


### create the leaderboard page ###

# sort everything from .txt file
def sortContents(file):
    contents = readFile(file)
    joinedContents = "~".join(contents.split("\n"))
    joinedContents = joinedContents[:-1]
    newContents = joinedContents.split("~")
    return set(newContents)

# create a list of ranked players
def rankContents(contents):
    new = []
    for item in contents:
        new.append(item.split(","))
    rankings = dict()
    scores = []
    for item in new:
        name = item[1]
        score = int(item[0])
        scores.append(score)
        rankings[name] = str(score)
    stdscores = sorted(scores, reverse=True)
    result = []
    leaders = []
    for i in range(0, len(stdscores)):
        result.append(str(stdscores[i]))
    for score in result:
        for name in rankings:
            if rankings[name] == score:
                nameScore = name + "          " + score
                leaders.append(nameScore)
    return leaders


# draw the leaderboard
def drawLeaderboard():
    global LEADERBOARD

    leaderboard = leaderboardPic
    leaderboard = pygame.transform.scale(leaderboard, (WIDTH, HEIGHT), screen)

    screen.blit(leaderboard, (0, 0))
    pygame.display.update()

    readLeaderboard = sortContents("leaderboard.txt")
    contents = rankContents(readLeaderboard)

    draw_text(screen, "1." + contents[0], 40,
              WIDTH / 2, HEIGHT / 8, WHITE)
    draw_text(screen, "2." + contents[1], 40,
              WIDTH / 2, HEIGHT / 8 + 70, WHITE)
    draw_text(screen, "3." + contents[2], 40,
              WIDTH / 2, HEIGHT / 8 + 140, WHITE)
    draw_text(screen, "4." + contents[3], 40,
              WIDTH / 2, HEIGHT / 8 + 210, WHITE)
    draw_text(screen, "5." + contents[4], 40,
              WIDTH / 2, HEIGHT / 8 + 280, WHITE)
    draw_text(screen, "6." + contents[5], 40,
              WIDTH / 2, HEIGHT / 8 + 350, WHITE)
    draw_text(screen, "7." + contents[6], 40,
              WIDTH / 2, HEIGHT / 8 + 420, WHITE)
    draw_text(screen, "8." + contents[7], 40,
              WIDTH / 2, HEIGHT / 8 + 490, WHITE)
    draw_text(screen, "9." + contents[8], 40,
              WIDTH / 2, HEIGHT / 8 + 560, WHITE)
    draw_text(screen, "10." + contents[9],
              40, WIDTH / 2, HEIGHT / 8 + 630, WHITE)

    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if distance(pos, (40, 40)) <= 40:
                startScreen = startScreenPic
                startScreen = pygame.transform.scale(
                    startScreen, (WIDTH, HEIGHT), screen)
                screen.blit(startScreen, (0, 0))
                pygame.draw.rect(screen, WHITE, [WIDTH / 2 - 80, HEIGHT / 2 + 320, 160, 50], 2)
                draw_text(screen, "LEADERBOARD", 20,WIDTH / 2, HEIGHT / 2 + 335, WHITE)

                pygame.draw.rect(screen, WHITE, [WIDTH / 2 + 160, HEIGHT / 2 + 320, 80, 50], 2)
                draw_text(screen, "HELP", 20, WIDTH / 2 + 200, HEIGHT / 2 + 335, WHITE)

                pygame.display.update()

                player = Player(150, 150, WIDTH // 2 - 75, HEIGHT // 2 - 80)
                player.draw()
                pygame.display.update()

                break
        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()


# draw the help page
def helpScreen():

    helpScreen = helpScreenPic
    helpScreen = pygame.transform.scale(helpScreen, (WIDTH, HEIGHT), screen)

    screen.blit(helpScreen, (0, 0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if distance(pos, (40, 40)) <= 40:
                startScreen = startScreenPic
                startScreen = pygame.transform.scale(
                    startScreen, (WIDTH, HEIGHT), screen)
                screen.blit(startScreen, (0, 0))
                pygame.draw.rect(
                    screen, WHITE, [WIDTH / 2 - 80, HEIGHT / 2 + 320, 160, 50], 2)
                draw_text(screen, "LEADERBOARD", 20,
                          WIDTH / 2, HEIGHT / 2 + 335, WHITE)

                pygame.draw.rect(screen, WHITE, [WIDTH / 2 + 160, HEIGHT / 2 + 320, 80, 50], 2)
                draw_text(screen, "HELP", 20, WIDTH / 2 + 200, HEIGHT / 2 + 335, WHITE)
                pygame.display.update()

                player = Player(150, 150, WIDTH // 2 - 75, HEIGHT // 2 - 80)
                player.draw()
                pygame.display.update()

                break
        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()


### create the character selection page ###
def drawCharacterSelection():
    global CHARACTER
    size = 20
    font = pygame.font.Font(font_name, size)
    text = font.render("You changed your avatar to %s!" %
                       CHARACTER, True, WHITE)
    screen.blit(text, (WIDTH / 2 - 200, HEIGHT / 8))
    pygame.display.update()


def characterScreen():
    global screen, CHARACTER

    characterScreen = characterScreenPic
    characterScreen = pygame.transform.scale(characterScreen, (WIDTH, HEIGHT), screen)
    screen.blit(characterScreen, (0, 0))

    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if distance(pos, (40, 40)) <= 40:
                startScreen = startScreenPic
                startScreen = pygame.transform.scale(
                    startScreen, (WIDTH, HEIGHT), screen)

                screen.blit(startScreen, (0, 0))
                pygame.draw.rect(
                    screen, WHITE, [WIDTH / 2 - 80, HEIGHT / 2 + 320, 160, 50], 2)
                draw_text(screen, "LEADERBOARD", 20,
                          WIDTH / 2, HEIGHT / 2 + 335, WHITE)

                pygame.draw.rect(screen, WHITE, [WIDTH / 2 + 160, HEIGHT / 2 + 320, 80, 50], 2)
                draw_text(screen, "HELP", 20, WIDTH / 2 + 200, HEIGHT / 2 + 335, WHITE)

                player = Player(150, 150, WIDTH // 2 - 75, HEIGHT // 2 - 80)
                player.draw()
                pygame.display.update()
                break

            elif distance(pos, (100, 370)) <= 100:
                CHARACTER = "robot"
                drawCharacterSelection()
            elif distance(pos, (300, 370)) <= 100:
                CHARACTER = "tiger"
                drawCharacterSelection()
            elif distance(pos, (500, 370)) <= 100:
                CHARACTER = "elephant"
                drawCharacterSelection()
            elif distance(pos, (100, 630)) <= 100:
                CHARACTER = "doggy"
                drawCharacterSelection()
            elif distance(pos, (300, 630)) <= 100:
                CHARACTER = "bird"
                drawCharacterSelection()
            elif distance(pos, (500, 630)) <= 100:
                CHARACTER = "oneeye"
                drawCharacterSelection()

        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()


### create the speed selection page ###
def drawRecommendedSpeed():
    size = 30
    font = pygame.font.Font(font_name, size)
    text = font.render("Tip: (3) is the best!", True, WHITE)
    screen.blit(text, (WIDTH / 2 - 150, HEIGHT - 100))
    pygame.display.update()


def drawYouAreCrazy(speed):
    size = 20
    font = pygame.font.Font(font_name, size)
    width = WIDTH / 2
    if speed <= 3:
        text = font.render("Good call!", True, WHITE)
        width = WIDTH / 2 - 50
    elif speed > 3 and speed <= 6:
        text = font.render("How Brave!", True, WHITE)
        width = WIDTH / 2 - 50
    elif speed > 6 and speed <= 9:
        text = font.render("Please go back!", True, WHITE)
        width = WIDTH / 2 - 70
    else:
        text = font.render("Ambulance please this man is crazy!", True, WHITE)
        width = WIDTH / 2 - 180
    screen.blit(text, (width, HEIGHT / 8 - 10))
    pygame.display.update()


def challengeScreen():
    global screen, SPEED

    challengeScreen = challengeScreenPic
    challengeScreen = pygame.transform.scale(challengeScreen, (WIDTH, HEIGHT), screen)
    screen.blit(challengeScreen, (0, 0))

    pygame.display.update()

    drawRecommendedSpeed()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if distance(pos, (40, 40)) <= 40:
                startScreen = startScreenPic
                startScreen = pygame.transform.scale(
                    startScreen, (WIDTH, HEIGHT), screen)

                screen.blit(startScreen, (0, 0))

                pygame.draw.rect(
                    screen, WHITE, [WIDTH / 2 - 80, HEIGHT / 2 + 320, 160, 50], 2)
                draw_text(screen, "LEADERBOARD", 20,
                          WIDTH / 2, HEIGHT / 2 + 335, WHITE)

                pygame.draw.rect(screen, WHITE, [WIDTH / 2 + 160, HEIGHT / 2 + 320, 80, 50], 2)
                draw_text(screen, "HELP", 20, WIDTH / 2 + 200, HEIGHT / 2 + 335, WHITE)

                pygame.display.update()

                player = Player(150, 150, WIDTH // 2 - 75, HEIGHT // 2 - 80)
                player.draw()
                break

            elif distance(pos, (175, 225)) <= 50:
                SPEED = 2
                drawYouAreCrazy(1)
            elif distance(pos, (300, 225)) <= 50:
                SPEED = 2.5
                drawYouAreCrazy(2)
            elif distance(pos, (425, 225)) <= 50:
                SPEED = 3
                drawYouAreCrazy(3)
            elif distance(pos, (175, 350)) <= 50:
                SPEED = 3.5
                drawYouAreCrazy(4)
            elif distance(pos, (300, 350)) <= 50:
                SPEED = 4
                drawYouAreCrazy(5)
            elif distance(pos, (425, 350)) <= 50:
                SPEED = 4
                drawYouAreCrazy(6)
            elif distance(pos, (175, 475)) <= 50:
                SPEED = 4
                drawYouAreCrazy(7)
            elif distance(pos, (300, 475)) <= 50:
                SPEED = 4
                drawYouAreCrazy(8)
            elif distance(pos, (425, 475)) <= 50:
                SPEED = 4
                drawYouAreCrazy(9)
            elif distance(pos, (175, 600)) <= 50:
                SPEED = 4
                drawYouAreCrazy(10)
            elif distance(pos, (300, 600)) <= 50:
                SPEED = 4
                drawYouAreCrazy(11)
            elif distance(pos, (425, 600)) <= 50:
                SPEED = 4
                drawYouAreCrazy(12)

        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()


#################################################
# Gameplay (elements)
#################################################

##############################
# Brick
##############################

class Brick(object):

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.w = BRICKW
        self.h = BRICKH
        self.speed = speed
        self.color1 = COLORS[random.randint(0, len(COLORS) - 1)]
        self.color2 = COLORS[random.randint(0, len(COLORS) - 1)]
        self.color3 = COLORS[random.randint(0, len(COLORS) - 1)]
        self.color4 = COLORS[random.randint(0, len(COLORS) - 1)]
        self.patterns = [0, 1, 2, 3, 4, 5]
        self.pattern = self.patterns[random.randint(0, len(self.patterns) - 1)]
        self.flip = flipACoin()

    def draw(self):
        shadowH = 10

        if self.pattern == 0:
            draw_rectangle(screen, self.x, self.y, self.w, self.h, self.color1)
            triangleH = self.h // 2
            draw_triangle(screen, self.x - 2 * triangleH, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_triangle(screen, self.x - triangleH, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_triangle(screen, self.x, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_triangle(screen, self.x + triangleH, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_star(screen, self.x - triangleH, self.y -
                      self.h / 5, self.h / 3, 5, self.color3)
            draw_star(screen, self.x, self.y - self.h /
                      5, self.h / 3, 5, self.color3)
            draw_star(screen, self.x + triangleH, self.y -
                      self.h / 5, self.h / 3, 5, self.color3)
            shadowpoints = [(self.x - self.w / 2, self.y - self.h / 2),
                            (self.x - self.w / 2 + self.w, self.y - self.h / 2),
                            (self.x + self.w / 2 - self.w /
                             8, self.y - self.h / 2 - shadowH),
                            (self.x - self.w / 2 + self.w / 8, self.y - self.h / 2 - shadowH)]
            pygame.draw.polygon(screen, self.color4, shadowpoints)

        elif self.pattern == 1:
            draw_rectangle(screen, self.x, self.y, self.w, self.h, self.color1)
            triangleH = self.h // 2
            draw_triangle(screen, self.x - 2 * triangleH, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_triangle(screen, self.x - triangleH, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_triangle(screen, self.x, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_triangle(screen, self.x + triangleH, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_circle(screen, int(self.x - 1.5 * triangleH),
                        self.y - 15, 5, self.color3)
            draw_circle(screen, int(self.x - 0.5 * triangleH),
                        self.y - 15, 5, self.color3)
            draw_circle(screen, int(self.x + 0.5 * triangleH),
                        self.y - 15, 5, self.color3)
            draw_circle(screen, int(self.x + 1.5 * triangleH),
                        self.y - 15, 5, self.color3)
            shadowpoints = [(self.x - self.w / 2, self.y - self.h / 2),
                            (self.x - self.w / 2 + self.w, self.y - self.h / 2),
                            (self.x + self.w / 2 - self.w /
                             8, self.y - self.h / 2 - shadowH),
                            (self.x - self.w / 2 + self.w / 8, self.y - self.h / 2 - shadowH)]
            pygame.draw.polygon(screen, self.color4, shadowpoints)

        elif self.pattern == 2:
            draw_rectangle(screen, self.x, self.y, self.w, self.h, self.color1)
            triangleH = self.h // 2
            draw_triangle2(screen, self.x - 2 * triangleH, self.y +
                           triangleH - 1, triangleH, self.color2)
            draw_triangle2(screen, self.x - triangleH, self.y +
                           triangleH - 1, triangleH, self.color2)
            draw_triangle2(screen, self.x, self.y +
                           triangleH - 1, triangleH, self.color2)
            draw_triangle2(screen, self.x + triangleH, self.y +
                           triangleH - 1, triangleH, self.color2)
            shadowpoints = [(self.x - self.w / 2, self.y - self.h / 2),
                            (self.x - self.w / 2 + self.w, self.y - self.h / 2),
                            (self.x + self.w / 2 - self.w /
                             8, self.y - self.h / 2 - shadowH),
                            (self.x - self.w / 2 + self.w / 8, self.y - self.h / 2 - shadowH)]
            pygame.draw.polygon(screen, self.color4, shadowpoints)

        elif self.pattern == 3:
            draw_rectangle(screen, self.x, self.y, self.w, self.h, self.color1)
            triangleH = self.h // 2
            draw_triangle(screen, self.x - 2 * triangleH, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_triangle(screen, self.x - triangleH, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_triangle(screen, self.x, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_triangle(screen, self.x + triangleH, self.y +
                          triangleH - 1, triangleH, self.color2)
            draw_circle(screen, int(self.x - 1.5 * triangleH),
                        self.y + 25, 5, self.color3)
            draw_circle(screen, int(self.x - 0.5 * triangleH),
                        self.y + 25, 5, self.color3)
            draw_circle(screen, int(self.x + 0.5 * triangleH),
                        self.y + 25, 5, self.color3)
            draw_circle(screen, int(self.x + 1.5 * triangleH),
                        self.y + 25, 5, self.color3)
            shadowpoints = [(self.x - self.w / 2, self.y - self.h / 2),
                            (self.x - self.w / 2 + self.w, self.y - self.h / 2),
                            (self.x + self.w / 2 - self.w /
                             8, self.y - self.h / 2 - shadowH),
                            (self.x - self.w / 2 + self.w / 8, self.y - self.h / 2 - shadowH)]
            pygame.draw.polygon(screen, self.color4, shadowpoints)

        elif self.pattern == 4:
            draw_rectangle(screen, self.x, self.y, self.w, self.h, self.color1)
            triangleH = self.h // 2
            if self.flip == "Heads":
                name = "112"
            else:
                name = "122"
            draw_text(screen, name, 50, self.x, self.y - 20, WHITE)
            shadowpoints = [(self.x - self.w / 2, self.y - self.h / 2),
                            (self.x - self.w / 2 + self.w, self.y - self.h / 2),
                            (self.x + self.w / 2 - self.w /
                             8, self.y - self.h / 2 - shadowH),
                            (self.x - self.w / 2 + self.w / 8, self.y - self.h / 2 - shadowH)]
            pygame.draw.polygon(screen, self.color4, shadowpoints)

        elif self.pattern == 5:
            draw_rectangle(screen, self.x, self.y, self.w, self.h, self.color1)
            triangleH = self.h // 2
            if self.flip == "Heads":
                name = "KAMYAR"
            else:
                name = "GOOGLE"
            draw_text(screen, name, 30, self.x, self.y - 10, WHITE)
            shadowpoints = [(self.x - self.w / 2, self.y - self.h / 2),
                            (self.x - self.w / 2 + self.w, self.y - self.h / 2),
                            (self.x + self.w / 2 - self.w /
                             8, self.y - self.h / 2 - shadowH),
                            (self.x - self.w / 2 + self.w / 8, self.y - self.h / 2 - shadowH)]
            pygame.draw.polygon(screen, self.color4, shadowpoints)

    # move horizontally
    def move(self):
        self.x += self.speed
        if self.x > WIDTH:
            self.speed = -self.speed
        if self.x < 1:
            self.speed = -self.speed

    def stop(self):
        self.speed = 0

    # brick falling animation
    def push(self):
        yspeed = 10
        self.y += yspeed


##############################
# Stack
##############################

# create the class for the stack
class Stack(object):

    def __init__(self):
        self.stack = []
        self.stackSize = 1
        for i in range(self.stackSize):
            newBrick = Brick(WIDTH, HEIGHT // 2 + 135, -4)
            self.stack.append(newBrick)
        self.speedlog = 0

    def draw(self):
        for i in range(self.stackSize):
            self.stack[i].draw()

    def move(self):
        for i in range(self.stackSize):
            self.stack[i].move()

    # avoid inefficiency
    def pop(self):
        self.stack.pop(0)
        self.stackSize -= 1

    def addNewBrick(self):
        global SCORE, SPEED

        # increasing difficulty over time
        if SCORE >= 50 or SPEED <= 2.5 or SPEED >= 6.0:
            SPEED += 0
        else:
            if SCORE % 3 == 0:
                SPEED += 0.4
            if SCORE % 5 == 0:
                SPEED -= 0.2

        y = self.stack[self.stackSize - 1].y
        # create randomly placed new bricks
        newBrickLeft = Brick(0, y - BRICKH, round(random.uniform(SPEED, SPEED + 1), 2))
        newBrickRight = Brick(WIDTH, y - BRICKH, round(random.uniform(SPEED, SPEED + 1), 2))

        # randomize direction the brick comes from
        self.stackSize += 1
        flip = flipACoin()
        if flip == "Heads":
            self.stack.append(newBrickRight)
        else:
            self.stack.append(newBrickLeft)

    # push the rest of the stack down one brick
    def pushToStack(self):
        global SCORE

        b = self.stack[self.stackSize - 2]
        b2 = self.stack[self.stackSize - 1]

        if b2.x <= b.x and not (b2.x + b2.w < b.x):
            self.speedlog = self.stack[self.stackSize - 1].speed
            self.stack[self.stackSize - 1].speed = 0
            SCORE += 1
            if STREAK > 0:
                SCORE += (STREAK - 1)

        elif b.x <= b2.x <= b.x + b.w:
            self.speedlog = self.stack[self.stackSize - 1].speed
            self.stack[self.stackSize - 1].speed = 0
            SCORE += 1
            if STREAK > 0:
                SCORE += (STREAK - 1)

    # animation of stack lowering
    def push(self):
        for i in range(self.stackSize):
            self.stack[i].push()


##############################
# Player
##############################

class Player(object):

    def __init__(self, imageWidth, imageHeight, x, y):
        self.imageWidth = imageWidth
        self.imageHeight = imageHeight
        self.angle = 0
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            'images/characters/%s.png' % CHARACTER).convert_alpha(), (self.imageWidth, self.imageHeight)), self.angle)
        self.imagerect = self.image.get_rect()
        self.x = x
        self.y = y

        self.jumping = False

        self.jumpOffset = 0

        # gravity jump effect
        # change values for different jumping heights
        self.velocity = list((i / 2) - 10.5 for i in range(0, 43))
        self.velocity_index = 0

        # "catch" the player
        self.platform_y = self.y

    def jump(self):
        # gravity jumping effect
        if self.jumping:
            self.y += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) - 1:
                self.velocity_index = len(self.velocity) - 1
            if self.y > self.platform_y:
                self.y = self.platform_y
                self.jumping = False
                self.velocity_index = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


##############################
# Background
##############################

class Background(object):
    # really don't need a class for this but oh well it's here

    def __init__(self):
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            'images/Background.png').convert_alpha(), (WIDTH, HEIGHT)), 0)

    def draw(self):
        screen.blit(self.image, (0, 0))


##############################
# Starting Ground
##############################

class StartingGround(object):
    # This is where the avatar stands

    def __init__(self):
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            'images/startingGround.png').convert_alpha(), (WIDTH, HEIGHT)), 0)
        self.x = 0
        self.y = 0

    def move(self):
        self.y += BRICKH

    def push(self):
        yspeed = 10
        self.y += yspeed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


#################################################
# In-game Screens
#################################################

##############################
# 2nd Chance screen
##############################

def secondChance():
    # Everybody gets a second chance! Be nice tho
    global screen, SCORE, SPEED, MODE

    loop = True

    reviveSound.play()
    size = 50
    font = pygame.font.Font(font_name, size)
    text = font.render("Second Chance?", True, WHITE)

    textRect = text.get_rect()
    textRect.center = (WIDTH / 2, HEIGHT / 2 - 200)

    draw_text(screen, "Tip: Press [a] or [t] for AI to jump for you!",
              20, WIDTH / 2, HEIGHT / 2 - 160, WHITE)

    draw_text(screen, "Tip: Press [h] for HELL MODE!!",
              20, WIDTH / 2, HEIGHT / 2 - 125, WHITE)

    draw_text(screen, "Note: [a] is auto-jump & [t] is training mode",
              20, WIDTH / 2, HEIGHT / 2 + 125, WHITE)

    draw_text(screen, "Auto-jump tries to survive",
              20, WIDTH / 2, HEIGHT / 2 + 160, WHITE)

    draw_text(screen, "Training mode learns to land perfectly",
              20, WIDTH / 2, HEIGHT / 2 + 190, WHITE)

    screen.blit(text, textRect)

    heartPic = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        'images/heart.png').convert_alpha(), (200, 200)), 0)

    screen.blit(heartPic, (WIDTH / 2 - 100, HEIGHT / 2 - 100))

    skipPic = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        'images/skip.png').convert_alpha(), (250, 80)), 0)

    screen.blit(skipPic, (WIDTH / 2 - 125, HEIGHT / 2 + 250))

    while loop:
        ev = pygame.event.poll()
        if ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if distance(pos, (300, 400)) <= 150:
                break
            elif distance(pos, (300, 700)) <= 100:
                SCORE = 0
                SPEED = 3
                MODE = "start"
                main()
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                pass
        elif ev.type == pygame.QUIT:
            close()

        pygame.mixer.music.pause()

        pygame.display.update()
        clock.tick()

##############################
# Game Over Screen
##############################

# prompt user to input his/her name for rankings using tkinter
# code modified from a similar question on StackOverflow
# https://stackoverflow.com/questions/20865010/how-do-i-create-an-input-box-with-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
def getUserName():
    master = Tk()
    e = Entry(master)
    e.pack()

    e.focus_set()

    def callback():
        global NAME
        NAME = e.get()
        # print(e.get())

    b = Button(master, text="OK", width=10, command=callback)
    b.pack(side=LEFT)
    c = Button(master, text="QUIT", width=10, command=master.destroy)
    c.pack(side=RIGHT)

    mainloop()


def gameOver():
    # game over :(
    global SCORE, SPEED, MODE, NAME

    loop = True

    size = 60
    #font = pygame.font.SysFont("Agency FB", 60)
    font = pygame.font.Font(font_name, size)
    text = font.render("Game Over!", True, WHITE)

    textRect = text.get_rect()
    textRect.center = (WIDTH / 2, HEIGHT / 2 - 80)

    quitPic = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        'images/quit.png').convert_alpha(), (250, 80)), 0)

    draw_text(screen, "What's your name?", 30, WIDTH / 2, HEIGHT / 2, WHITE)

    pygame.display.update()

    getUserName()

    draw_rectangle(screen, WIDTH / 2, HEIGHT / 2 +
                   100, 500, 500, color=GOOGLEBLUE)

    draw_text(screen, "Congratulations,", 25,
              WIDTH / 2, HEIGHT / 2 + 60, WHITE)

    draw_text(screen, "___%s___" %
              NAME, 35, WIDTH / 2, HEIGHT / 2 + 100, WHITE)

    pygame.display.update()

    draw_text(screen, "Your score has been saved to our database!",
              20, WIDTH / 2, HEIGHT / 2 + 160, WHITE)

    draw_text(screen, "Click anywhere to restart except [QUIT]",
              20, WIDTH / 2, HEIGHT / 2 + 200, WHITE)

    screen.blit(quitPic, (WIDTH / 2 - 125, HEIGHT / 2 + 250))

    pygame.display.update()

    # write user information to file
    writeToFile("leaderboard.txt", '%d,%s' % (SCORE, NAME) + '\n')

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    SCORE = 0
                    SPEED = 3
                    MODE = "start"
                    SECONDCHANCE = False
                    main()
                if event.key == pygame.K_SPACE:
                    SCORE = 0
                    SPEED = 3
                    MODE = "start"
                    SECONDCHANCE = False
                    main()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if distance(pos, (300, 700)) <= 100:
                    close()
                else:
                    SCORE = 0
                    SPEED = 3
                    MODE = "start"
                    SECONDCHANCE = False
                    main()

        screen.blit(text, textRect)

        pygame.mixer.music.stop()

        pygame.display.update()
        clock.tick()

#################################################
# Gameplay (controls)
#################################################

def drawScore():
    # draw the score
    size = 70
    font = pygame.font.Font(font_name, size)
    text = font.render(str(SCORE), True, WHITE)
    if SCORE < 10:
        screen.blit(text, (WIDTH / 2 - size / 6, 50))
    elif SCORE >= 10 and SCORE < 100:
        screen.blit(text, (WIDTH / 2 - size / 4, 50))
    else:
        screen.blit(text, (WIDTH / 2 - size / 2, 50))

def drawStreak():
    # draw streaks
    if STREAK == 1:
        size = 40
    elif STREAK == 2:
        size = 45
    elif STREAK == 3:
        size = 52
    elif STREAK == 4:
        size = 74
    elif STREAK == 5:
        size = 90
    else:
        size = 100
    font = pygame.font.Font(font_name, size)
    text = font.render("+ %d" % STREAK, True, WHITE)
    if STREAK > 0 and STREAK < 10:
        screen.blit(text, (WIDTH / 2 + BRICKW - 20, HEIGHT - 3 * BRICKH))
    elif STREAK >= 10:
        screen.blit(text, (WIDTH / 2 + BRICKW - 50, HEIGHT - 3 * BRICKH))


def drawAutoJump():
    size = 20
    font = pygame.font.Font(font_name, size)
    text = font.render("Auto-Jump: On", True, WHITE)
    screen.blit(text, (50, 50))


def drawTraining():
    # draw the score
    size = 20
    font = pygame.font.Font(font_name, size)
    text = font.render("Training Mode: On", True, WHITE)
    screen.blit(text, (50, 50))


##############################
# MAIN
##############################

class Main(object):
    # this is where the magic happens

    def init(self):
        self.timer = 0
        self.player = Player(100, 100, WIDTH // 2 - 50, HEIGHT // 2 + 70)
        self.background = Background()
        self.startingGround = StartingGround()
        self.stack = Stack()
        self.pushing = False
        self.isPaused = False
        self.streakCount = 0
        self.ai = False

        self.training = False
        self.dis = 45
        self.spd = 0

    def mousePressed(self, x, y):
        if self.player.jumping == False:
            self.player.jumping = True
            flip = flipACoin()
            if flip == "Heads":
                jumpingSound1.play()
            else:
                jumpingSound2.play()

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        global STREAK, SPEED

        if keyCode == pygame.K_SPACE:
            if self.player.jumping == False:
                self.player.jumping = True
                flip = flipACoin()
                if flip == "Heads":
                    jumpingSound1.play()
                else:
                    jumpingSound2.play()

        # turn on the AI
        if keyCode == pygame.K_a:
            self.ai = not self.ai

        if keyCode == pygame.K_p:
            self.isPaused = not self.isPaused
            if self.isPaused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

        # turn on HELL MODE!!!
        if keyCode == pygame.K_h:
            SPEED = 7.5

        if keyCode == pygame.K_t:
            self.training = not self.training

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        # magic happens here
        global STREAK, SECONDCHANCE

        if not self.isPaused:
            # smooth animation!
            if self.pushing:
                self.stack.push()
                self.startingGround.push()

            self.timer += 1

            self.player.jump()

            self.stack.move()

            movingBrick = self.stack.stack[self.stack.stackSize - 1]
            playerL, playerR = self.player.x, self.player.x + self.player.imageWidth
            playerT, playerB = self.player.y, self.player.y + self.player.imageHeight
            brickL, brickR = movingBrick.x - BRICKW / 2, movingBrick.x + BRICKW / 2
            brickT, brickB = movingBrick.y - BRICKH / 2, movingBrick.y + BRICKH / 2
            stationaryBrick = self.stack.stack[self.stack.stackSize - 2]
            stationaryBrickL, stationaryBrickR = stationaryBrick.x - BRICKW / 2, stationaryBrick.x + BRICKW / 2

            # uncomment to pause the moving brick from going over the stack

            # if movingBrick.speed < 0 and brickL < stationaryBrickL:
            #     movingBrick.stop()
            #
            # if movingBrick.speed > 0 and brickR >= stationaryBrickR:
            #     movingBrick.stop()

            # draw the streaks! make 'diff' bigger for easier streaks
            diff = 5
            if self.stack.stackSize > 1 and self.player.velocity[self.player.velocity_index] == 7.0 and abs(brickL - stationaryBrickL) <= diff:
                self.streakCount = self.stack.stackSize
                STREAK += 1
                streakSound.play()
            elif self.player.velocity[self.player.velocity_index] == 7.0 and abs(brickL - stationaryBrickL) > diff:
                STREAK = 0

            offset = 95
            if brickB >= HEIGHT // 2 + BRICKH + offset:
                self.pushing = False

            # 4 ways to die in this game :(
            # basic collision stuff here
            if self.player.jumping and self.player.velocity[self.player.velocity_index] < 0:
                if movingBrick.speed < 0 and brickL <= (playerR - 30) and playerB >= brickT:
                    self.isPaused = True
                    gameOverSound.play()
                    if SECONDCHANCE == False:
                        secondChance()
                        SECONDCHANCE = True
                        self.init()
                        pygame.mixer.music.unpause()
                    else:
                        gameOver()
                elif movingBrick.speed > 0 and brickR >= (playerL + 30) and playerB >= brickT:
                    self.isPaused = True
                    gameOverSound.play()
                    if SECONDCHANCE == False:
                        secondChance()
                        SECONDCHANCE = True
                        self.init()
                        pygame.mixer.music.unpause()
                    else:
                        gameOver()
            elif not self.player.jumping:
                if movingBrick.speed < 0 and brickL <= playerR and playerB >= brickT:
                    gameOverSound.play()
                    if SECONDCHANCE == False:
                        secondChance()
                        SECONDCHANCE = True
                        self.init()
                        pygame.mixer.music.unpause()
                    else:
                        gameOver()
                elif movingBrick.speed > 0 and brickR >= playerL and playerB >= brickT:
                    gameOverSound.play()
                    if SECONDCHANCE == False:
                        secondChance()
                        SECONDCHANCE = True
                        self.init()
                        pygame.mixer.music.unpause()
                    else:
                        gameOver()

            # Survive!!! Score!!! Be the best!!!
            # complicated collision stuff here
            elif self.player.velocity[self.player.velocity_index] >= 0 and abs(playerL - brickL) <= self.player.imageWidth \
                    and abs(playerR - brickR) <= self.player.imageWidth and abs(playerB - brickT) <= 3:
                self.stack.pushToStack()
                self.pushing = True
                self.stack.addNewBrick()

                # for the late game to not be laggy
                if self.stack.stackSize >= 10:
                    self.stack.pop()

            # Make the avatar jump by him/herself based on the speed of and distance from the incoming brick
            # Can survive any speed up to 8.5, but will not try to jump perfectly
            if self.ai:
                if abs(movingBrick.speed) > 3.5 and abs(movingBrick.speed) < 6.0:
                    if (movingBrick.speed > 0 and playerL - brickR <= 55):
                        if self.player.jumping == False:
                            self.player.jumping = True
                            flip = flipACoin()
                            if flip == "Heads":
                                jumpingSound1.play()
                            else:
                                jumpingSound2.play()
                    elif (movingBrick.speed < 0 and brickL - playerR <= 55):
                        if self.player.jumping == False:
                            self.player.jumping = True
                            flip = flipACoin()
                            if flip == "Heads":
                                jumpingSound1.play()
                            else:
                                jumpingSound2.play()
                elif abs(movingBrick.speed) <= 3.5:
                    if (movingBrick.speed > 0 and playerL - brickR <= 30):
                        if self.player.jumping == False:
                            self.player.jumping = True
                            flip = flipACoin()
                            if flip == "Heads":
                                jumpingSound1.play()
                            else:
                                jumpingSound2.play()
                    elif (movingBrick.speed < 0 and brickL - playerR <= 30):
                        if self.player.jumping == False:
                            self.player.jumping = True
                            flip = flipACoin()
                            if flip == "Heads":
                                jumpingSound1.play()
                            else:
                                jumpingSound2.play()
                elif abs(movingBrick.speed) >= 6.0 and abs(movingBrick.speed) < 7.0:
                    if (movingBrick.speed > 0 and playerL - brickR <= 120):
                        if self.player.jumping == False:
                            self.player.jumping = True
                            flip = flipACoin()
                            if flip == "Heads":
                                jumpingSound1.play()
                            else:
                                jumpingSound2.play()
                    elif (movingBrick.speed < 0 and brickL - playerR <= 120):
                        if self.player.jumping == False:
                            self.player.jumping = True
                            flip = flipACoin()
                            if flip == "Heads":
                                jumpingSound1.play()
                            else:
                                jumpingSound2.play()
                else:  # only 10.0 speed!!!
                    if (movingBrick.speed > 0 and playerL - brickR <= 600):
                        if self.player.jumping == False:
                            self.player.jumping = True
                            flip = flipACoin()
                            if flip == "Heads":
                                jumpingSound1.play()
                            else:
                                jumpingSound2.play()
                    elif (movingBrick.speed < 0 and brickL - playerR <= 600):
                        if self.player.jumping == False:
                            self.player.jumping = True
                            flip = flipACoin()
                            if flip == "Heads":
                                jumpingSound1.play()
                            else:
                                jumpingSound2.play()

            # Adjusts its jumping distance according to offset from the center of the block in previous run to help it jump close to the center
            # Cannot survive speed over 7.0 but will jump towards the middle of the brick
            # Machine learning? Robots taking over!
            if self.training:
                # print(self.dis)
                # print(movingBrick.speed - self.stack.speedlog)
                if self.player.velocity[self.player.velocity_index] == 7.0 and self.player.x + self.player.imageWidth*0.5 < movingBrick.x:
                        self.dis -= (movingBrick.speed - self.stack.speedlog)
                elif self.player.velocity[self.player.velocity_index] == 7.0 and self.player.x + self.player.imageWidth*0.5 > movingBrick.x:
                        self.dis += (movingBrick.speed - self.stack.speedlog)

                if (movingBrick.speed > 0 and playerL - brickR <= self.dis):
                    if self.player.jumping == False:
                        self.player.jumping = True
                        flip = flipACoin()
                        if flip == "Heads":
                            jumpingSound1.play()
                        else:
                            jumpingSound2.play()
                elif (movingBrick.speed < 0 and brickL - playerR <= self.dis):
                    if self.player.jumping == False:
                        self.player.jumping = True
                        flip = flipACoin()
                        if flip == "Heads":
                            jumpingSound1.play()
                        else:
                            jumpingSound2.play()


    # draw everything!
    def redrawAll(self, screen):
        global MODE
        if MODE == "start":
            main_menu()
            pygame.time.wait(2000)
            MODE = "game"
            self.player = Player(100, 100, WIDTH // 2 - 50, HEIGHT // 2 + 70)
        elif MODE == "game":
            self.background.draw()
            drawScore()
            if self.ai:
                drawAutoJump()
            elif self.training:
                drawTraining()
            self.startingGround.draw()
            self.stack.draw()
            self.player.draw()
            drawStreak()

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

### run function and all that boring stuff (jk this is the best!) ###

    def __init__(self, width=WIDTH, height=HEIGHT, fps=FPS, title=TITLE):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)

    def run(self):

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = Main()
    game.run()


if __name__ == '__main__':
    main()