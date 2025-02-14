import pygame
from sys import exit
from time import time, ctime

import constants
import classes

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption(constants.CAPTION)
clock = pygame.time.Clock()

# game over
gameOver = False
gameOver_surf = pygame.image.load("graphics/gameOver.png").convert()
gameOver_rect = screen.get_rect()

# pause
pause = True
pause_surf = pygame.image.load("graphics/pause.png").convert()
pause_rect = screen.get_rect()

# play area
playArea_surf = pygame.image.load("graphics/grid.png").convert()
playArea_rect = playArea_surf.get_rect(center = screen.get_rect().center)

# ground
ground_group = classes.Ground(playArea_rect)

# player
player_group = classes.Player(playArea_rect, ground_group)

# font
robotoMono = pygame.font.Font("fonts/RobotoMono.ttf", 30)

# next shape
nextShape_surf = pygame.surface.Surface((180, 180)).convert()
nextShape_rect = nextShape_surf.get_rect(topleft = (playArea_rect.right + 30, playArea_rect.top + 51))
nextShapeFont_surf = robotoMono.render("Next:", True, "White")
nextShapeFont_rect = nextShapeFont_surf.get_rect(centerx=nextShape_rect.centerx, top=nextShape_rect.top - 40)

# holded
holded_surf = pygame.surface.Surface((180, 180)).convert()
holded_rect = holded_surf.get_rect(topright = (playArea_rect.left - 30, playArea_rect.top + 51))
holdedFont_surf = robotoMono.render("Holded:", True, "White")
holdedFont_rect = holdedFont_surf.get_rect(centerx=holded_rect.centerx, top=holded_rect.top - 40)

# score
score_surf = robotoMono.render("Score:", True, "White")
score_rect = score_surf.get_rect(topright = (playArea_rect.left - 50, playArea_rect.bottom - 321))

# level
level_surf = robotoMono.render("Level:", True, "White")
level_rect = level_surf.get_rect(topright = (playArea_rect.left - 50, playArea_rect.bottom - 231))

# lines
lines_surf = robotoMono.render("Lines:", True, "White")
lines_rect = lines_surf.get_rect(topright = (playArea_rect.left - 50, playArea_rect.bottom - 141))

def updateScores(player: classes.Player, ground: classes.Ground):
    score_surf = robotoMono.render(f"{player.score}", True, "White")
    score_rect = score_surf.get_rect(topright = (playArea_rect.left - 50, playArea_rect.bottom - 281))

    level_surf = robotoMono.render(f"{player.level}", True, "White")
    level_rect = level_surf.get_rect(topright = (playArea_rect.left - 50, playArea_rect.bottom - 191))

    lines_surf = robotoMono.render(f"{ground.lines}", True, "White")
    lines_rect = lines_surf.get_rect(topright = (playArea_rect.left - 50, playArea_rect.bottom - 101))

    return [[score_surf, score_rect], [level_surf, level_rect], [lines_surf, lines_rect]]

def loadHighscore(filename: str):
    highscores = {}

    try:
        with open(filename, 'r') as file:
            for line in file:
                score = line.split(" on ")

                if len(score) != 2:
                    continue

                highscores[score[1]] = int(score[0])
    except FileNotFoundError:
        pass
 
    return highscores 

def saveHighscore(filename: str, score: int):
    highscores = loadHighscore(filename)
    highscores[f"{ctime()}"] = score
    highscores_sorted = dict(sorted(list(highscores.items()), key=lambda item: int(item[1]), reverse=True))

    with open(filename, 'w') as file:
        for idx, (key, value) in enumerate(highscores_sorted.items()):
            if idx == 5:
                break
            
            file.write(f"{value} on {key}\n")

def displayHighscore(filename: str, screen: pygame.Surface):
    highscore = loadHighscore(filename)

    surf = robotoMono.render("Highscores:", True, "White")
    rect = surf.get_rect(center = (screen.get_rect().centerx, screen.get_rect().top + 400))
    screen.blit(surf, rect)

    for idx, (key, value) in enumerate(highscore.items()):
        surf = robotoMono.render(f"{value} on {key}", True, "White")
        rect = surf.get_rect(center = (screen.get_rect().centerx, screen.get_rect().top + (idx * 50 + 400)))
        screen.blit(surf, rect)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            saveHighscore(constants.HIGHSCORES_FILENAME, player_group.score)
            pygame.quit()
            exit()   

        if gameOver == False and event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pause = True if pause == False else False
        
        if gameOver == False and player_group.updateOnEvent(event):
            gameOver = True 
            saveHighscore(constants.HIGHSCORES_FILENAME, player_group.score)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            pause = False
            gameOver = False

            for sprite in ground_group:
                sprite.kill()

            player_group.score = 0
            player_group.level = 1
            ground_group.lines = 0
    
    if pause:
        screen.blit(pause_surf, pause_rect)

        player_group.lastFallTime = time()
    elif gameOver:
        screen.blit(gameOver_surf, gameOver_rect)

        displayHighscore(constants.HIGHSCORES_FILENAME, screen)

        player_group.lastFallTime = time()
    else:
        scores = updateScores(player_group, ground_group)

        screen.fill(constants.BACKCOLOUR)
        screen.blit(playArea_surf, playArea_rect)

        screen.blit(score_surf, score_rect)
        screen.blit(scores[0][0], scores[0][1])

        screen.blit(level_surf, level_rect)
        screen.blit(scores[1][0], scores[1][1])

        screen.blit(lines_surf, lines_rect)
        screen.blit(scores[2][0], scores[2][1])

        screen.blit(nextShapeFont_surf, nextShapeFont_rect)        
        screen.blit(nextShape_surf, nextShape_rect)
        nextShape = classes.Shape((nextShape_rect.left + 30, nextShape_rect.top + 50), size=constants.CRATE_LEN, shape=player_group.nextShape)
        nextShape.draw(screen)

        screen.blit(holdedFont_surf, holdedFont_rect)
        screen.blit(holded_surf, holded_rect)
        if player_group.holded != None:
            holded = classes.Shape((holded_rect.left + 30, holded_rect.top + 50), size=constants.CRATE_LEN, shape=player_group.holded)
            holded.draw(screen)

        player_group.draw(screen)
        if player_group.update():
            gameOver = True
            saveHighscore(constants.HIGHSCORES_FILENAME, player_group.score)

        ground_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)