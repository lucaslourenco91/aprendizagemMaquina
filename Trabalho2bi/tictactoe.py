import math
import copy

# Constantes para representar os jogadores e uma célula vazia
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Retorna o estado inicial do tabuleiro.
    Um tabuleiro vazio (3x3) representado por listas dentro de uma lista.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Retorna o jogador que tem o próximo turno no tabuleiro.
    Se o número de X for igual ou menor que o número de O, é a vez de X.
    Caso contrário, é a vez de O.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    """
    Retorna um conjunto com todas as ações possíveis no tabuleiro.
    Cada ação é uma tupla (i, j) representando a linha e a coluna de uma célula vazia.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Retorna o novo estado do tabuleiro após o jogador fazer o movimento indicado por action.
    Não altera o tabuleiro original.

    Se a ação for inválida, levanta uma exceção.
    """
    if action not in actions(board):
        raise Exception("Ação inválida")

    # Faz uma cópia profunda do tabuleiro para não alterar o original
    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Retorna o vencedor do jogo, se houver.
    Pode ser X, O ou None (se ainda não houver vencedor).
    """
    for player_ in [X, O]:
        # Verifica todas as linhas
        for row in board:
            if all(cell == player_ for cell in row):
                return player_

        # Verifica todas as colunas
        for col in range(3):
            if all(board[row][col] == player_ for row in range(3)):
                return player_

        # Verifica as duas diagonais
        if all(board[i][i] == player_ for i in range(3)):
            return player_

        if all(board[i][2 - i] == player_ for i in range(3)):
            return player_

    return None  # Sem vencedor


def terminal(board):
    """
    Retorna True se o jogo acabou (vitória ou empate), False caso contrário.
    """
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)


def utility(board):
    """
    Retorna o valor da utilidade do tabuleiro terminal:
    1 se X venceu,
    -1 se O venceu,
    0 em caso de empate.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Retorna a ação ótima para o jogador atual no tabuleiro.
    Utiliza o algoritmo Minimax com uma pequena otimização (poda simplificada).
    """
    if terminal(board):
        return None

    current_player = player(board)

    # Função para o jogador MAX (X)
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
                    break  # Melhor resultado possível, pode parar
        return v, best_action

    # Função para o jogador MIN (O)
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
                    break  # Pior resultado possível para O, pode parar
        return v, best_action

    # Decide quem vai jogar agora e chama a função correspondente
    if current_player == X:
        _, action = max_value(board)
    else:
        _, action = min_value(board)

    return action
