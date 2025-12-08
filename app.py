from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import Digits, Static
from textual.containers import Horizontal, Vertical


class DashboardApp(App):
    CSS = """
    Screen {
        background: transparent;
        align: center middle;
    }

    .box {
        border: white;
        background: transparent;
        content-align: center middle;
        padding: 1 1;
    }

    #top_row {
        width: 100%;
        height: 50%;
    }

    #bottom_row {
        width: 100%;
        height: 50%;
    }

    #weather {
        width: 40%;
        height: 100%;
    }

    #greeting {
        width: 100%;
        height: 100%;
    }

    #clock {
        width: 60%;
        height: 100%;
        border: white;
        background: transparent;
        padding: 0;
        content-align: center middle;
    }

    Digits {
        width: 100%;
        height: 100%;
        text-align: center;
    }

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ansi_color = True

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="top_row"):
                self.clock = Digits("", id="clock", classes="box")
                self.clock.border_title = "Local Time"
                self.clock.ALLOW_SELECT = False

                self.weather = Static("Loading…", id="weather", classes="box")
                self.weather.border_title = "Weather"

                yield self.clock
                yield self.weather

            with Horizontal(id="bottom_row"):
                self.greeting = Static("", id="greeting", classes="box")
                self.greeting.border_title = "Welcome"
                yield self.greeting

    def on_ready(self) -> None:
        self.update_all()
        self.set_interval(1, self.update_clock)
        self.set_interval(60, self.update_weather)
        self.set_interval(30, self.update_greeting)

    # ---- Updaters ----

    def update_all(self) -> None:
        self.update_clock()
        self.update_weather()
        self.update_greeting()

    def update_clock(self) -> None:
        now = datetime.now()
        self.clock.update(f"{now:%T}")

    def update_weather(self) -> None:
        # Placeholder – replace with real API later
        self.weather.update("🌤 72°F / 22°C\nPartly Cloudy")

    def update_greeting(self) -> None:
        hour = datetime.now().hour
        if hour < 12:
            text = "Good Morning ☀️"
        elif hour < 18:
            text = "Good Afternoon 🌤"
        else:
            text = "Good Evening 🌙"
        self.greeting.update(text)


if __name__ == "__main__":
    DashboardApp().run(inline=True)
