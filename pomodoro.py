import time
import threading
import winsound
import tkinter as tk
from tkinter import messagebox

POMODORO_DURATION = 25 * 60  # 25 minuti in secondi
PAUSA_DURATION = 5 * 60      # 5 minuti in secondi
FREQUENZA_SUONO = 1000       # Frequenza del beep in Hz
DURATA_SUONO = 1000          # Durata del beep in ms

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x150")
        self.root.resizable(False, False)

        self.is_running = False
        self.is_pomodoro = True
        self.time_left = POMODORO_DURATION

        self.label = tk.Label(root, text="25:00", font=("Helvetica", 48))
        self.label.pack(pady=10)

        self.status_label = tk.Label(root, text="Pomodoro", font=("Helvetica", 14))
        self.status_label.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.timer_thread = None

    def beep(self):
        winsound.Beep(FREQUENZA_SUONO, DURATA_SUONO)

    def update_label(self):
        mins, secs = divmod(self.time_left, 60)
        self.label.config(text=f"{mins:02d}:{secs:02d}")

    def timer_countdown(self):
        while self.is_running and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1
            self.root.after(0, self.update_label())
        if self.is_running and self.time_left == 0:
            self.beep()
            if self.is_pomodoro:
                messagebox.showinfo("Pomodoro", "Pomodoro terminato! Ora pausa di 5 minuti.")
                self.is_pomodoro = False
                self.time_left = PAUSA_DURATION
                self.status_label.config(text="Pausa")
            else:
                messagebox.showinfo("Pausa", "Pausa terminata! Torna al lavoro.")
                self.is_pomodoro = True
                self.time_left = POMODORO_DURATION
                self.status_label.config(text="Pomodoro")
            self.root.after(0, self.update_label())
            self.timer_countdown()  # Ricomincia automaticamente

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
            self.timer_thread = threading.Thread(target=self.timer_countdown)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)

    def reset_timer(self):
        self.is_running = False
        self.is_pomodoro = True
        self.time_left = POMODORO_DURATION
        self.update_label()
        self.status_label.config(text="Pomodoro")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
