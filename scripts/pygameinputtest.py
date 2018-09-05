import pygame
pygame.init()
width = 972
height = 792

#pygame basic settings
window = pygame.display.set_mode((width,height))
pygame.key.set_repeat()

while True:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        else:
            if event.type == pygame.KEYDOWN:
                print (event.key)
                if event.key==pygame.K_RIGHT:
                    print('press right')
                if event.key==pygame.K_LEFT:
                    print('press left')
            if event.type == pygame.KEYUP:
                print (event.key)
                if event.key==pygame.K_RIGHT:
                    print('release right')
                if event.key==pygame.K_LEFT:
                    print('release left')
            pygame.event.clear()

    
    #pygame refresh
    pygame.display.flip()