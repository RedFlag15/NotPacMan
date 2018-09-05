import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemyId, pos , gridSize, map):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Assets/player'+enemyId+'.jpg').convert()
        self.image = pygame.transform.scale(self.image,(gridSize//2, gridSize//2))
        self.rect = self.image.get_rect()      
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.id = enemyId
        self.speed = 9
        self.dx = 0
        self.dy = 0
        self.map = map

    def movement(self, enemy, action, direction):
        print(enemy, action, direction)
        print(self.id)
        if enemy.decode("utf-8") == self.id:
            if action == b'press':
                if direction == b'right':
                    self.dx = self.speed
                    self.dy = 0
                elif direction == b'left':
                    self.dx = -self.speed
                    self.dy = 0
                elif direction == b'up':
                    self.dy = -self.speed
                    self.dx = 0
                elif direction == b'down':
                    self.dy = self.speed
                    self.dx = 0
            elif action == b'release':
                self.dx = 0
                self.dy = 0
        print(self.dx, self.dy)

    def collisions(self):
        #sides collision
        self.rect.x += self.dx
        wallsCollide = pygame.sprite.spritecollide(self,self.map.wallsSprites,False)
        for wall in wallsCollide:
            if self.dx > 0:
                self.rect.right = wall.rect.left
            elif self.dx < 0:
                self.rect.left = wall.rect.right
        
        #up and down collision
        self.rect.y += self.dy
        wallsCollide = pygame.sprite.spritecollide(self,self.map.wallsSprites,False)
        for wall in wallsCollide:
            if self.dy > 0:
                self.rect.bottom = wall.rect.top
            elif self.dy < 0:
                self.rect.top = wall.rect.bottom

    def update(self):
        self.collisions()