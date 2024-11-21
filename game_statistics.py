# game_statistics.py
import json

class Statistics:
    def __init__(self):
        self.stats = {"X": {"wins": 0, "losses": 0, "ties": 0}, 
                      "O": {"wins": 0, "losses": 0, "ties": 0}}
        self.load_stats()

    def load_stats(self):
        try:
            with open("statistics.json", "r") as f:
                self.stats = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.initialize_stats()  # Initialize with default stats

    def initialize_stats(self):
        with open("statistics.json", "w") as f:
            json.dump(self.stats, f)

    def update_score(self, player_symbol, result):
        if player_symbol not in self.stats:
            self.stats[player_symbol] = {"wins": 0, "losses": 0, "ties": 0}
        
        if result == "win":
            self.stats[player_symbol]["wins"] += 1
            self.stats["O" if player_symbol == "X" else "X"]["losses"] += 1
        elif result == "tie":
            self.stats[player_symbol]["ties"] += 1
        
        self.save_stats()

    def save_stats(self):
        with open("statistics.json", "w") as f:
            json.dump(self.stats, f)

    def get_stats(self):
        return self.stats
