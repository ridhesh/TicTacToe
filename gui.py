# gui.py
import tkinter as tk
from tkinter import messagebox, StringVar
from game import TicTacToeGame
from ai import TicTacToeAI
from game_statistics import Statistics
from profiles import ProfileManager

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Dynamic Tic Tac Toe")
        self.window.geometry("800x600")
        self.window.config(bg="#F0F0F0")
        
        self.current_theme = self.default_theme()  # Initialize current_theme here

        # Initialize game, AI, stats, and profiles
        self.game = None
        self.ai = None
        self.stats = Statistics()
        self.profile_manager = ProfileManager()
        
        # Initialize the frame attribute
        self.frame = None
        
        self.create_start_screen()

    def default_theme(self):
        return {
            'bg': "#F0F0F0",
            'btn_bg': "#FFFFFF",
            'btn_fg': "black",
            'btn_active_bg': "#FFC107",
            'btn_winner_bg': "#3F51B5",
            'game_over_bg': "#F44336"
        }

    def create_start_screen(self):
        title_label = tk.Label(
            self.window, text="Welcome to Tic Tac Toe!", font=('Arial', 30, 'bold'), bg=self.current_theme['bg'])
        title_label.pack(pady=20)

        tk.Label(self.window, text="Select Board Size (3 to 10):", font=('Arial', 14), bg=self.current_theme['bg']).pack(pady=10)
        self.board_size_input = tk.Entry(self.window, font=('Arial', 14))
        self.board_size_input.pack(pady=10)

        tk.Button(self.window, text="Start Game", command=self.start_game, font=('Arial', 14),
                  bg="#4CAF50", fg="white").pack(pady=10)

        # Theme Selection
        theme_label = tk.Label(self.window, text="Select Theme:", font=('Arial', 14), bg=self.current_theme['bg'])
        theme_label.pack(pady=10)

        self.theme_var = StringVar(value="Default")
        themes = [
            ("Default", self.default_theme()),
            ("Dark", self.dark_theme()),
            ("Light", self.light_theme())
        ]

        # Create a frame to house the Radiobuttons
        theme_frame = tk.Frame(self.window, bg=self.current_theme['bg'])  # Frame for better styling
        theme_frame.pack(pady=5)

        for theme_name, theme in themes:
            rb = tk.Radiobutton(theme_frame, text=theme_name, variable=self.theme_var,
                                value=theme_name, command=lambda t=theme: self.change_theme(t),
                                bg=self.current_theme['bg'], fg=self.current_theme['btn_fg'])  # Correct color handling
            rb.pack(anchor='w')

    def change_theme(self, theme):
        self.current_theme = theme
        self.window.config(bg=self.current_theme['bg'])
        for widget in self.window.winfo_children():
            widget.config(bg=self.current_theme['bg'])

    def dark_theme(self):
        return {
            'bg': "#333333",
            'btn_bg': "#555555",
            'btn_fg': "white",
            'btn_active_bg': "#777777",
            'btn_winner_bg': "#BB86FC",
            'game_over_bg': "#FF3D00"
        }

    def light_theme(self):
        return {
            'bg': "#FFFFFF",
            'btn_bg': "#FFDDC1",
            'btn_fg': "black",
            'btn_active_bg': "#FFC107",
            'btn_winner_bg': "#4CAF50",
            'game_over_bg': "#F44336"
        }

    def start_game(self):
        try:
            board_size = int(self.board_size_input.get())
            if board_size < 3 or board_size > 10:
                raise ValueError("Invalid board size.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer between 3 and 10 for board size.")
            return

        self.game = TicTacToeGame(board_size)
        self.ai = TicTacToeAI(self.game)
        self.create_board_buttons()
        self.update_statistics()
        self.moves_history = []
        self.create_moves_history()

    def create_moves_history(self):
        self.history_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        self.history_frame.pack(pady=10)

        tk.Label(self.history_frame, text="Moves History:", font=('Arial', 14), bg=self.current_theme['bg']).pack()

        self.moves_listbox = tk.Listbox(self.history_frame, width=50, height=10, font=('Arial', 12))
        self.moves_listbox.pack(pady=5)

    def create_board_buttons(self):
        self.clear_frame()  # Safely call clear_frame after frame has been initialized
        self.frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        self.frame.pack()

        self.buttons = []
        for i in range(self.game.board_size):
            row = []
            for j in range(self.game.board_size):
                btn = tk.Button(self.frame, text=" ", font=('Arial', 24), width=5, height=2,
                                command=lambda i=i, j=j: self.make_move(i, j),
                                activebackground=self.current_theme['btn_active_bg'], bg=self.current_theme['btn_bg'])
                btn.grid(row=i, column=j, sticky='nsew')
                row.append(btn)
            self.buttons.append(row)

        for i in range(self.game.board_size):
            self.frame.grid_rowconfigure(i, weight=1)
            self.frame.grid_columnconfigure(i, weight=1)

    def make_move(self, i, j):
        winner = self.game.make_move(i, j)
        move_description = f"{self.game.current_player_symbol} makes move at ({i + 1}, {j + 1})"
        self.moves_listbox.insert(tk.END, move_description)
        self.buttons[i][j].config(text=self.game.current_player_symbol, state=tk.DISABLED,
                                   bg=self.current_theme['btn_winner_bg'], fg="white")

        if winner is not None:  # Check if we have a winner
            self.end_game(f"{winner} wins!")
            if self.game.winner in self.game.players:  # Ensure winner is in players
                self.profile_manager.update_profile(self.game.players[self.game.winner].name, "win")
        elif winner == "TIE":
            self.end_game("It's a tie!")
        else:
            self.ai_move()

    def ai_move(self):
        move = self.ai.get_move("hard")  # Implement AI move
        if move:
            i, j = move
            if self.game.make_move(i, j):
                self.buttons[i][j].config(text=self.game.current_player_symbol, state=tk.DISABLED,
                                           bg=self.current_theme['btn_winner_bg'], fg="white")
                move_description = f"{self.game.current_player_symbol} (AI) makes move at ({i + 1}, {j + 1})"
                self.moves_listbox.insert(tk.END, move_description)
                if self.game.check_winner():
                    self.end_game(f"{self.game.current_player_symbol} wins!")

    def end_game(self, message):
        for button in self.buttons:
            for b in button:
                b.config(state=tk.DISABLED, bg=self.current_theme['game_over_bg'])
        messagebox.showinfo("Game Over", message)

    def clear_frame(self):
        if self.frame:  # Check if frame is initialized
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.pack_forget()

    def update_statistics(self):
        stats = self.stats.get_stats()
        stats_text = f"X Wins: {stats['X']['wins']} | O Wins: {stats['O']['wins']} | Ties: {stats['X']['ties']}"
        if hasattr(self, 'stats_label'):
            self.stats_label.config(text=stats_text)
        else:
            self.stats_label = tk.Label(self.window, text=stats_text, font=('Arial', 14), bg=self.current_theme['bg'])
            self.stats_label.pack(pady=10)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = TicTacToeGUI()
    app.run()
