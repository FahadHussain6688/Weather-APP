import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "1ecf1e984a2e0cb108181f117f3a22a0"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Wizard")
        self.root.geometry("600x720")

        # Set initial theme
        self.style = ttk.Style()
        self.current_theme = "cosmo"
        self.style.theme_use(self.current_theme)

        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Title Label
        self.title_label = ttk.Label(
            self.main_frame,
            text="\U0001F324\ufe0f Weather Wizard",
            font=("Helvetica", 20, "bold"),
            anchor=CENTER,
            bootstyle=PRIMARY
        )
        self.title_label.pack(pady=(0, 10))

        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=X, pady=10)

        self.city_entry = ttk.Entry(
            self.header_frame,
            font=('Helvetica', 14),
            width=25,
            bootstyle=PRIMARY
        )
        self.city_entry.pack(side=LEFT, padx=5)

        self.get_btn = ttk.Button(
            self.header_frame,
            text="Get Weather",
            command=self.get_weather,
            bootstyle=(SUCCESS, OUTLINE),
            width=12
        )
        self.get_btn.pack(side=LEFT, padx=5)

        self.clear_btn = ttk.Button(
            self.header_frame,
            text="Clear",
            command=self.clear_data,
            bootstyle=(WARNING, OUTLINE),
            width=8
        )
        self.clear_btn.pack(side=LEFT, padx=5)

        # Theme Toggle
        self.theme_btn = ttk.Button(
            self.main_frame,
            text=f"Theme: {self.current_theme.title()}",
            command=self.toggle_theme,
            bootstyle=(INFO, OUTLINE),
            width=18
        )
        self.theme_btn.pack(pady=10)

        # Current Weather
        self.weather_frame = ttk.Labelframe(
            self.main_frame,
            text="Current Weather",
            bootstyle=PRIMARY
        )
        self.weather_frame.pack(fill=X, pady=10)

        self.icon_label = ttk.Label(self.weather_frame)
        self.icon_label.pack(pady=5)

        self.result_frame = ttk.Frame(self.weather_frame)
        self.result_frame.pack(pady=10)

        self.result_label = ttk.Label(
            self.result_frame,
            font=('Helvetica', 12),
            wraplength=500,
            anchor=CENTER,
            justify=CENTER
        )
        self.result_label.pack()

        # Forecast
        self.forecast_frame = ttk.Labelframe(
            self.main_frame,
            text="5-Day Forecast",
            bootstyle=INFO
        )
        self.forecast_frame.pack(fill=BOTH, expand=True)

        self.forecast_text = ttk.Text(
            self.forecast_frame,
            height=8,
            font=('Helvetica', 10),
            wrap=WORD,
            state=DISABLED,
            relief=RIDGE,
            borderwidth=2
        )
        self.forecast_text.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Footer
        self.footer_label = ttk.Label(
            self.main_frame,
            text="Created by Fahad · Powered by OpenWeatherMap",
            font=("Helvetica", 9),
            anchor=CENTER
        )
        self.footer_label.pack(side=BOTTOM, pady=5)

    def toggle_theme(self):
        self.current_theme = "darkly" if self.current_theme == "cosmo" else "cosmo"
        self.style.theme_use(self.current_theme)
        self.theme_btn.config(text=f"Theme: {self.current_theme.title()}")

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        if city.strip().lower() == "ryk":
            messagebox.showinfo("Weather Info", "Bahir jaa kar dekh lo")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                temp = data["main"]["temp"]
                condition = data["weather"][0]["description"].title()
                humidity = data["main"]["humidity"]
                icon_code = data["weather"][0]["icon"]

                self.show_weather_icon(icon_code)

                result_text = (f"\U0001F4CD {city}\n"
                                f"\U0001F321 Temperature: {temp}°C\n"
                                f"\U0001F308 Condition: {condition}\n"
                                f"\U0001F4A7 Humidity: {humidity}%")
                self.result_label.config(text=result_text)

                self.get_forecast(city)
            else:
                message = data.get("message", "City not found.")
                messagebox.showerror("Error", message)

        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Failed to connect to weather service.")

    def show_weather_icon(self, icon_code):
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            icon_response = requests.get(icon_url)
            if icon_response.status_code == 200:
                icon_img = Image.open(BytesIO(icon_response.content))
                icon_img = icon_img.resize((80, 80), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_img)
                self.icon_label.config(image=icon_photo)
                self.icon_label.image = icon_photo
        except:
            self.icon_label.config(image='')
            self.icon_label.image = None

    def get_forecast(self, city):
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        try:
            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()

            if forecast_response.status_code == 200:
                self.forecast_text.config(state=NORMAL)
                self.forecast_text.delete(1.0, END)

                forecast_text = ""
                for i in range(0, len(forecast_data["list"]), 8):
                    date_time = forecast_data["list"][i]["dt_txt"]
                    temp = forecast_data["list"][i]["main"]["temp"]
                    condition = forecast_data["list"][i]["weather"][0]["description"].title()
                    forecast_text += f"\U0001F4C5 {date_time.split()[0]}: {temp}°C | {condition}\n\n"

                self.forecast_text.insert(END, forecast_text)
                self.forecast_text.config(state=DISABLED)
        except:
            messagebox.showerror("Error", "Failed to fetch forecast data.")

    def clear_data(self):
        self.city_entry.delete(0, END)
        self.result_label.config(text="")
        self.forecast_text.config(state=NORMAL)
        self.forecast_text.delete(1.0, END)
        self.forecast_text.config(state=DISABLED)
        self.icon_label.config(image='')
        self.icon_label.image = None

if __name__ == "__main__":
    root = ttk.Window()
    app = WeatherApp(root)
    root.mainloop()
