import tkinter as tk
import os

# CONFIGURATION
# Professionals use constants for "magic numbers" so they are easy to change later
THRESHOLD_CLICKS = 10    # The 'x' amount of clicks
BASE_MULTIPLIER = 1      # Initial points per click
BOOSTED_MULTIPLIER = 2   # Points per click after threshold
CURRENCY_COST = 50       # The 'y' amount to spend
CURRENCY_REWARD = 100    # The '2y' amount to gain
HIGHSCORE_FILE = "highscore.txt"

class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Clicker: The Glitch")
        self.root.geometry("400x300")

        # Game State Variables
        self.score = 0
        self.click_count = 0
        self.high_score = self.load_high_score()

        # Initialize UI
        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        """Creates and places all visual elements."""
        # High Score Display
        self.lbl_highscore = tk.Label(self.root, text=f"High Score: {self.high_score}", fg="gray")
        self.lbl_highscore.pack(pady=5)

        # Main Score Display
        self.lbl_score = tk.Label(self.root, text="Score: 0", font=("Helvetica", 24, "bold"))
        self.lbl_score.pack(pady=20)

        # Click Info
        self.lbl_status = tk.Label(self.root, text="Level: Beginner (1 pt/click)", fg="blue")
        self.lbl_status.pack()

        # The Main Click Button
        self.btn_click = tk.Button(self.root, text="CLICK ME", command=self.on_click, 
                                   bg="#dddddd", height=2, width=15)
        self.btn_click.pack(pady=10)

        # The "Broken" Exchange Feature
        self.btn_exchange = tk.Button(self.root, text=f"Exchange {CURRENCY_COST} for {CURRENCY_REWARD}", 
                                      command=self.exploit_currency, bg="gold")
        self.btn_exchange.pack(pady=20)

    def on_click(self):
        """Handles the main clicking logic."""
        self.click_count += 1
        
        # Logic: After x clicks, return 2x points (or double multiplier)
        if self.click_count >= THRESHOLD_CLICKS:
            points_to_add = BOOSTED_MULTIPLIER
            self.lbl_status.config(text="Level: BOOSTED (2 pts/click)!", fg="red")
        else:
            points_to_add = BASE_MULTIPLIER

        self.score += points_to_add
        self.check_high_score()
        self.update_ui()

    def exploit_currency(self):
        """The 'broken' feature requested: Buy money with less money."""
        if self.score >= CURRENCY_COST:
            self.score -= CURRENCY_COST  # Pay y
            self.score += CURRENCY_REWARD # Gain 2y
            self.check_high_score()
            self.update_ui()
        else:
            # Visual feedback if they can't afford it
            original_text = self.lbl_score.cget("text")
            self.lbl_score.config(text="Not enough funds!", fg="red")
            # Schedule a reset of the text after 1000ms (1 second)
            self.root.after(1000, self.update_ui)

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def update_ui(self):
        """Refreshes the labels to match current variables."""
        self.lbl_score.config(text=f"Score: {self.score}", fg="black")
        self.lbl_highscore.config(text=f"High Score: {self.high_score}")
        
        # Optional: Disable exchange button if they can't afford it
        if self.score >= CURRENCY_COST:
            self.btn_exchange.config(state="normal")
        else:
            self.btn_exchange.config(state="disabled")

    def load_high_score(self):
        """Reads highscore from file. Returns 0 if file doesn't exist."""
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    return int(f.read())
            except:
                return 0
        return 0

    def save_high_score(self):
        """Writes the new highscore to the file."""
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.high_score))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerGame(root)
    root.mainloop()