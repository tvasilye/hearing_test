import tkinter as tk
from tkinter import messagebox

class HearingTestApp:
    def __init__(self, master):
        self.master = master
        master.title("Hearing Test")
        master.geometry("400x300")

        self.label = tk.Label(master, text="Take a hearing-test! Click 'Play Sound' to start the test!")
        self.label.pack(pady=20)

        self.play_button = tk.Button(master, text="Play Sound", command=self.play_sound)
        self.play_button.pack(pady=10)

        self.hear_button = tk.Button(master, text="I can hear a sound", command=self.start_test, state=tk.DISABLED)
        self.hear_button.pack(pady=10)

        self.yes_button = tk.Button(master, text="Yes", command=self.record_response, state=tk.DISABLED)
        self.yes_button.pack(pady=10)

        self.frequencies = [125, 250, 500, 1000, 2000, 4000, 8000]
        self.responses = []
        self.current_frequency = 0

    def play_sound(self):
        # Hier Code zum Abspielen des Sounds einfügen
        self.hear_button.config(state=tk.NORMAL)

    def start_test(self):
        messagebox.showinfo("Test Started", "The test will now start. Click 'Yes' every time you hear a sound.")
        self.play_button.config(state=tk.DISABLED)
