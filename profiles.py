# profiles.py
import json

class Profile:
    def __init__(self, name, wins=0, losses=0, ties=0):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.ties = ties

    def to_dict(self):
        return {
            "name": self.name,
            "wins": self.wins,
            "losses": self.losses,
            "ties": self.ties
        }

class ProfileManager:
    def __init__(self):
        self.profiles = {}
        self.load_profiles()

    def load_profiles(self):
        try:
            with open("profiles.json", "r") as f:
                data = json.load(f)
                self.profiles = {name: Profile(**info) for name, info in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            self.profiles = {}
            self.initialize_profiles()  # Create default profiles

    def initialize_profiles(self):
        default_profiles = {
            "Player1": {"name": "Player1", "wins": 0, "losses": 0, "ties": 0},
            "Player2": {"name": "Player2", "wins": 0, "losses": 0, "ties": 0},
        }
        with open("profiles.json", "w") as f:
            json.dump(default_profiles, f)

    def save_profiles(self):
        with open("profiles.json", "w") as f:
            json.dump({name: profile.to_dict() for name, profile in self.profiles.items()}, f)

    def update_profile(self, name, result):
        if name in self.profiles:
            profile = self.profiles[name]
            if result == "win":
                profile.wins += 1
            elif result == "loss":
                profile.losses += 1
            elif result == "tie":
                profile.ties += 1
            self.save_profiles()
