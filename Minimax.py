import math
import copy

def maximizar(board, playerNumber, alpha, beta, depth):
    bestScore = -math.inf
    bestMovimiento = []
    scoreActual = 0

    if checkWinner(board):
        if playerNumber == 1:
            playerNumber = 2
        else:
            playerNumber = 1        
        score = checkDiffScore(board, playerNumber)
        return score, []

    if depth > 3:
        score = checkDiffScore(board, playerNumber)
        return score, []

    contador = 0
    bestScore = -math.inf
    # Recorremos el tablero tomando un arreglo a la vez
    # copiaTablero = board
    for i in board:
        contador2 = 0
        # Recorremos el arreglo tomado del arreglo elemento por elemento
        for j in i:
            # copiaArreglo = i
            # Revisamos si el espacio está vacío para hacer nuestra jugada
            if j == 99:
                scoreActual = 0
                scoreActual = scoreJugada(board, playerNumber, [contador, contador2])
                # bestMovimiento = [contador, contador2]
                if scoreActual >= alpha:
                    alpha = scoreActual
                    bestScore = scoreActual
                    bestMovimiento =  [contador, contador2]
                    nuevoTablero = ingresarJugada(copy.deepcopy(board), playerNumber, [contador, contador2])
                    if playerNumber == 1:
                        playerNumber = 2
                    else:
                        playerNumber = 1
                    if bestScore > 0:
                        if playerNumber == 1:
                            playerNumber = 2
                        else:
                            playerNumber = 1
                        score, _ = maximizar(copy.deepcopy(nuevoTablero),copy.deepcopy(playerNumber),-10000,10000, copy.deepcopy(depth + 1))
                    else:
                        score, _ = minimizar(copy.deepcopy(nuevoTablero),copy.deepcopy(playerNumber),-10000,10000, copy.deepcopy(depth + 1))
                    score = scoreActual + score
                    if score > bestScore:
                        bestScore = score
                        bestMovimiento =  [contador, contador2]
            contador2 = contador2 + 1
        contador = contador + 1
    return bestScore, bestMovimiento  

def minimizar(board, playerNumber, alpha, beta, depth):
    bestScore = math.inf
    bestMovimiento = []
    scoreActual = 0

    if checkWinner(board):
        if playerNumber == 1:
            playerNumber = 2
        else:
            playerNumber = 1        
        score = checkDiffScore(board, playerNumber)
        return score, []

    if depth > 3:
        score = checkDiffScore(board, playerNumber)
        return score, []

    contador = 0
    bestScore = math.inf
    # Recorremos el tablero tomando un arreglo a la vez
    # copiaTablero = board
    for i in board:
        contador2 = 0
        # Recorremos el arreglo tomado del arreglo elemento por elemento
        for j in i:
            # copiaArreglo = i
            # Revisamos si el espacio está vacío para hacer nuestra jugada
            if j == 99:
                scoreActual = 0
                scoreActual = scoreJugada(board, playerNumber, [contador, contador2])
                # bestMovimiento = [contador, contador2]
                if scoreActual < beta:
                    beta = scoreActual
                    bestScore = scoreActual * - 1
                    bestMovimiento =  [contador, contador2]
                    nuevoTablero = ingresarJugada(copy.deepcopy(board), playerNumber, [contador, contador2])
                    if playerNumber == 1:
                        playerNumber = 2
                    else:
                        playerNumber = 1
                    score, _ = maximizar(copy.deepcopy(nuevoTablero),copy.deepcopy(playerNumber),-10000,10000, copy.deepcopy(depth + 1))
                    score = score - scoreActual * -1
                    score = -1 * score
                    if score < bestScore:
                        bestScore = score
                        bestMovimiento =  [contador, contador2]
            contador2 = contador2 + 1
        contador = contador + 1
    return bestScore, bestMovimiento 

def checkDiffScore(board, playerNumber):
    player1 = 0
    player2 = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2


    for i in range(len(board[0])):
        if board[0][i] == FILLEDP12:
            player1 = player1 + 2
        elif board[0][i] == FILLEDP11:
            player1 = player1 + 1
        elif board[0][i] == FILLEDP22:
            player2 = player2 + 2
        elif board[0][i] == FILLEDP21:
            player2 = player2 + 1

    for j in range(len(board[1])):
        if board[1][j] == FILLEDP12:
            player1 = player1 + 2
        elif board[1][j] == FILLEDP11:
            player1 = player1 + 1
        elif board[1][j] == FILLEDP22:
            player2 = player2 + 2
        elif board[1][j] == FILLEDP21:
            player2 = player2 + 1

    if playerNumber == 1:
        return player1 - player2
    else:
        return player2 - player1

def scoreJugada(board, playerNumber, move):
    EMPTY = 99
    FILL = 0
    N = 6

    punteoInicial = 0
    punteoFinal = 0

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoInicial = punteoInicial + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0

    board[move[0]][move[1]] = FILL

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoFinal = punteoFinal + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0

    board[move[0]][move[1]] = EMPTY

    return punteoFinal - punteoInicial

def ingresarJugada(board, playerNumber, move):
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6

    punteoInicial = 0
    punteoFinal = 0

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoInicial = punteoInicial + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0

    board[move[0]][move[1]] = FILL

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoFinal = punteoFinal + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    
    if punteoInicial < punteoFinal:
        if playerNumber == 1:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP12
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP11
        elif playerNumber == 2:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP22
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP21
    
    return board

def checkWinner(board):
    pointsP1 = checkMyScore(board, 1)
    pointsP2 = checkMyScore(board, 2)

    if (pointsP1 + pointsP2) == 25:
        return True
    else:
        return False

def checkMyScore(board, playerNumber):
    player1 = 0
    player2 = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2


    for i in range(len(board[0])):
        if board[0][i] == FILLEDP12:
            player1 = player1 + 2
        elif board[0][i] == FILLEDP11:
            player1 = player1 + 1
        elif board[0][i] == FILLEDP22:
            player2 = player2 + 2
        elif board[0][i] == FILLEDP21:
            player2 = player2 + 1

    for j in range(len(board[1])):
        if board[1][j] == FILLEDP12:
            player1 = player1 + 2
        elif board[1][j] == FILLEDP11:
            player1 = player1 + 1
        elif board[1][j] == FILLEDP22:
            player2 = player2 + 2
        elif board[1][j] == FILLEDP21:
            player2 = player2 + 1

    if playerNumber == 1:
        return player1
    else:
        return player2

def checkScore(board, playerNumber):
    player1 = 0
    player2 = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2


    for i in range(len(board[0])):
        if board[0][i] == FILLEDP12:
            player1 = player1 + 2
        elif board[0][i] == FILLEDP11:
            player1 = player1 + 1
        elif board[0][i] == FILLEDP22:
            player2 = player2 + 2
        elif board[0][i] == FILLEDP21:
            player2 = player2 + 1

    for j in range(len(board[1])):
        if board[1][j] == FILLEDP12:
            player1 = player1 + 2
        elif board[1][j] == FILLEDP11:
            player1 = player1 + 1
        elif board[1][j] == FILLEDP22:
            player2 = player2 + 2
        elif board[1][j] == FILLEDP21:
            player2 = player2 + 1

    if playerNumber == 1:
        return player1 - player2
    else:
        return player2 - player1