# ai.py
import math
import random
from game import TicTacToeGame

class TicTacToeAI:
    def __init__(self, game):
        self.game = game

    def get_move(self, difficulty):
        if difficulty == 'easy':
            return self.random_move()
        elif difficulty == 'medium':
            return self.medium_move()
        elif difficulty == 'hard':
            return self.minimax(0, "O")[1]  # Change: get only the best move

    def random_move(self):
        available_moves = [i for i in range(len(self.game.board)) if self.game.board[i] == " "]
        if available_moves:
            return divmod(random.choice(available_moves), self.game.board_size)
        return None

    def medium_move(self):
        # Attempt to block opponent from winning if possible
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.board[i * self.game.board_size + j] == " ":
                    self.game.board[i * self.game.board_size + j] = "X"  # Assuming "X" is the player
                    if self.game.check_winner():
                        return (i, j)
                    self.game.board[i * self.game.board_size + j] = " "  # Undo move

        return self.random_move()  # If nothing can be blocked, choose randomly

    def minimax(self, depth, player):
        if self.game.check_winner():
            if self.game.winner == "O":
                return 1, None  # AI wins
            elif self.game.winner == "X":
                return -1, None  # Player wins
            else:
                return 0, None  # Tie

        best_move = None
        if player == "O":
            best_value = -math.inf
            for i in range(self.game.board_size):
                for j in range(self.game.board_size):
                    index = i * self.game.board_size + j
                    if self.game.board[index] == " ":
                        self.game.board[index] = player
                        score, _ = self.minimax(depth + 1, "X")  # Check for player X's best move
                        self.game.board[index] = " "  # Undo move
                        if score > best_value:
                            best_value = score
                            best_move = (i, j)
            return best_value, best_move  # Return best score and move
        else:
            best_value = math.inf
            for i in range(self.game.board_size):
                for j in range(self.game.board_size):
                    index = i * self.game.board_size + j
                    if self.game.board[index] == " ":
                        self.game.board[index] = player
                        score, _ = self.minimax(depth + 1, "O")  # Check for AI's best move
                        self.game.board[index] = " "  # Undo move
                        if score < best_value:
                            best_value = score
                            best_move = (i, j)
            return best_value, best_move  # Return best score and move
