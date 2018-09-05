import pygame

width = 972
height = 792

class Wall(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (x,y)
        
    
class Map:
    def __init__(self,numMaps , gridSize, model, background, wall):
        self.numMaps = numMaps
        self.model = model
        self.gridSize = gridSize
        self.background = background
        self.wall = wall
        self.texture = pygame.Surface((width, height))
        self.wallsSprites = pygame.sprite.Group()
    def drawMap(self):
        self.texture.blit(self.background,(0,0))
        self.model = open (self.model, 'r')
        for row, line in enumerate(self.model):
            for j in range(0, self.numMaps):
                for column, char in enumerate(line):
                    for i in range(0,self.numMaps):
                        if char == '#':
                            self.wallsSprites.add(Wall(self.gridSize, self.gridSize, (width/self.numMaps*i)+column*self.gridSize, (height/self.numMaps*j)+row*self.gridSize))
                            self.texture.blit(self.wall,((width/self.numMaps*i)+column*self.gridSize,(height/self.numMaps*j)+row*self.gridSize))                        

        self.model.close()