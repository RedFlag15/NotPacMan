import math, pygame, os, zmq, sys, _thread
from scripts import map, player, menu, enemy, rocket

#ip = "192.168.60.60"
ip = "localhost"

if len(sys.argv) != 3:
        print("Must have a name and id! * Sample call: python PacMan2.py <name> <id> *")
        exit()
name = sys.argv[1].encode('utf-8')
id = sys.argv[2].encode('utf-8')

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1' #center the window on desktop

#variables to modify
numPlayers = 15
maxPlayers = 15
grid = 36
spawnPositions = [[36,36], [36*15, 36], [36, 36*20], [36*14, 36*18], [36*14, 36*12]]

#socket initialize
context = zmq.Context()
socket = context.socket(zmq.DEALER)
syncSocket = context.socket(zmq.DEALER)
socket.setsockopt(zmq.IDENTITY, id)
syncSocket.setsockopt(zmq.IDENTITY, id)
socket.connect("tcp://"+ip+":5555")
syncSocket.connect("tcp://"+ip+":6666")
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
poller.register(syncSocket, zmq.POLLIN)

#basic variables
numMaps = math.ceil(numPlayers/maxPlayers)
gridSize = grid//numMaps
clockTickRate = 20
end = False
width = 972
widthWindow = width + 200
height = 792
checkWin = 0

#pygame basic settings
window = pygame.display.set_mode((widthWindow, height))
pygame.display.set_caption('Pac-Man?')
clock = pygame.time.Clock()
pygame.key.set_repeat()
font = pygame.font.Font("Assets/CinzelDecorative-Bold.otf", 18)

#loadResources
background = pygame.image.load('Assets/background.jpg').convert()
wall = pygame.image.load('Assets/wall-01.png').convert()
wall = pygame.transform.scale(wall,(gridSize,gridSize))
Map = map.Map(numMaps, gridSize, 'maze.txt', background, wall)
Map.drawMap()

