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

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
        screen.fill(constants.BACKCOLOUR)
        screen.blit(playArea_surf, playArea_rect)
        
        screen.blit(nextShape_surf, nextShape_rect)
        nextShape = classes.Shape(nextShape_rect, player_group.nextShape)
        nextShape.draw(screen)

        screen.blit(holded_surf, holded_rect)
        if player_group.holded != None:
            holded = classes.Shape(holded_rect, player_group.holded)
            holded.draw(screen)

        player_group.draw(screen)
        if player_group.update():
            gameOver = True

        ground_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)