# player.py
class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return f"Player(name={self.name}, symbol={self.symbol})"
