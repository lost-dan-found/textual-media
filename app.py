from datetime import datetime
from zoneinfo import ZoneInfo
from textual.app import App, ComposeResult
from textual.widgets import Digits, Static, Header, Footer
from textual.containers import Horizontal, Vertical
import requests
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

LAT = 42.36     # Boston latitude
LON = -71.06    # Boston longitude

# Timezone for clock
TIMEZONE = "America/New_York"


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
        border: white;
        background: transparent;
        padding: 0;
        content-align: center middle;
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
        self.weather_data = None

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
        self.set_interval(1, self.update_weather)  # update weather every 10 min
        self.set_interval(600, self.update_greeting)

    # ---- Updaters ----

    def update_all(self) -> None:
        self.update_clock()
        self.update_weather()
        self.update_greeting()

    def update_clock(self) -> None:
        now = datetime.now(ZoneInfo(TIMEZONE))
        time_str = now.strftime("%I:%M")
        self.clock.update(time_str)

    def map_weather_code(self, code: int) -> str:
        """Map Open-Meteo weather codes to emojis."""
        mapping = {
            0: "Clear",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return mapping.get(code, "❓ Unknown")


    def update_weather(self):

        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        cw = data.get("current_weather", {})
        temp = cw.get("temperature")  # in Celsius by default
        # convert to Fahrenheit if you like
        temp_f = int(temp * 9/5 + 32) if temp is not None else None
        desc = cw.get("weathercode")  # you might need a mapping from weathercode → text/emoji
        # then update self.weather accordingly
        emoji = self.map_weather_code(desc)
        self.weather.update(f"{temp_f}° F | {emoji}")

    def update_greeting(self) -> None:
        hour = datetime.now(ZoneInfo(TIMEZONE)).hour
        if hour < 12:
            text = "Good Morning ☀️"
        elif hour < 18:
            text = "Good Afternoon 🌤"
        else:
            text = "Good Evening 🌙"
        self.greeting.update(text)


if __name__ == "__main__":
    DashboardApp().run(inline=True)