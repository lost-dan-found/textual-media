from util import get_timezone, get_weather_details, get_location_details, update_greeting

from datetime import datetime
from zoneinfo import ZoneInfo
from textual.app import App, ComposeResult
from textual.widgets import Digits, Static
from textual.containers import Horizontal, Vertical

LOCATION = "Boston"

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

    Digits {
        width: 100%;
        height: 100%;
        text-align: center;
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
        border: white;
        background: transparent;
        padding: 0;
        content-align: center middle;
    }

    #clock {
        width: 60%;
        height: 100%;
        border: white;
        background: transparent;
        padding: 0;
        content-align: center middle;
    }

    #quote {
        width: 100%;
        height: 100%;
        padding: 0 3;
    }

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ansi_color = True
        self.location_data = get_location_details(LOCATION)
        self.timezone = get_timezone(self.location_data[0],self.location_data[1])
        self.weather_data = None

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="top_row"):
                self.clock = Digits("Loading...", id="clock", classes="box")
                self.clock.border_title = "Time"
                self.clock.ALLOW_SELECT = False

                self.weather = Static("Loading…", id="weather", classes="box")
                self.weather.border_title = "Weather"
                self.weather.ALLOW_SELECT = False

                yield self.clock
                yield self.weather

            with Horizontal(id="bottom_row"):
                self.quote = Static("Loading...", id="quote", classes="box")
                self.quote.border_title = update_greeting(self.timezone)
                self.quote.ALLOW_SELECT = False
                yield self.quote

    def on_ready(self):
        self.update_all()
        self.set_interval(1, self.update_clock)
        self.set_interval(600, self.update_weather)
        self.set_interval(600, self.update_quote)

    # ---- Updaters ----

    def update_all(self):
        self.update_clock()
        self.update_weather()
        self.update_quote()

    def update_clock(self):
        now = datetime.now(self.timezone)
        time_str = now.strftime("%I:%M")
        self.clock.update(time_str)

    def update_weather(self):
            temp, weather, city = get_weather_details(self.location_data[2])
            if temp is None or weather is None or city is None:
                self.weather.update("No Weather Data")
            else:
                self.weather.update(f"{temp}° F | {weather} | {city}")

    def update_quote(self):
        self.quote.update("There comes a day in every man's life that he can no longer write another line of SAAS code. -Dan")
        self.quote.border_title = update_greeting(self.timezone)




if __name__ == "__main__":
    DashboardApp().run(inline=True)