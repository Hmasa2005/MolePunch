import tkinter as tk
import random

# ゲーム設定
GAME_TIME = 30  # ゲーム時間（秒）
MOLE_INTERVAL = 500  # モグラ出現間隔（ミリ秒）

class WhackAMoleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("モグラ叩きゲーム")
        self.score = 0
        self.time_left = GAME_TIME
        self.current_mole = None

        self.label_score = tk.Label(root, text="スコア: 0", font=("Arial", 16))
        self.label_score.pack()

        self.label_timer = tk.Label(root, text="残り時間: 30", font=("Arial", 16))
        self.label_timer.pack()

        self.canvas = tk.Canvas(root, width=300, height=300, bg="lightgreen")
        self.canvas.pack()

        self.holes = []
        for y in range(3):
            for x in range(3):
                hole = self.canvas.create_oval(20 + x*90, 20 + y*90, 100 + x*90, 100 + y*90, fill="brown")
                self.holes.append(hole)

        self.canvas.bind("<Button-1>", self.hit)

        self.root.after(1000, self.countdown)
        self.spawn_mole()

    def countdown(self):
        self.time_left -= 1
        self.label_timer.config(text=f"残り時間: {self.time_left}")
        if self.time_left > 0:
            self.root.after(1000, self.countdown)
        else:
            self.end_game()

    def spawn_mole(self):
        if self.time_left <= 0:
            return

        if self.current_mole:
            self.canvas.itemconfig(self.current_mole, fill="brown")

        self.current_mole = random.choice(self.holes)
        self.canvas.itemconfig(self.current_mole, fill="black")

        self.root.after(MOLE_INTERVAL, self.spawn_mole)

    def hit(self, event):
        if self.time_left <= 0:
            return

        clicked = self.canvas.find_closest(event.x, event.y)[0]
        if clicked == self.current_mole:
            self.score += 1
            self.label_score.config(text=f"スコア: {self.score}")
            self.canvas.itemconfig(self.current_mole, fill="brown")
            self.current_mole = None

    def end_game(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.create_text(150, 150, text="ゲーム終了！", font=("Arial", 24), fill="red")

# 実行
if __name__ == "__main__":
    root = tk.Tk()
    game = WhackAMoleGame(root)
    root.mainloop()
