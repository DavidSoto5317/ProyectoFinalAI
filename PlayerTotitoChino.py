import socketio
import random
import math
from Minimax import maximizar

# Se setean los 
#HOST = 'localhost'
#PORT = '4000'
HOST = input("Ingrese la IP del host:\n")
PORT = input("Ingrese el puerto del host:\n")
userName = input("Ingrese su nombre de usuario para el torneo:\n")
tournamentID = int(input("Ingrese el ID del torneo:\n"))

# Se creal el cliente SocketIO de Python
sio = socketio.Client()
address = 'http://' + HOST + ':' + PORT
sio.connect(address)
#userName = 'NoobMaster69'
#tournamentID = 142857

#listaTirosPosibles = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,15],[0,16],[0,17],[0,18],[0,19],[0,20],[0,21],[0,22],[0,23],[0,24],[0,25],[0,26],[0,27],[0,28],[0,29],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,21],[1,22],[1,23],[1,24],[1,25],[1,26],[1,27],[1,28],[1,29]]

def humanBoard(board):
    resultado = ''
    acumulador = 0

    for i in range(int(len(board[0])/5)):
        if board[0][i] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+6] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+12] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+18] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+24] == 99:
            resultado = resultado + '*   *\n'
        else:
            resultado = resultado + '* - *\n'

        if i != 5:
            for j in range(int(len(board[1])/5)):
                if board[1][j + acumulador] == 99:
                    resultado = resultado + '    '
                else:
                    resultado = resultado + '|   '
            acumulador = acumulador + 6
            resultado = resultado + '\n'

    return resultado

def validateHumanMovement(movement):
    
    if movement == []:
        return False
    
    num = None
    for conv in (int, float, complex):
        try:
            num = conv(movement[0])
            break
        except ValueError:
            pass

    if num is None:
        return False

    num = None
    for conv in (int, float, complex):
        try:
            num = conv(movement[1])
            break
        except ValueError:
            pass

    if num is None:
        return False    

    movement = [int(movement[0]), int(movement[1])]

    if movement[0] < 0 or movement[0] > 1:
        return False

    if movement[1] < 0 or movement[1] > 29:
        return False

    return True

@sio.on('connect')
def connect():
    ## Client has connected
    print("Conectado: " + userName)

    ## Signin signal
    sio.emit('signin', {
        'user_name' : userName,
        'tournament_id' : tournamentID,
        'user_role' : 'player'
    })

@sio.on('ready')
def ready(data):
    ## Client is about to move
    print("About to move. Board:\n")
    print(humanBoard(data['board']))

    ## Aqui está como se cuentan los puntos de cada jugador cuando reciben el tablero
    player1 = 0
    player2 = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2

    for i in range(len(data['board'][0])):
        if data['board'][0][i] == FILLEDP12:
            player1 = player1 + 2
        elif data['board'][0][i] == FILLEDP11:
            player1 = player1 + 1
        elif data['board'][0][i] == FILLEDP22:
            player2 = player2 + 2
        elif data['board'][0][i] == FILLEDP21:
            player2 = player2 + 1

    for j in range(len(data['board'][1])):
        if data['board'][1][j] == FILLEDP12:
            player1 = player1 + 2
        elif data['board'][1][j] == FILLEDP11:
            player1 = player1 + 1
        elif data['board'][1][j] == FILLEDP22:
            player2 = player2 + 2
        elif data['board'][1][j] == FILLEDP21:
            player2 = player2 + 1

    ## Aqui imprimimos los punteos de cada jugador
    print("Yo soy el jugador: ", data['player_turn_id'])
    print("Punteo Jugador 1: ", player1)
    print("Punteo Jugador 2: ", player2)
    movement = []

    while validateHumanMovement(movement) != True:
        #arreglo = input("Ingrese:\n 0. Si desea agregar una raya horizontal\n 1. Si desea agregar una raya vertical\n")
        #posicion = input("Ingrese una posición entre 0 y 29:\n")

        #movement = [arreglo, posicion]

        # Para random del viernes
        tablero = data['board']
        #listaTirosPosibles = []
        #contador = 0
        #for i in tablero:
        #    contador2 = 0
        #    for j in i:
        #        if j == 99:
        #            listaTirosPosibles.append([contador,contador2])
        #        contador2 = contador2 + 1
        #    contador = contador + 1
 
        #movement = random.choice(listaTirosPosibles)

        _, movement = maximizar(tablero, data['player_turn_id'], -10000, 10000, 0)
        print(movement)
        #listaTirosPosibles.remove(movement)

    #movement = [int(arreglo), int(posicion)]

    sio.emit('play', {
        'player_turn_id' : data['player_turn_id'],
        'tournament_id' : tournamentID,
        'game_id' : data['game_id'],
        'movement': movement
    })

@sio.on('finish')
def finish(data):
    print("Game", data['game_id'], "has finished")
    if data['winner_turn_id'] == data['player_turn_id']:
        print("Tu ganaste")
    else:
        print("Tu perdiste")

    print("Ready to play again!")

    ## Start Again

    sio.emit('player_ready', {
        'tournament_id' : tournamentID,
        'game_id' : data['game_id'],
        'player_turn_id': data['player_turn_id']
    })


