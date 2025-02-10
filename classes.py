import pygame
import constants
from random import choice
from time import time
import math

class Block(pygame.sprite.Sprite):
    def __init__(self, playArea: pygame.Rect, coords: tuple[int, int], color: str):
        super().__init__()
        
        self.image = pygame.surface.Surface((constants.CRATE_LEN, constants.CRATE_LEN))
        self.image.fill(color=color)
        
        coords = (playArea.left + 1 + (coords[0] * constants.CRATE_LEN), playArea.top + 1 + (coords[1] * constants.CRATE_LEN))
        self.rect = self.image.get_rect(topleft = coords)

class Ground(pygame.sprite.Group):
    def __init__(self, playArea: pygame.Rect):
        super().__init__()
        self.playArea = playArea

    def update(self):
        colisionBlock = Block(self.playArea, (0, 0), "Black")
        
        for i in range(constants.ROWS):
            colisionBlock.rect.x = self.playArea.left + 1
            toClear = True

            for j in range(constants.COLUMNS):
                if pygame.sprite.spritecollideany(colisionBlock, self) == None:
                    toClear = False
                    break

                colisionBlock.rect.x += constants.CRATE_LEN
            
            colisionBlock.rect.y += constants.CRATE_LEN

            if toClear:
                for block in self:
                    if block.rect.bottom == self.playArea.top + 1 + ((i + 1) * constants.CRATE_LEN):
                        self.remove(block)

                for block in self:
                    if block.rect.bottom <= self.playArea.top + 1 + (i * constants.CRATE_LEN):
                        block.rect.y += constants.CRATE_LEN

class Player(pygame.sprite.Group):
    def __init__(self, playArea: pygame.Rect, ground_group: pygame.sprite.Group, shape: str):
        super().__init__()
        
        for i in range(4):
            self.add(Block(playArea, constants.SHAPES_COORDS[shape][i], constants.SHAPES_COLORS[shape]))

        self.playArea = playArea
        self.shape = shape
        self.ground_group = ground_group
        self.lastFallTime = time()
        self.level = 1

    def spawn(self):
        for block in self:
            self.remove(block)
            self.ground_group.add(block)

        self.shape = choice([shape for shape in constants.SHAPES_COLORS.keys() if shape is not self.shape])

        for i in range(4):    
            self.add(Block(self.playArea, constants.SHAPES_COORDS[self.shape][i], constants.SHAPES_COLORS[self.shape]))

        self.ground_group.update()
        
    # little goofy
    def collision(self, offsetX: int, offsetY: int):
        for block in self:
            if block.rect.left + offsetX <= self.playArea.left or block.rect.right + offsetX >= self.playArea.right or block.rect.top + offsetY <= self.playArea.top or block.rect.bottom + offsetY >= self.playArea.bottom:
                return True
    
        for block in self:
            block.rect.x += offsetX
            block.rect.y += offsetY

        if pygame.sprite.groupcollide(self, self.ground_group, False, False):
            for block in self:
                block.rect.x -= offsetX
                block.rect.y -= offsetY
            
            return True
        
        for block in self:
            block.rect.x -= offsetX
            block.rect.y -= offsetY

        return False

    def moveLeft(self):
        if self.collision(-constants.CRATE_LEN, 0) is False:
            for block in self:
                block.rect.x -= constants.CRATE_LEN

    def moveRight(self):
        if self.collision(constants.CRATE_LEN, 0) is False:
            for block in self:
                block.rect.x += constants.CRATE_LEN

    def hardDrop(self):
        while self.collision(0, constants.CRATE_LEN) is False:
            for block in self:
                block.rect.y += constants.CRATE_LEN

        self.spawn()

    def softDrop(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            if self.collision(0, constants.CRATE_LEN) is False:
                for block in self:
                    block.rect.y += constants.CRATE_LEN
            else:
                self.spawn()

    def fall(self):
        if time() - self.lastFallTime > 1.5 - (self.level * 0.1):
            if self.collision(0, constants.CRATE_LEN):
                self.spawn()
            else:
                for block in self:
                    block.rect.y += constants.CRATE_LEN

            self.lastFallTime = time()

    def rotate(self, clockwise: bool):
        if self.shape != 'O':
            angle = math.radians(-90 if clockwise else 90)

            centerX = self.sprites()[0].rect.centerx
            centerY = self.sprites()[0].rect.centery

            for block in self:
                relative_x = block.rect.centerx - centerX
                relative_y = block.rect.centery - centerY

                new_x = relative_x * math.cos(angle) - relative_y * math.sin(angle)
                new_y = relative_x * math.sin(angle) + relative_y * math.cos(angle)

                block.rect.centerx = centerX + new_x
                block.rect.centery = centerY + new_y

            if self.collision(0, 0):
                self.rotate(False if clockwise else True)

    def hold(self):
        pass

    def updateOnEvent(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moveLeft()
            elif event.key == pygame.K_RIGHT:
                self.moveRight()
            elif event.key == pygame.K_SPACE:
                self.hardDrop()
            elif event.key == pygame.K_UP:
                self.rotate(False)
            elif event.key == pygame.K_z:
                self.rotate(True)
            elif event.key == pygame.K_c:
                self.hold()

    def update(self):
        self.softDrop()
        self.fall()