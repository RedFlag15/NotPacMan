import zmq, _thread

#ip = "192.168.60.60"
ip = '*'
numPlayers = 2

#socket initialization
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
syncSocket = context.socket(zmq.ROUTER)
socket.bind("tcp://{}:5555".format(ip))
syncSocket.bind("tcp://{}:6666".format(ip))

def lobby():
    idForPlayer = 0
    gameStart = False
    while not gameStart:
        idPlayer, namePlayer = socket.recv_multipart() #new client
        if namePlayer == b'ready':
            players[idPlayer] = [namePlayer]
        else:
            print("New player: id {} name {}".format(idPlayer, namePlayer))
            socket.send_multipart([idPlayer, str(idForPlayer).encode("utf-8")])
            playersNames.append((namePlayer, str(idForPlayer)))
            idForPlayer += 1
        if len(players) == numPlayers:   #max players on lobby
            print("Game start")
            gameStart = True
            for player in players.keys(): 
                socket.send_multipart([player, b'start', str(playersNames).encode("utf-8")]) #send START

def sync(socket):
    syncList = []
    while True:
        sender, idPlayer, x, y = socket.recv_multipart()
        if syncList.count([idPlayer, x, y]) == 0:
            syncList.append([idPlayer, x, y])
        if len(syncList) == numPlayers:
            for player in players.keys():
                socket.send_multipart([player, str(syncList).encode("utf-8")])
            syncList = []

def game():
    _thread.start_new_thread(sync, (syncSocket, ))
    endGame = False
    while not endGame:
        idPlayer, *rest = socket.recv_multipart()
        if rest[0] == b'win':
            endGame = True
        else:
            for player in players.keys():
                if idPlayer != player:
                    socket.send_multipart([player, rest[0], rest[1], rest[2]])


if __name__ == '__main__':
    players = {}
    playersNames = []
    lobby()
    game()
