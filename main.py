import pygame
import constants
from sys import exit
import classes

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("mkgorka's Tetris")
clock = pygame.time.Clock()
pause = True

# play area
playArea_surf = pygame.image.load("graphics/grid.png").convert()
playArea_rect = playArea_surf.get_rect(topleft = (49, 49))

# fonts
SCORES_FONT = pygame.font.Font("fonts/RobotoMono.ttf", 35)
HOLD_N_NEXT_FONT = pygame.font.Font("fonts/RobotoMono.ttf", 20)

# next shape
nextShape_surf = pygame.surface.Surface((200, 200))
nextShape_rect = nextShape_surf.get_rect(center = constants.NEXTSHAPE_COORDINATES)
nextShapeFont_surf = HOLD_N_NEXT_FONT.render("Next shape:", True, "White")
nextShapeFont_rect = nextShapeFont_surf.get_rect(center = (600, 60))

# hold
hold_surf = pygame.surface.Surface((200, 200))
hold_rect = hold_surf.get_rect(center = constants.HOLD_COORDINATES)
holdFont_surf = HOLD_N_NEXT_FONT.render("Hold:", True, "White")
holdFont_rect = holdFont_surf.get_rect(center = (600, 320))

# score
score_surf = SCORES_FONT.render("Score: 0", True, "White")
score_rect = score_surf.get_rect(center = (600, 600))

# level
level_surf = SCORES_FONT.render("Level: 0", True, "White")
level_rect = level_surf.get_rect(center = (600, 650))

# lines
lines_surf = SCORES_FONT.render("Lines: 0", True, "White")
lines_rect = lines_surf.get_rect(center = (600, 700))

# pause
author_surf = SCORES_FONT.render("Tetris by mkgorka", True, "White")
author_rect = author_surf.get_rect(center = (screen.get_rect().centerx, screen.get_rect().centery - 20))

continue_surf = SCORES_FONT.render("Press \'P\' to continue", True, "White")
continue_rect = continue_surf.get_rect(center = (screen.get_rect().centerx, screen.get_rect().centery + 20))

# player
ground_group = pygame.sprite.Group()
player = classes.Player(playArea_rect, ground_group)
ground = classes.Ground(player)

player_group = pygame.sprite.GroupSingle()
player_group.add(player)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pause = False
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if pause:
                    pause = False
                else:
                    pause = True

                break

            player.updateOnEvent(event)
    
    if pause:
        screen.fill("Black")
        
        screen.blit(continue_surf, continue_rect)
        screen.blit(author_surf, author_rect)
    else:
        screen.fill(constants.BACKCOLOUR)

        screen.blit(playArea_surf, playArea_rect)
        
        screen.blit(nextShape_surf, nextShape_rect)
        screen.blit(nextShapeFont_surf, nextShapeFont_rect)
        screen.blit(player.nextShape_image, player.nextShape_rect)

        screen.blit(hold_surf, hold_rect)
        screen.blit(holdFont_surf, holdFont_rect)
        screen.blit(player.holded_image, player.holded_rect)

        screen.blit(score_surf, score_rect)
        screen.blit(level_surf, level_rect)
        screen.blit(lines_surf, lines_rect)

        player_group.draw(screen)
        player_group.update()

        ground_group.draw(screen)
        ground_group.update()

    pygame.display.flip()
    clock.tick(60)