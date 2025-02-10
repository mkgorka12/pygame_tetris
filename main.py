import pygame
from sys import exit

import constants
import classes

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption(constants.CAPTION)
clock = pygame.time.Clock()

# play area
playArea_surf = pygame.image.load("graphics/grid.png").convert()
playArea_rect = playArea_surf.get_rect(center = screen.get_rect().center)

# ground
ground_group = classes.Ground(playArea_rect)

# player
player_group = classes.Player(playArea_rect, ground_group, "T")

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()   

        player_group.updateOnEvent(event)   
    
    screen.fill(constants.BACKCOLOUR)
    screen.blit(playArea_surf, playArea_rect)
    
    player_group.draw(screen)
    player_group.update()

    ground_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)