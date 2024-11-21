# themes.py
from tkinter import StringVar

class Themes:
    def __init__(self, root):
        self.root = root
        self.available_themes = ["Default", "Dark", "Light"]

    def apply_theme(self, theme):
        if theme == "Dark":
            self.root.config(bg="black")
            self.root.option_add('*TButton*highlightThickness', 0)
            self.root.option_add('*TButton*background', 'grey')
            self.root.option_add('*TButton*foreground', 'white')
        elif theme == "Light":
            self.root.config(bg="white")
            self.root.option_add('*TButton*highlightThickness', 0)
            self.root.option_add('*TButton*background', 'lightgrey')
            self.root.option_add('*TButton*foreground', 'black')
        else:
            self.root.config(bg="SystemButtonFace")  # Default
