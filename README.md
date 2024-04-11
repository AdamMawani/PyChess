# PyChess
PyChess is a Python program designed to create a fully functional chess game with a graphical user interface (GUI) using the Tkinter library. It allows users to play the classic game of chess against each other on a computer.

## Features
1. **Graphical User Interface**: Utilizes Tkinter to provide an intuitive and visually appealing interface for playing chess.
2. **Classic Chess Rules**: Follows the standard rules of chess, including piece movement, captures, check, and checkmate.
3. **Turn-Based Gameplay**: Implements a turn-based system where players take alternating moves.
4. **Legal Move Validation**: Validates the legality of moves according to the rules of chess, preventing illegal moves from being made.
5. **Check and Checkmate Detection**: Automatically detects when a player's king is in check and when a player is in checkmate, ending the game accordingly.
6. **Promotion**: Supports pawn promotion when a pawn reaches the opposite end of the board.
7. **Castling**: Implements castling, allowing players to perform this special move if the conditions are met.
8. **En Passant**: Handles the en passant rule, allowing players to capture a pawn that has moved two squares forward from its starting position.
9. **Draw Detection**: Detects stalemate and insufficient material situations, offering a draw option to the players.
10. **Game Log**: Keeps track of the moves made during the game, displaying them in a log for reference.
11. **Save and Load Game**: Allows players to save the current game state to a file and load it later to resume play.

## How to Use
1. **Installation**:
   - Ensure you have Python installed on your system.
   - Install the required libraries using pip:
     ```
     pip install tk
     ```

2. **Run the Program**:
   - Execute the `chess_game_gui.py` file using Python:
     ```
     python chess_game_gui.py
     ```

3. **Gameplay**:
   - Upon launching the program, the chessboard GUI will be displayed.
   - Click on a piece to select it, then click on a valid square to move the piece.
   - Follow the standard rules of chess to play the game.
   - The game log will display the moves made by both players.

4. **Save and Load Game**:
   - To save the game, click on the "Save Game" button and choose a file name.
   - To load a saved game, click on the "Load Game" button and select the saved file.

## Requirements
- Python 3.x
- Tkinter library