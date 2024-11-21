# game.py
from player import Player

class TicTacToeGame:
    def __init__(self, board_size=3):
        self.board_size = board_size
        self.reset_game()
        self.current_player_symbol = "X"  # Start with Player X
        self.players = {
            "X": None,
            "O": None
        }

    def reset_game(self):
        self.board = [" " for _ in range(self.board_size ** 2)]
        self.game_history = []
        self.winner = None

    def set_players(self, player1, player2):
        self.players["X"] = Player(player1, "X")
        self.players["O"] = Player(player2, "O")

    def switch_player(self):
        self.current_player_symbol = "O" if self.current_player_symbol == "X" else "X"

    def make_move(self, i, j):
        index = i * self.board_size + j
        if self.board[index] == " " and self.winner is None:
            self.board[index] = self.current_player_symbol
            self.game_history.append((i, j, self.current_player_symbol))

            if self.check_winner():
                return self.winner
            elif " " not in self.board:
                return "TIE"
            self.switch_player()
        return None

    def check_winner(self):
        winning_combinations = []

        # Rows
        for i in range(self.board_size):
            winning_combinations.append([i * self.board_size + j for j in range(self.board_size)])

        # Columns
        for j in range(self.board_size):
            winning_combinations.append([i * self.board_size + j for i in range(self.board_size)])

        # Diagonals
        winning_combinations.append([i * self.board_size + i for i in range(self.board_size)])  # \
        winning_combinations.append([i * self.board_size + (self.board_size - 1 - i) for i in range(self.board_size)])  # /

        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                self.winner = self.board[combo[0]]
                return True

        return False

    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.players[self.current_player_symbol]
