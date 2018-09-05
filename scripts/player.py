import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, playerId, gridSize, map, socket):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Assets/player'+playerId+'.jpg').convert()
        self.image = pygame.transform.scale(self.image,(gridSize//2, gridSize//2))
        self.rect = self.image.get_rect()      
        self.rect.x = 36
        self.rect.y = 36
        self.speed = 9
        self.dx = 0
        self.dy = 0
        self.map = map
        self.event = []
        self.id = playerId
        self.socket = socket
        self.keyState = 'released'
        self.keyAction = ''
       
    def movement(self):
        #when player release a button
        if self.event.type == pygame.KEYUP:
            if self.event.key == pygame.K_RIGHT and self.keyAction == 'right':
                self.socket.send_multipart([self.id.encode("utf-8"), b'release', b'right'])
                self.dx=0                
                self.keyAction = ''
            if self.event.key == pygame.K_LEFT and self.keyAction == 'left':
                self.socket.send_multipart([self.id.encode("utf-8"), b'release', b'right'])
                self.dx=0                
                self.keyAction = ''
            if self.event.key == pygame.K_UP and self.keyAction == 'up':
                self.socket.send_multipart([self.id.encode("utf-8"), b'release', b'right'])
                self.dy = 0                
                self.keyAction = ''
            if self.event.key == pygame.K_DOWN and self.keyAction == 'down':
                self.socket.send_multipart([self.id.encode("utf-8"), b'release', b'right'])
                self.dy = 0                
                self.keyAction = ''
        #when player press a button
        if self.event.type == pygame.KEYDOWN:
            print(self.event.key)
            if self.event.key == pygame.K_RIGHT and self.keyAction != 'right':
                self.socket.send_multipart([self.id.encode("utf-8"), b'press', b'right'])
                self.dx = self.speed
                self.dy = 0
                self.keyAction = 'right'
                self.keyState = 'right'
            if self.event.key == pygame.K_LEFT and self.keyAction != 'left':
                self.socket.send_multipart([self.id.encode("utf-8"), b'press', b'left'])
                self.dx=-self.speed
                self.dy = 0
                self.keyAction = 'left'
                self.keyState = 'left'
            if self.event.key == pygame.K_UP and self.keyAction != 'up':
                self.socket.send_multipart([self.id.encode("utf-8"), b'press', b'up'])
                self.dy=-self.speed
                self.dx = 0
                self.keyAction = 'up'
                self.keyState = 'up'
            if self.event.key == pygame.K_DOWN and self.keyAction != 'down':
                self.socket.send_multipart([self.id.encode("utf-8"), b'press', b'down'])
                self.dy=self.speed
                self.dx = 0
                self.keyAction = 'down'
                self.keyState = 'down'          
        self.event = 0
        
    def collisions(self):
        #sides collision
        self.rect.x += self.dx
        wallsCollide = pygame.sprite.spritecollide(self, self.map.wallsSprites, False)
        for wall in wallsCollide:
            if self.dx > 0:
                self.rect.right = wall.rect.left
            elif self.dx < 0:
                self.rect.left = wall.rect.right
        
        #up and down collision
        self.rect.y += self.dy
        wallsCollide = pygame.sprite.spritecollide(self, self.map.wallsSprites, False)
        for wall in wallsCollide:
            if self.dy > 0:
                self.rect.bottom = wall.rect.top
            elif self.dy < 0:
                self.rect.top = wall.rect.bottom

    def update(self):
        #movement
        #self.movement()
        self.collisions()
        
        
        

        
        
            
            