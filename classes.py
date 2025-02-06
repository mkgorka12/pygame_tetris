import pygame
import constants
from random import choice
from time import time

class Player(pygame.sprite.Sprite):
    def __init__(self, playArea: pygame.rect.Rect, ground_group: pygame.sprite.Group):
        super().__init__()
        
        self.ground_group = ground_group

        self.level = 1
        self.lastFallTime = time()
        
        self.holded = 'N'
        self.can_hold = True
        self.holded_image = pygame.surface.Surface((1, 1))
        self.holded_rect = self.holded_image.get_rect(center = constants.HOLD_COORDINATES)
        
        self.playArea = playArea
    
        self.shape = choice(constants.SHAPES)
        self.nextShape = choice([i for i in constants.SHAPES if i != self.shape])
        self.nextShape_image = pygame.image.load(f"graphics/{self.nextShape}.png").convert_alpha()
        self.nextShape_rect = self.nextShape_image.get_rect(center = constants.NEXTSHAPE_COORDINATES)

        self.image = pygame.image.load(f"graphics/{self.shape}.png").convert_alpha()
        self.rect = self.image.get_rect(topright = (self.playArea.centerx, self.playArea.top))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN] and self.rect.bottom + constants.CRATE_LEN < self.playArea.bottom:
            self.rect.y += constants.CRATE_LEN

        self.mask = pygame.mask.from_surface(self.image)

    def fall(self):
        if time() - self.lastFallTime > 1.5 - (self.level * 0.1):
            if self.rect.bottom + constants.CRATE_LEN < self.playArea.bottom:
                self.rect.y += constants.CRATE_LEN
                self.mask = pygame.mask.from_surface(self.image)

            self.lastFallTime = time()

    def spawnNew(self, shape: str, calledByHold: bool):        
        self.shape = shape
        
        if not calledByHold:
            newGround = Ground(self)
            self.ground_group.add(newGround)
            self.can_hold = True

            self.nextShape = choice([i for i in constants.SHAPES if i != self.shape])
            self.nextShape_image = pygame.image.load(f"graphics/{self.nextShape}.png").convert_alpha()
            self.nextShape_rect = self.nextShape_image.get_rect(center = constants.NEXTSHAPE_COORDINATES)
        elif self.holded not in constants.SHAPES:
            self.nextShape = choice([i for i in constants.SHAPES if i != self.shape])
            self.nextShape_image = pygame.image.load(f"graphics/{self.nextShape}.png").convert_alpha()
            self.nextShape_rect = self.nextShape_image.get_rect(center = constants.NEXTSHAPE_COORDINATES)

        self.image = pygame.image.load(f"graphics/{self.shape}.png").convert_alpha()
        self.rect = self.image.get_rect(topright = (self.playArea.centerx, self.playArea.top))

    def freeze(self):
        self.rect.y += constants.CRATE_LEN
        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.bottom >= self.playArea.bottom:
            self.rect.y -= constants.CRATE_LEN
            self.mask = pygame.mask.from_surface(self.image)
            self.spawnNew(self.nextShape, False)
            return True

        for sprite in self.ground_group:
            if pygame.sprite.collide_mask(self, sprite):
                self.rect.y -= constants.CRATE_LEN
                self.mask = pygame.mask.from_surface(self.image)
                self.spawnNew(self.nextShape, False)
                return True

        self.rect.y -= constants.CRATE_LEN
        self.mask = pygame.mask.from_surface(self.image)

        return False

    def updateOnEvent(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.rect.left - constants.CRATE_LEN > self.playArea.left:
                self.rect.x -= constants.CRATE_LEN
            elif event.key == pygame.K_RIGHT and self.rect.right + constants.CRATE_LEN < self.playArea.right:
                self.rect.x += constants.CRATE_LEN
            elif event.key == pygame.K_c and self.can_hold: # HOLD
                self.can_hold = False

                temp = self.shape
                
                if self.holded in constants.SHAPES:
                    self.spawnNew(self.holded, True)
                else:
                    self.spawnNew(self.nextShape, True)

                self.holded = temp

                self.holded_image = pygame.image.load(f"graphics/{self.holded}.png").convert_alpha()
                self.holded_rect = self.holded_image.get_rect(center = constants.HOLD_COORDINATES)
            elif event.key == pygame.K_SPACE: # DROP
                while self.freeze() is False:
                    self.rect.bottom += constants.CRATE_LEN
                    self.mask = pygame.mask.from_surface(self.image)             
            elif event.key == pygame.K_UP: # ROTATE COUNTER CLOCKWISE
                self.image = pygame.transform.rotate(self.image, -90).convert_alpha()
                self.rect = self.image.get_rect(topleft = (self.rect.x, self.rect.y))

                if self.rect.right > self.playArea.right:
                    self.rect = self.image.get_rect(topright = (self.playArea.right - 1, self.rect.y))
            elif event.key == pygame.K_z: # ROTATE CLOCKWISE
                self.image = pygame.transform.rotate(self.image, 90).convert_alpha()
                self.rect = self.image.get_rect(topright = (self.rect.right, self.rect.y))

                if self.rect.left < self.playArea.left:
                    self.rect = self.image.get_rect(topleft = (self.playArea.left + 1, self.rect.y))

            self.mask = pygame.mask.from_surface(self.image)
            self.freeze()

    def update(self):
        self.freeze()
        self.move()
        self.fall()

class Ground(pygame.sprite.Sprite):
    def __init__(self, player: Player):
        super().__init__()
        self.image = player.image
        self.rect = player.rect
        self.mask = player.mask