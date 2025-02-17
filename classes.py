import pygame
import constants

from random import choice
from time import time
import math

class Block(pygame.sprite.Sprite):
    def __init__(self, coords: tuple[int, int], size: int, color = "Black"):
        super().__init__()

        if size == constants.CRATE_LEN:
            try:
                self.image = pygame.image.load(f"graphics/{color}.png").convert()
            except FileNotFoundError:
                self.image = pygame.surface.Surface((size, size)).convert()
                self.image.fill(color=color)
        else:
            self.image = pygame.surface.Surface((size, size)).convert()
            self.image.fill(color=color)

        self.rect = self.image.get_rect(topleft = coords)

class Shape(pygame.sprite.Group):
    def __init__(self, offset: tuple[int, int], size: int, shape = None):
        super().__init__(self)

        self.shape = shape if shape != None else choice(list(constants.SHAPES))

        for i in range(4):
            coords = (offset[0] + (constants.SHAPES[self.shape][i][0] * size), offset[1] + (constants.SHAPES[self.shape][i][1] * size))
            self.add(Block(coords, size, self.shape))

class Ground(pygame.sprite.Group):
    def __init__(self, playArea: pygame.Rect):
        super().__init__()
        self.playArea = playArea
        self.lines = 0

    def update(self):
        colisionBlock = Block((self.playArea.left + 1, self.playArea.top + 1), constants.CRATE_LEN)
        
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
                self.lines += 1

                for block in self:
                    if block.rect.bottom == self.playArea.top + 1 + ((i + 1) * constants.CRATE_LEN):
                        self.remove(block)

                for block in self:
                    if block.rect.bottom <= self.playArea.top + 1 + (i * constants.CRATE_LEN):
                        block.rect.y += constants.CRATE_LEN

class Player(Shape):
    def __init__(self, playArea: pygame.Rect, ground_group: Ground):
        super().__init__((playArea.left + (3 * constants.CRATE_LEN) + 1, playArea.top + 1), constants.CRATE_LEN)

        self.playArea = playArea
        
        self.ground_group = ground_group

        self.lastFallTime = time()
        self.score = 0
        self.level = 1

        self.nextShape = choice([shape for shape in constants.SHAPES if shape != self.shape])

        self.canHold = True
        self.holded = None

        self.putSound = pygame.mixer.Sound("audio/put.mp3")
        self.putSound.set_volume(0.5)

        self.oneClearSound = pygame.mixer.Sound("audio/oneClear.mp3")
        self.oneClearSound.set_volume(0.5)

        self.fourClearSound = pygame.mixer.Sound("audio/fourClear.mp3")
        self.fourClearSound.set_volume(0.5)

    def spawn(self, calledByHold: bool):
        if not calledByHold:
            for block in self:
                self.remove(block)
                self.ground_group.add(block)

            self.shape = self.nextShape
            self.nextShape = choice([shape for shape in constants.SHAPES if shape is not self.shape])

            for i in range(4):    
                coords = (self.playArea.left + (3 * constants.CRATE_LEN) + 1 + (constants.SHAPES[self.shape][i][0] * constants.CRATE_LEN), self.playArea.top + 1 + (constants.SHAPES[self.shape][i][1] * constants.CRATE_LEN))
                self.add(Block(coords, constants.CRATE_LEN, self.shape))

            self.canHold = True

            lastLines = self.ground_group.lines
            self.ground_group.update()

            if self.ground_group.lines - lastLines == 4:
                self.score += 1000
                self.fourClearSound.play()
            elif self.ground_group.lines - lastLines > 0:
                self.score += (self.ground_group.lines - lastLines) * 250
                self.oneClearSound.play()
            else:
                self.score += 100
                self.putSound.play()

            self.level = (self.score // 25000) + 1
        else:
            for block in self:
                self.remove(block)

            if self.holded != None:
                temp = self.shape
                self.shape = self.holded
                self.holded = temp
            else: 
                self.holded = self.shape
                self.shape = self.nextShape
                self.nextShape = choice([shape for shape in constants.SHAPES if shape is not self.shape])

            for i in range(4):    
                coords = (self.playArea.left + (3 * constants.CRATE_LEN) + 1 + (constants.SHAPES[self.shape][i][0] * constants.CRATE_LEN), self.playArea.top + 1 + (constants.SHAPES[self.shape][i][1] * constants.CRATE_LEN))
                self.add(Block(coords, constants.CRATE_LEN, self.shape))

            self.canHold = False
        
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

        self.spawn(False)

    def softDrop(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            if self.collision(0, constants.CRATE_LEN) is False:
                for block in self:
                    block.rect.y += constants.CRATE_LEN
            else:
                self.spawn(False)

    def fall(self):
        if time() - self.lastFallTime > 1.5 - (self.level * 0.1):
            if self.collision(0, constants.CRATE_LEN):
                self.spawn(False)
            else:
                for block in self:
                    block.rect.y += constants.CRATE_LEN

            self.lastFallTime = time()

    def rotate(self, clockwise: bool):
        if self.shape != "Yellow":
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

            for block in self:
                if block.rect.left <= self.playArea.left and self.collision(constants.CRATE_LEN, 0) is False:
                    for b in self:
                        b.rect.x += constants.CRATE_LEN
                    break

            for block in self:
                if block.rect.right >= self.playArea.right and self.collision(-constants.CRATE_LEN, 0) is False:
                    for b in self:
                        b.rect.x -= constants.CRATE_LEN
                    break
            
            for block in self:
                if block.rect.top <= self.playArea.top and self.collision(0, constants.CRATE_LEN) is False:
                    for b in self:
                        b.rect.y += constants.CRATE_LEN
                    break

            for block in self:
                if block.rect.bottom >= self.playArea.bottom and self.collision(0, -constants.CRATE_LEN) is False:
                    for b in self:
                        b.rect.y -= constants.CRATE_LEN
                    break

    def hold(self):
        if self.canHold:
            self.spawn(True)

    # returns game over flag
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

        if self.collision(0, 0):
            return True
        else:
            return False

    # returns game over flag
    def update(self):
        self.softDrop()
        self.fall()

        if self.collision(0, 0):
            return True
        else:
            return False