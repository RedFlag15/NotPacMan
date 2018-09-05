import pygame

class Rocket(pygame.sprite.Sprite):
    def __init__(self, playerId, playerDirection, playerPos, gridSize, map, enemies):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Assets/player'+playerId+'.jpg').convert()
        self.image = pygame.transform.scale(self.image,(gridSize//4, gridSize//4))
        self.rect = self.image.get_rect()  
        self.rect.x, self.rect.y = playerPos
        self.initialPos = playerPos
        self.direction = playerDirection
        self.speed = 9*2
        self.dx = 0
        self.dy = 0
        self.playerId = playerId
        self.map = map


    def update(self):
        if self.direction == 'right':
            self.dx = self.speed
        elif self.direction == 'left':
            self.dx = -self.speed
        elif self.direction == 'up':
            self.dy = -self.speed
        elif self.direction == 'down':
            self.dy = self.speed
        
        self.rect.x += self.dx
        self.rect.y += self.dy