from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.window import Window

class ReversePomodoroApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=20)

        Window.clearcolor = (0, 0, 0, 1)  # Start with black background

        # Welcome Screen (temporary)
        self.welcome_label = Label(text="🎯 Welcome to Reverse Pomodoro!\nThe Ultimate Unproductivity Timer!",
                                   font_size=24, halign="center", valign="middle")
        self.root.add_widget(self.welcome_label)

        Clock.schedule_once(self.setup_screen, 3)  # Show setup after 3 seconds
        return self.root

    def setup_screen(self, dt):
        self.root.clear_widgets()

        # Productivity Time Selection
        self.activity_label = Label(text="Select Productivity Minutes:", font_size=20)
        self.root.add_widget(self.activity_label)

        self.activity_spinner = Spinner(
            text="5",
            values=["5", "10", "15", "30", "60"],
            size_hint=(1, None),
            height=44
        )
        self.root.add_widget(self.activity_spinner)

        # Cycle Selection
        self.cycle_label = Label(text="Select Number of Cycles:", font_size=20)
        self.root.add_widget(self.cycle_label)

        self.cycle_spinner = Spinner(
            text="3",
            values=[str(i) for i in range(3, 11)],
            size_hint=(1, None),
            height=44
        )
        self.root.add_widget(self.cycle_spinner)

        # Confirm Button
        self.confirm_button = Button(text="Confirm Settings", size_hint=(1, None), height=50, on_press=self.confirm_settings)
        self.root.add_widget(self.confirm_button)

        # Timer Display (Hidden initially)
        self.timer_label = Label(text="00:00:00", font_size=48)
        self.status_label = Label(text="", font_size=24)

    def confirm_settings(self, instance):
        self.activity_minutes = int(self.activity_spinner.text)
        self.rest_minutes = self.activity_minutes * 5
        self.total_cycles = int(self.cycle_spinner.text)
        self.current_cycle = 1

        self.root.clear_widgets()

        self.root.add_widget(self.timer_label)
        self.root.add_widget(self.status_label)

        # Start Button
        self.start_button = Button(text="Start Reverse Pomodoro", size_hint=(1, None), height=50, on_press=self.start_timer)
        self.root.add_widget(self.start_button)

    def start_timer(self, instance):
        self.start_button.disabled = True
        self.running = True
        self.run_cycles()

    def run_cycles(self):
        if self.current_cycle <= self.total_cycles:
            self.update_phase(f"🚀 Activity Time! Cycle {self.current_cycle}", (1, 0, 0, 1))  # Red background
            self.countdown(self.activity_minutes * 60, self.start_rest_phase)
        else:
            self.finish_timer()

    def start_rest_phase(self, dt=None):
        self.update_phase(f"😎 Inactivity Time! Cycle {self.current_cycle}", (0, 0, 1, 1))  # Blue background
        self.countdown(self.rest_minutes * 60, self.next_cycle)

    def next_cycle(self, dt=None):
        self.current_cycle += 1
        self.run_cycles()

    def update_phase(self, message, color):
        self.status_label.text = message
        Window.clearcolor = color

    def countdown(self, total_seconds, callback):
        self.seconds_left = total_seconds
        self.countdown_event = Clock.schedule_interval(lambda dt: self.update_timer(callback), 1)

    def update_timer(self, callback):
        mins, secs = divmod(self.seconds_left, 60)
        self.timer_label.text = f"00:{mins:02d}:{secs:02d}"
        self.seconds_left -= 1

        if self.seconds_left < 0:
            self.countdown_event.cancel()
            callback()

    def finish_timer(self):
        Window.clearcolor = (0, 1, 0, 1)  # Green background
        self.timer_label.text = "00:00:00"
        self.status_label.text = "🎉 All cycles completed! 🎉"

if __name__ == '__main__':
    ReversePomodoroApp().run()
