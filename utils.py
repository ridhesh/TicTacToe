# utils.py
import random
import string

def clear_string(s):
    """ Cleans a string by filtering non-printable characters. """
    return ''.join(filter(lambda x: x in string.printable, s))

def random_string(length=10):
    """ Generates a random string of a specified length. """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def is_valid_move(board, index):
    """ Checks if a move is valid on the given board. """
    return 0 <= index < len(board) and board[index] == " "

def print_board(board):
    """ Prints the current board state in a readable format. """
    size = int(len(board) ** 0.5)  # Assuming it's a square board
    for i in range(size):
        print("|".join(board[i * size:(i + 1) * size]))
        if i < size - 1:
            print("-" * (size * 2 - 1))

def load_json(filename):
    """ Loads JSON data from a file. """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None  # Return None if the file doesn't exist or is empty/corrupted

def save_json(data, filename):
    """ Saves data to a JSON file. """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def score_player_data(players):
    """ Returns a scored representation of player data for rankings or display. """
    return sorted(players.items(), key=lambda item: (item[1]['wins'], item[1]['losses']))