def on_draw():
    window.blit(Map.texture,(0,0))
    window.blit(font.render(name, 0, menu.black), (width+50, height//4))
    window.blit(player.image, (width+10, height//4))
    inc = 0
    #rockets
    enemiesRockets.draw(window)
    enemiesRockets.update()
    rockets.draw(window)
    rockets.update()
    #enemies
    enemies.draw(window)
    enemies.update()
    #player
    players.draw(window)
    players.update()
    #players names
    for en in enemiesNames:
        if name != en[0]:
            inc += 30
            window.blit(font.render(en[0], 0, menu.black), (width+50, height//4 + inc))
            for eny in enemies2:
                if eny.id == en[1]:
                    window.blit(eny.image, (width+10, height//4 + inc))

def spawnEnemies(spawnPos, spawnPositions):
    enemies = pygame.sprite.Group()
    for enum, i in enumerate(spawnPositions):
        if enum != spawnPos:
            newEnemy = enemy.Enemy(str(enum), i, gridSize, Map)
            enemies.add(newEnemy)
            enemies2.add(newEnemy)
    return enemies

def recBroadcast(socket, enemies):
    while True:
        enemyId, action, direction = socket.recv_multipart()
        if action != b'shoot':
            for en in enemies:
                en.movement(enemyId, action, direction)
        else:
            for en in enemies:
                if enemyId.decode("utf-8") == en.id:
                    enRocket = rocket.Rocket(en.id, direction.decode("utf-8"), [en.rect.x, en.rect.y], gridSize, Map, socket)                    
                    enemiesRockets.add(enRocket)
                    #mixer('Assets/40_smith_wesson_single-mike-koenig.wav')

def recSync(socket, enemies):
    while True:
        enemyInfo = socket.recv().decode("utf-8")
        enemyInfo = eval(enemyInfo)
        #print(enemyInfo)
        for en in enemies2:
            for i in enemyInfo:
                if i[0].decode("utf-8") == en.id:
                    en.rect.x = int(i[1].decode("utf-8"))
                    en.rect.y = int(i[2].decode("utf-8"))

def mixer(archivo):
	sound=pygame.mixer.Sound(archivo)
	sound.play()
	sound.set_volume(0.2)

def music(archivo):
	pygame.mixer.music.load(archivo)
	pygame.mixer.music.play(-1)
	pygame.mixer.music.set_volume(0.01)

#main loop
if __name__ == '__main__':
        #get an id for player
        socket.send(name)
        newId = socket.recv().decode("utf-8")
        print ("Got spawn position {}".format(newId))

        #initialize player
        players = pygame.sprite.Group()
        player = player.Player(newId, gridSize, Map, socket)
        player.event = pygame.event.get()[0]
        players.add(player)
        rockets = pygame.sprite.Group()
        shootRocket = ''
        listRocketEnemiesCollision = []
        enemiesRockets = pygame.sprite.Group()
        enemies2 = pygame.sprite.Group()

        #start music theme
        music('Assets/TheLoomingBattle.OGG')
        
        #menu loop
        menu.menu(window, background, clock)
        print ('Waiting for players...')
        
        #start the game and spawning enemies
        socket.send(b'ready')
        res, enemiesNames = socket.recv_multipart()
        enemiesNames = eval(enemiesNames.decode("utf-8"))
        print ("Got {}".format(res))
        enemies = spawnEnemies(int(newId), spawnPositions)

        #Threads for multiplayer connection
        _thread.start_new_thread(recBroadcast, (socket, enemies))
        _thread.start_new_thread(recSync, (syncSocket, enemies))

        if res == b'start':
            window.blit(background, (0,0))
            player.rect.x, player.rect.y = spawnPositions[int(newId)]
            while not end:
                #events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = True
                    else:
                        player.event = event
                        player.movement()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_z and len(rockets.sprites()) == 0:
                                mixer('Assets/40_smith_wesson_single-mike-koenig.wav')
                                if checkWin == 0:
                                    socket.send_multipart([player.id.encode("utf-8"), b'shoot', player.keyState.encode("utf-8")])
                                shootRocket = rocket.Rocket(player.id, player.keyState, [player.rect.x, player.rect.y], gridSize, Map, socket)
                                rockets.add(shootRocket)                                  
                            if event.key == pygame.K_SPACE and checkWin == 1:
                                end = True                              
                        pygame.event.clear()

                #rocket collision
                if shootRocket != '':
                    rocketCollide = pygame.sprite.spritecollide(shootRocket, enemies, False)
                    rocketWallCollide = pygame.sprite.spritecollide(shootRocket, Map.wallsSprites, False)
                    if len(rocketCollide) != 0:
                        shootRocket.kill()
                        for en in rocketCollide:
                            en.kill()
                    if len(rocketWallCollide) != 0:
                        shootRocket.kill()

                if len(enemiesRockets) != 0:
                    enRocketsWithWalls = pygame.sprite.groupcollide(enemiesRockets, Map.wallsSprites, True, False)
                    playerRocketCollide = pygame.sprite.spritecollide(player, enemiesRockets, True)                
                    if len(playerRocketCollide) != 0:
                        player.kill()

                    enemiesRocketCollide = pygame.sprite.groupcollide(enemies, enemiesRockets, False, False)
                    for col in enemiesRocketCollide.keys():
                        for col2 in enemiesRocketCollide[col]:
                            if col.id != col2.playerId:
                                col.kill()
                                col2.kill()

                on_draw()

                #win or lose
                if len(enemies) == 0:
                    if len(players) != 0:
                        window.blit(font.render("You Win!!", 0, menu.black), (width//2 - 10, height//2))  
                        if checkWin == 0:                  
                            socket.send(b'win')
                        checkWin = 1
                else:
                    if len(players) == 0:
                        window.blit(font.render("You Lose", 0, menu.black), (width//2 - 10, height//2))
                        if len(enemies) == 1:
                            for won in enemies:
                                for en in enemiesNames:
                                    if won.id == en[1]:
                                        window.blit(font.render(en[0].decode("utf-8")+" Won the Game!!", 0, menu.black), (width//2 - 60, height//2 + 50))
                                        checkWin = 1

                #position sync between players
                gameTime = pygame.time.get_ticks()
                gameTime = gameTime // 1000
                if (gameTime % (1/2)) == 0 and checkWin == 0:
                    syncSocket.send_multipart([player.id.encode("utf-8"), str(player.rect.x).encode("utf-8"), str(player.rect.y).encode("utf-8")])
                
                #pygame refresh
                pygame.display.flip()
                clock.tick(clockTickRate)
