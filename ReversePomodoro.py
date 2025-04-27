import tkinter as tk
import time
from threading import Thread

class ReversePomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reverse Pomodoro Timer 🎯")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.running = False

        # Default values (will be updated by user)
        self.activity_minutes = 5
        self.rest_minutes = 25
        self.total_cycles = 3
        self.cycle = 1

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_widgets()
        self.welcome_label = tk.Label(
            self.root,
            text="🎯 Welcome to the Reverse Pomodoro App 🎯\nThe Ultimate Unproductivity Timer!",
            font=("Helvetica", 18),
            justify="center"
        )
        self.welcome_label.pack(expand=True)
        
        # After 3 seconds, move to setup screen
        self.root.after(3000, self.create_setup_screen)

    def create_setup_screen(self):
        self.clear_widgets()

        # Productivity Time Selection
        tk.Label(self.root, text="Select Productivity Time (minutes):", font=("Helvetica", 14)).pack(pady=10)
        self.activity_var = tk.StringVar(value="5")
        activity_options = ["5", "10", "15", "30", "60"]
        self.activity_menu = tk.OptionMenu(self.root, self.activity_var, *activity_options, command=self.update_rest_time)
        self.activity_menu.config(font=("Helvetica", 12))
        self.activity_menu.pack()

        # Cycle Count Selection
        tk.Label(self.root, text="Select Number of Cycles:", font=("Helvetica", 14)).pack(pady=10)
        self.cycle_var = tk.StringVar(value="3")
        cycle_options = [str(i) for i in range(3, 11)]
        self.cycle_menu = tk.OptionMenu(self.root, self.cycle_var, *cycle_options)
        self.cycle_menu.config(font=("Helvetica", 12))
        self.cycle_menu.pack()

        # Info Label
        self.info_label = tk.Label(self.root, text="", font=("Helvetica", 12), fg="green")
        self.info_label.pack(pady=15)

        # Confirm Button
        self.confirm_button = tk.Button(self.root, text="Confirm Settings", font=("Helvetica", 14), command=self.confirm_settings)
        self.confirm_button.pack(pady=10)

        # Timer Widgets (hidden initially)
        self.timer_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 48), fg="white", bg="black")
        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 20))
        self.start_button = tk.Button(self.root, text="Start Reverse Pomodoro", font=("Helvetica", 16), command=self.start_timer)
        self.cycle_label = tk.Label(self.root, text="", font=("Helvetica", 14))

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def update_rest_time(self, selected_activity):
        minutes = int(selected_activity)
        rest = minutes * 5
        self.info_label.config(text=f"Got it! For {minutes} minutes, you'll have {rest} minutes of inactivity.")

    def confirm_settings(self):
        self.activity_minutes = int(self.activity_var.get())
        self.rest_minutes = self.activity_minutes * 5
        self.total_cycles = int(self.cycle_var.get())
        self.info_label.config(text=f"OK, let's get started! 🚀")
        self.show_timer_screen()

    def show_timer_screen(self):
        self.clear_widgets()

        self.timer_label.pack(pady=20)
        self.status_label.pack(pady=10)
        self.start_button.pack(pady=20)
        self.cycle_label.pack()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_button.config(state="disabled")
            t = Thread(target=self.run_cycles)
            t.start()

    def run_cycles(self):
        while self.cycle <= self.total_cycles:
            # Activity Phase
            self.update_status(f"🚀 Activity Time! Cycle {self.cycle}", "red")
            self.countdown(self.activity_minutes * 60)

            # Rest Phase
            self.update_status(f"😎 Inactivity Time! Cycle {self.cycle}", "blue")
            self.countdown(self.rest_minutes * 60)

            self.cycle += 1
            self.update_cycle_display()

        # Finished all cycles
        self.show_finished_message()

    def update_status(self, message, color):
        self.status_label.config(text=message)
        self.root.config(bg=color)
        self.timer_label.config(bg=color)

    def update_cycle_display(self):
        if self.cycle <= self.total_cycles:
            self.cycle_label.config(text=f"Cycle {self.cycle} of {self.total_cycles}")

    def countdown(self, seconds):
        while seconds >= 0 and self.running:
            mins, secs = divmod(seconds, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            self.timer_label.config(text=f"00:{time_format}")
            time.sleep(1)
            seconds -= 1

    def show_finished_message(self):
        self.running = False
        self.status_label.config(text="🎉 All cycles completed! 🎉")
        self.timer_label.config(text="00:00:00")
        self.cycle_label.config(text=f"Total {self.total_cycles} cycles done ✅")
        self.start_button.config(state="disabled")

# Launch the app
root = tk.Tk()
app = ReversePomodoroApp(root)
root.mainloop()
