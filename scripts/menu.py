import pygame, sys

clockTickRate = 20
width = 972
height = 792
white = [255, 255, 255]
black = [0, 0, 0]
class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/menubutton.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font = pygame.font.Font("Assets/CinzelDecorative-Bold.otf", 36*2)
        self.text = self.font.render(text, 0, white)
        self.rectText = self.text.get_rect()
        self.width = width
        self.height = height
        self.type = text
    
    def hover(self, cond):
        if cond:
            self.image=pygame.image.load('Assets/menubuttonhover.png').convert_alpha()
            self.image = pygame.transform.scale(self.image,(self.width, self.height))
        else:
            self.image = pygame.image.load("Assets/menubutton.png").convert_alpha()
            self.image = pygame.transform.scale(self.image,(self.width, self.height))

def menu(window, background, clock):
    end = False
    click = False
    font = pygame.font.Font("Assets/CinzelDecorative-Bold.otf", 18)
    waitingForPlayers = font.render("Waiting for players...", 0, black)

    #buttons
    buttonSprites = pygame.sprite.Group()
    playButton = Button(width//2, 36*4, width//4, height//8, "PLAY")
    buttonSprites.add(playButton)
    howButton = Button(width//2-20, 36*4, width//4+10, height//4+height//10, "LEARN")
    buttonSprites.add(howButton)
    exitButton = Button(width//2-30, 36*4, width//4+15, height//2+height//10, "EXIT")
    buttonSprites.add(exitButton)

    #graphics
    window.blit(background, (0,0))
    while not end:
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                click = True
                pygame.event.clear()
                
        buttonSprites.draw(window)
        for button in buttonSprites:
            window.blit(button.text, [button.rect.centerx-(button.rectText.width//2), button.rect.centery-(button.rectText.height//2)])
            if mousePos[0] >= button.rect.left and mousePos[0] <= button.rect.right and mousePos[1] >= button.rect.top and mousePos[1] <= button.rect.bottom:
                button.hover(True)
                if click and button.type=='PLAY':
                    #check players in lobby
                    window.blit(waitingForPlayers, (width-100, height//2 - 18))
                    click = False
                    end = True
                if click and button.type=='EXIT':
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            else:
                button.hover(False)
        
        click = False

        pygame.display.flip()
        clock.tick(clockTickRate)
    
    #player click play
    
