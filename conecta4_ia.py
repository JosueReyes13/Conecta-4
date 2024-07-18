import numpy as np
import random

# Constantes del juego
ROWS = 6
COLUMNS = 7
PLAYER_1 = 1
PLAYER_2 = 2
EMPTY = 0

def create_board():
    """Crea el tablero de juego vacío"""
    board = np.zeros((ROWS, COLUMNS), dtype=int)
    return board

def drop_piece(board, row, col, piece):
    """Coloca la ficha en el tablero"""
    board[row][col] = piece

def is_valid_location(board, col):
    """Verifica si la columna es válida para colocar una ficha"""
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    """Obtiene la siguiente fila disponible en la columna"""
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    """Imprime el tablero en la consola"""
    print(np.flip(board, 0))

def winning_move(board, piece):
    """Verifica si el movimiento actual es una victoria"""
    # Verifica las filas
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if all([board[r][c+i] == piece for i in range(4)]):
                return True

    # Verifica las columnas
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if all([board[r+i][c] == piece for i in range(4)]):
                return True

    # Verifica las diagonales (positiva)
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if all([board[r+i][c+i] == piece for i in range(4)]):
                return True

    # Verifica las diagonales (negativa)
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if all([board[r-i][c+i] == piece for i in range(4)]):
                return True

    return False

def get_valid_locations(board):
    """Obtiene todas las columnas válidas donde se puede colocar una ficha"""
    valid_locations = []
    for col in range(COLUMNS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    """Elige el mejor movimiento para la IA basado en reglas simples"""
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def score_position(board, piece):
    """Evalúa la puntuación de una posición determinada en el tablero"""
    score = 0

    # Puntuación de las filas
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Puntuación de las columnas
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Puntuación de las diagonales (positiva)
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Puntuación de las diagonales (negativa)
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    """Evalúa la puntuación de una ventana de 4 fichas"""
    score = 0
    opp_piece = PLAYER_1 if piece == PLAYER_2 else PLAYER_2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def play_game():
    """Función principal para jugar Conecta 4 contra la IA"""
    board = create_board()
    game_over = False
    turn = 0

    print_board(board)
    while not game_over:
        # Turno del jugador
        if turn % 2 == 0:
            col = int(input("Jugador 1, elige una columna (0-6): "))
            piece = PLAYER_1
        else:
            # Turno de la IA
            col = pick_best_move(board, PLAYER_2)
            piece = PLAYER_2
            print(f"IA elige la columna {col}")

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)

            if winning_move(board, piece):
                print_board(board)
                if turn % 2 == 0:
                    print("¡Jugador 1 gana!")
                else:
                    print("¡La IA gana!")
                game_over = True
            else:
                print_board(board)

            turn += 1
        else:
            if turn % 2 == 0:
                print("Columna inválida. Inténtalo de nuevo.")

if __name__ == "__main__":
    play_game()
