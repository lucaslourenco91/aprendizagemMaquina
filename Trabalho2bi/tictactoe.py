import math
import copy

# Define os jogadores
X = "X"
O = "O"
EMPTY = None

# Cria o tabuleiro no formato do jogo da velha
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# Retorna o próximo jogador a jogar
def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

# Retorna as ações possíveis, verificando as partes vazias do tabuleiro
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

# Verifica se o jogo terminou (vitória ou empate)
def terminal(board):
    # Primeiro, verifica se há um vencedor
    if winner(board) is not None:
        return True

    # Agora, verifica se todas as casas estão preenchidas (sem EMPTY)
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False  # Ainda tem espaço vazio, o jogo continua

    # Se não há vencedor e não há espaço vazio, é empate
    return True

# defina a pontuação final: 1 para X, -1 para O, 0 para empate
def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

# Função que escolhe a melhor jogada para o jogador X (o que quer maximizar o placar)
def max_value(state):
    # Se o jogo já terminou, retorna a pontuação final e nenhuma ação
    if terminal(state):
        return utility(state), None

    # Inicializa a melhor pontuação com o menor valor possível
    melhor_valor = float('-inf')
    melhor_acao = None

    # Testa todas as jogadas possíveis
    for acao in actions(state):
        # Simula o resultado depois de fazer essa jogada
        novo_estado = result(state, acao)

        # Chama a função min_value para ver como o jogador O vai reagir a essa jogada
        valor_do_oponente, _ = min_value(novo_estado)

        # Se essa jogada der um resultado melhor, atualiza
        if valor_do_oponente > melhor_valor:
            melhor_valor = valor_do_oponente
            melhor_acao = acao

            # Se for o melhor caso possível para X, já pode parar
            if melhor_valor == 1:
                break

    # Retorna o melhor valor encontrado e a jogada correspondente
    return melhor_valor, melhor_acao

# Função que escolhe a melhor jogada para o jogador O (o que quer minimizar o placar)
def min_value(state):
    # Se o jogo já terminou, retorna a pontuação final e nenhuma ação
    if terminal(state):
        return utility(state), None

    # Inicializa a melhor pontuação com o maior valor possível
    melhor_valor = float('inf')
    melhor_acao = None

    # Testa todas as jogadas possíveis
    for acao in actions(state):
        # Simula o resultado depois de fazer essa jogada
        novo_estado = result(state, acao)

        valor_do_oponente, _ = max_value(novo_estado)
 
        if valor_do_oponente < melhor_valor:
            melhor_valor = valor_do_oponente
            melhor_acao = acao

            if melhor_valor == -1:
                break

    return melhor_valor, melhor_acao

# Algoritmo Minimax para escolher a melhor jogada
def minimax(board):
    if terminal(board):
        return None

    jogador_atual = player(board)

    if jogador_atual == X:
        _, acao = max_value(board)
    else:
        _, acao = min_value(board)

    return acao
