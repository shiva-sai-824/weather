from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    if request.method == 'POST':
        city = request.form['city']
        Api_Key = "2606f769271b8d545fe3458b2b72ed9f"  # Your API Key here
        final_URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Api_Key}"
        
        try:
            result = requests.get(final_URL)
            data = result.json()
            
            if data['cod'] == 200:
                temperature = data['main']['temp']
                coordinate_lon = data['coord']['lon']
                coordinate_lat = data['coord']['lat']
                
                # Convert temperature from Kelvin to Celsius
                temperature_celsius = temperature - 273.15
                
                weather_info = f"Temperature: {temperature_celsius:.2f}°C<br>Coordinates: ({coordinate_lat}, {coordinate_lon})"
            else:
                weather_info = "City not found. Please enter a valid city name."
        except Exception as e:
            weather_info = "Could not fetch data. Please check your internet connection and try again."
    
    return render_template_string("""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Weather App</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
          }
          .container {
            text-align: center;
          }
          .weather-form {
            margin-bottom: 20px;
          }
          .weather-info {
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: 0 auto;
          }
          .weather-info p {
            font-size: 18px;
            line-height: 1.6;
            text-align: center;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Weather App</h1>
          <form class="weather-form" method="post">
            <input type="text" name="city" placeholder="Enter Your City" required>
            <button type="submit">Fetch Weather</button>
          </form>
          <div class="weather-info">
            {% if weather_info %}
              <p>{{ weather_info|safe }}</p>
            {% endif %}
          </div>
        </div>
      </body>
    </html>
    """, weather_info=weather_info)

if __name__ == '__main__':
    app.run(debug=True)
