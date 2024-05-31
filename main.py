import tkinter as tk
from tkinter import simpledialog, messagebox

class ChessGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Chess Game")
        self.geometry("600x600")
        self.current_turn = 'white'
        self.selected_piece = None
        self.en_passant_target = None
        self.white_king_moved = self.black_king_moved = False
        self.white_rook_moved = [False, False]
        self.black_rook_moved = [False, False]
        self.last_move = None
        self.move_history = []
        self.game_state = 'ongoing'
        self.create_board()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def create_board(self):
        self.board = []
        for i in range(8):
            self.board.append([None] * 8)

        for color, row_pawn, row_back in [('white', 6, 7), ('black', 1, 0)]:
            self.place_piece(row_back, 0, '♖', color)
            self.place_piece(row_back, 1, '♘', color)
            self.place_piece(row_back, 2, '♗', color)
            self.place_piece(row_back, 3, '♕', color)
            self.place_piece(row_back, 4, '♔', color)
            self.place_piece(row_back, 5, '♗', color)
            self.place_piece(row_back, 6, '♘', color)
            self.place_piece(row_back, 7, '♖', color)
            for i in range(8):
                self.place_piece(row_pawn, i, '♙', color)

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

        if self.last_move:
            row1, col1, row2, col2 = self.last_move
            self.canvas.create_rectangle(col1 * 75, row1 * 75, (col1 + 1) * 75, (row1 + 1) * 75, outline="yellow", width=3)
            self.canvas.create_rectangle(col2 * 75, row2 * 75, (col2 + 1) * 75, (row2 + 1) * 75, outline="yellow", width=3)

        if self.selected_piece:
            row, col = self.selected_piece
            self.canvas.create_rectangle(col * 75, row * 75, (col + 1) * 75, (row + 1) * 75, outline="blue", width=3)
            self.highlight_possible_moves()

        self.show_game_status()

    def highlight_possible_moves(self):
        row, col = self.selected_piece
        piece = self.board[row][col]
        if piece and piece.color == self.current_turn:
            for r in range(8):
                for c in range(8):
                    if self.is_valid_move((row, col), (r, c)):
                        self.canvas.create_rectangle(c * 75, r * 75, (c + 1) * 75, (r + 1) * 75, outline="green", width=3)

    def is_valid_move(self, start_pos, end_pos):
        row1, col1 = start_pos
        row2, col2 = end_pos
        piece = self.board[row1][col1]

        if piece is None:
            return False

        if not (0 <= row2 <= 7 and 0 <= col2 <= 7) or start_pos == end_pos or \
                (self.board[row2][col2] is not None and self.board[row2][col2].color == piece.color):
            return False

        if piece.icon in ('♙', '♟'):
            direction = -1 if piece.color == 'white' else 1
            start_row = 6 if piece.color == 'white' else 1
            if (row2 == row1 + direction and col2 == col1 and self.board[row2][col2] is None) or \
               (row1 == start_row and row2 == row1 + 2 * direction and col1 == col2 and 
                self.board[row1 + direction][col2] is None and self.board[row2][col2] is None):
                self.en_passant_target = (row1 + direction, col1) if abs(row2 - row1) == 2 else None
                return True
            if row2 == row1 + direction and abs(col2 - col1) == 1:
                if self.board[row2][col2] is not None:
                    return True
                if self.en_passant_target == (row2, col2) and self.board[row1][col2] is not None and \
                   self.board[row1][col2].color != piece.color and self.board[row1][col2].icon in ('♙', '♟'):
                    return True
            return False

        elif piece.icon in ('♖', '♜'):
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

        elif piece.icon in ('♘', '♞'):
            if (abs(row2 - row1), abs(col2 - col1)) in [(1, 2), (2, 1)]:
                return True
            return False

        elif piece.icon in ('♗', '♝'):
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

        elif piece.icon in ('♕', '♛'):
            if row1 == row2 or col1 == col2:
                return self.is_valid_move((row1, col1), (row2, col2))
            elif abs(row2 - row1) == abs(col2 - col1):
                return self.is_valid_move((row1, col1), (row2, col2))
            return False

        elif piece.icon in ('♔', '♚'):
            if abs(row2 - row1) <= 1 and abs(col2 - col1) <= 1:
                return True
            if row1 == row2 and abs(col2 - col1) == 2:
                if piece.color == 'white' and not self.white_king_moved and \
                   ((col2 == 6 and not self.white_rook_moved[1] and all(self.board[row1][c] is None for c in range(5, 7))) or \
                    (col2 == 2 and not self.white_rook_moved[0] and all(self.board[row1][c] is None for c in range(1, 4)))):
                    return True
                if piece.color == 'black' and not self.black_king_moved and \
                   ((col2 == 6 and not self.black_rook_moved[1] and all(self.board[row1][c] is None for c in range(5, 7))) or \
                    (col2 == 2 and not self.black_rook_moved[0] and all(self.board[row1][c] is None for c in range(1, 4)))):
                    return True
            return False

        return False

    def move_piece(self, start_pos, end_pos):
        row1, col1 = start_pos
        row2, col2 = end_pos
        piece = self.board[row1][col1]
        if piece is None or piece.color != self.current_turn:
            return False
        if self.is_valid_move(start_pos, end_pos):
            if piece.icon in ('♙', '♟') and self.en_passant_target == (row2, col2):
                self.board[row1][col2] = None

            if piece.icon in ('♔', '♚') and abs(col2 - col1) == 2:
                if col2 == 6:
                    self.board[row1][5], self.board[row1][7] = self.board[row1][7], None
                elif col2 == 2:
                    self.board[row1][3], self.board[row1][0] = self.board[row1][0], None

            self.board[row2][col2] = piece
            self.board[row1][col1] = None

            if piece.icon in ('♙', '♟') and (row2 == 0 or row2 == 7):
                promoted_piece = simpledialog.askstring("Promotion", "Choose piece (Q, R, B, N):")
                promotion_dict = {'Q': '♕' if piece.color == 'white' else '♛',
                                  'R': '♖' if piece.color == 'white' else '♜',
                                  'B': '♗' if piece.color == 'white' else '♝',
                                  'N': '♘' if piece.color == 'white' else '♞'}
                self.board[row2][col2] = Piece(promotion_dict.get(promoted_piece, '♕' if piece.color == 'white' else '♛'), piece.color)

            if piece.icon == '♔':
                self.white_king_moved = True
            elif piece.icon == '♚':
                self.black_king_moved = True
            elif piece.icon == '♖' and row1 == 7:
                self.white_rook_moved[0 if col1 == 0 else 1] = True
            elif piece.icon == '♜' and row1 == 0:
                self.black_rook_moved[0 if col1 == 0 else 1] = True

            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            self.en_passant_target = None
            self.last_move = (row1, col1, row2, col2)
            self.move_history.append((start_pos, end_pos))
            self.check_game_status()
            self.draw_board()
            return True
        return False

    def undo_move(self):
        if not self.move_history:
            return
        start_pos, end_pos = self.move_history.pop()
        row1, col1 = start_pos
        row2, col2 = end_pos
        piece = self.board[row2][col2]
        self.board[row1][col1] = piece
        self.board[row2][col2] = None
        if piece.icon in ('♔', '♚') and abs(col2 - col1) == 2:
            if col2 == 6:
                self.board[row1][5], self.board[row1][7] = None, self.board[row1][5]
            elif col2 == 2:
                self.board[row1][3], self.board[row1][0] = None, self.board[row1][3]

        if piece.icon in ('♙', '♟') and self.en_passant_target == (row2, col2):
            self.board[row1][col2] = Piece('♙' if piece.color == 'black' else '♟', 'black' if piece.color == 'white' else 'white')

        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        self.en_passant_target = None
        self.last_move = None
        self.draw_board()

    def on_click(self, event):
        col = event.x // 75
        row = event.y // 75
        if self.selected_piece:
            if self.move_piece(self.selected_piece, (row, col)):
                self.selected_piece = None
            else:
                self.selected_piece = (row, col)
        else:
            self.selected_piece = (row, col)
        self.draw_board()

    def show_game_status(self):
        status_text = f"Turn: {self.current_turn.capitalize()}"
        if self.is_in_check('white'):
            status_text += " - White is in check"
        if self.is_in_check('black'):
            status_text += " - Black is in check"
        if self.is_checkmate('white'):
            status_text = "Checkmate! Black wins!"
            self.game_state = 'finished'
        if self.is_checkmate('black'):
            status_text = "Checkmate! White wins!"
            self.game_state = 'finished'
        self.canvas.create_text(300, 10, text=status_text, font=("Helvetica", 16), fill="black")

    def is_in_check(self, color):
        king_pos = None
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == color and piece.icon in ('♔', '♚'):
                    king_pos = (r, c)
                    break
        if not king_pos:
            return False
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color != color:
                    if self.is_valid_move((r, c), king_pos):
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == color:
                    for rr in range(8):
                        for cc in range(8):
                            if self.is_valid_move((r, c), (rr, cc)):
                                original_piece = self.board[rr][cc]
                                self.board[rr][cc] = piece
                                self.board[r][c] = None
                                if not self.is_in_check(color):
                                    self.board[r][c] = piece
                                    self.board[rr][cc] = original_piece
                                    return False
                                self.board[r][c] = piece
                                self.board[rr][cc] = original_piece
        return True

    def start(self):
        self.canvas.bind("<Button-1>", self.on_click)
        self.bind("<Control-z>", lambda event: self.undo_move())
        self.mainloop()

class Piece:
    def __init__(self, icon, color):
        self.icon = icon
        self.color = color

if __name__ == "__main__":
    game = ChessGame()
    game.start()