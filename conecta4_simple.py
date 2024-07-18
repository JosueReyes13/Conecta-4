# Conecta 4 en Python

import numpy as np

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

def play_game():
    """Función principal para jugar Conecta 4"""
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
            col = int(input("Jugador 2, elige una columna (0-6): "))
            piece = PLAYER_2

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)

            if winning_move(board, piece):
                print_board(board)
                print(f"Jugador {piece} gana!")
                game_over = True
            else:
                print_board(board)

            turn += 1
        else:
            print("Columna inválida. Inténtalo de nuevo.")

if __name__ == "__main__":
    play_game()
