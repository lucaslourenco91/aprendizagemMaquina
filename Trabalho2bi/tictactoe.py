import math
import copy

# Definindo os jogadores "X" e "O"
X = "X"
O = "O"
EMPTY = None

# Cria o tabuleiro vazio (3x3)
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# Retorna o próximo jogador a jogar
def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

# Retorna as ações possíveis (posições vazias)
def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions

# Retorna o novo tabuleiro após a jogada
def result(board, action):
    if action not in actions(board):
        raise Exception("Ação inválida")

    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = player(board)
    return new_board

# Verifica se há um vencedor
def winner(board):
    for player_ in [X, O]:
        # Checa linhas
        for row in board:
            if all(cell == player_ for cell in row):
                return player_
        # Checa colunas
        for col in range(3):
            if all(board[row][col] == player_ for row in range(3)):
                return player_
        # Checa diagonais
        if all(board[i][i] == player_ for i in range(3)):
            return player_
        if all(board[i][2 - i] == player_ for i in range(3)):
            return player_
    return None

# Retorna True se o jogo acabou (vitória ou empate)
def terminal(board):
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

# Retorna a pontuação final: 1 para X, -1 para O, 0 para empate
def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

# Algoritmo Minimax para escolher a melhor jogada
def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)

    # Maximiza a utilidade (jogador X)
    def max_value(state):
        if terminal(state):
            return utility(state), None
        v = float('-inf')
        best_action = None
        for action in actions(state):
            min_result, _ = min_value(result(state, action))
            if min_result > v:
                v = min_result
                best_action = action
                if v == 1:
                    break
        return v, best_action

    # Minimiza a utilidade (jogador O)
    def min_value(state):
        if terminal(state):
            return utility(state), None
        v = float('inf')
        best_action = None
        for action in actions(state):
            max_result, _ = max_value(result(state, action))
            if max_result < v:
                v = max_result
                best_action = action
                if v == -1:
                    break
        return v, best_action

    # Escolhe a função com base no jogador atual
    if current_player == X:
        _, action = max_value(board)
    else:
        _, action = min_value(board)

    return action
