import pygame
from sys import exit

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

# next shape
nextShape_surf = pygame.surface.Surface((160, 160)).convert()
nextShape_rect = nextShape_surf.get_rect(topleft = (playArea_rect.right + 30, playArea_rect.top + 1))

# holded
holded_surf = pygame.surface.Surface((160, 160)).convert()
holded_rect = holded_surf.get_rect(topright = (playArea_rect.left - 30, playArea_rect.top + 1))

# font
robotoMono = pygame.font.Font("fonts/RobotoMono.ttf", 30)

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

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()   

        if gameOver is False and event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pause = True if pause == False else False
        
        if player_group.updateOnEvent(event):
            gameOver = True  
    
    if pause:
        screen.blit(pause_surf, pause_rect)
    elif gameOver:
        screen.blit(gameOver_surf, gameOver_rect)
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
        
        screen.blit(nextShape_surf, nextShape_rect)
        nextShape = classes.Shape(nextShape_rect, size=20, shape=player_group.nextShape)
        nextShape.draw(screen)

        screen.blit(holded_surf, holded_rect)
        if player_group.holded != None:
            holded = classes.Shape(holded_rect, size=20, shape=player_group.holded)
            holded.draw(screen)

        player_group.draw(screen)
        if player_group.update():
            gameOver = True

        ground_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)