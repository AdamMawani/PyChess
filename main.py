import tkinter as tk

class ChessGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Chess Game")
        self.geometry("600x600")
        self.current_turn = 'white'
        self.create_board()
        self.draw_board()

    def create_board(self):
        self.board = []
        for i in range(8):
            self.board.append([None] * 8)

        # Place white pieces
        self.place_piece(0, 0, '♖', 'white')
        self.place_piece(0, 1, '♘', 'white')
        self.place_piece(0, 2, '♗', 'white')
        self.place_piece(0, 3, '♕', 'white')
        self.place_piece(0, 4, '♔', 'white')
        self.place_piece(0, 5, '♗', 'white')
        self.place_piece(0, 6, '♘', 'white')
        self.place_piece(0, 7, '♖', 'white')
        for i in range(8):
            self.place_piece(1, i, '♙', 'white')

        # Place black pieces
        self.place_piece(7, 0, '♜', 'black')
        self.place_piece(7, 1, '♞', 'black')
        self.place_piece(7, 2, '♝', 'black')
        self.place_piece(7, 3, '♛', 'black')
        self.place_piece(7, 4, '♚', 'black')
        self.place_piece(7, 5, '♝', 'black')
        self.place_piece(7, 6, '♞', 'black')
        self.place_piece(7, 7, '♜', 'black')
        for i in range(8):
            self.place_piece(6, i, '♟', 'black')

    def place_piece(self, row, col, piece_type, color):
        piece = Piece(piece_type, color)
        self.board[row][col] = piece

    def draw_board(self):
        self.canvas = tk.Canvas(self, width=600, height=600)
        self.canvas.pack()

        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(col * 75, row * 75, (col + 1) * 75, (row + 1) * 75, fill=color)

                piece = self.board[row][col]
                if piece is not None:
                    self.canvas.create_text(col * 75 + 37, row * 75 + 37, text=piece.icon, font=("Helvetica", 36))

    def is_valid_move(self, start_pos, end_pos):
        row1, col1 = start_pos
        row2, col2 = end_pos
        piece = self.board[row1][col1]

        if piece is None:  # No piece at start position
            return False

        # Basic checks (within bounds, not same position, not on same color piece)
        if not (0 <= row2 <= 7 and 0 <= col2 <= 7) or start_pos == end_pos or \
                (self.board[row2][col2] is not None and self.board[row2][col2].color == piece.color):
            return False

        # Implement piece-specific movement rules
        if piece.icon in ('♙', '♟'):  # Pawn
            if piece.color == 'white':
                if row2 == row1 - 1 and col2 == col1 and self.board[row2][col2] is None:
                    return True
                if row1 == 6 and row2 == 4 and col1 == col2 and self.board[5][col2] is None and self.board[4][col2] is None:
                    return True
            else:
                if row2 == row1 + 1 and col2 == col1 and self.board[row2][col2] is None:
                    return True
                if row1 == 1 and row2 == 3 and col1 == col2 and self.board[2][col2] is None and self.board[3][col2] is None:
                    return True
            return False

        elif piece.icon in ('♖', '♜'):  # Rook
            if row1 == row2 or col1 == col2:
                if row1 == row2:
                    step = 1 if col2 > col1 else -1
                    for c in range(col1 + step, col2, step):
                        if self.board[row1][c] is not None:
                            return False
                else:
                    step = 1 if row2 > row1 else -1
                    for r in range(row1 + step, row2, step):
                        if self.board[r][col1] is not None:
                            return False
                return True
            return False

        elif piece.icon in ('♘', '♞'):  # Knight
            if (abs(row2 - row1), abs(col2 - col1)) in [(1, 2), (2, 1)]:
                return True
            return False

        elif piece.icon in ('♗', '♝'):  # Bishop
            if abs(row2 - row1) == abs(col2 - col1):
                step_r = 1 if row2 > row1 else -1
                step_c = 1 if col2 > col1 else -1
                r, c = row1 + step_r, col1 + step_c
                while (r, c) != (row2, col2):
                    if self.board[r][c] is not None:
                        return False
                    r += step_r
                    c += step_c
                return True
            return False

        elif piece.icon in ('♕', '♛'):  # Queen
            if row1 == row2 or col1 == col2:
                return self.is_valid_move((row1, col1), (row2, col2))  # Rook movement
            elif abs(row2 - row1) == abs(col2 - col1):
                return self.is_valid_move((row1, col1), (row2, col2))  # Bishop movement
            return False

        elif piece.icon in ('♔', '♚'):  # King
            if abs(row2 - row1) <= 1 and abs(col2 - col1) <= 1:
                return True
            return False

        return False  # If none of the above conditions are met, the move is invalid

    def move_piece(self, start_pos, end_pos):
        row1, col1 = start_pos
        row2, col2 = end_pos
        piece = self.board[row1][col1]
        if piece is None or piece.color != self.current_turn:
            return False
        if self.is_valid_move(start_pos, end_pos):
            self.board[row2][col2] = piece
            self.board[row1][col1] = None
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            self.draw_board()
            return True
        return False

    def on_click(self, event):
        col = event.x // 75
        row = event.y // 75
        print(f"Clicked: ({row}, {col})")

    def start(self):
        self.canvas.bind("<Button-1>", self.on_click)
        self.mainloop()


class Piece:
    def __init__(self, icon, color):
        self.icon = icon
        self.color = color


if __name__ == "__main__":
    game = ChessGame()
    game.start()