# WeatherApp

A simple Python GUI application that fetches real-time weather data using the OpenWeatherMap API.

## Features
- Enter a city name to get:
  - Temperature
  - Weather condition
  - Humidity
- GUI built with Tkinter
- Error handling for invalid inputs

## Setup

1. Install dependencies:
   ```bash
   pip install requests
   ```

2. Get your API key from [OpenWeatherMap](https://openweathermap.org/api) and replace it in `main.py`.

3. Run the app:
   ```bash
   python main.py
   ```

## Notes
- All temperatures are in Celsius (`units=metric`)
