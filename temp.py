import requests


api_key = 'b1693ed7ad181ad79817cc99d0523aa3'  # Replace with your actual API key
base_url = 'https://api.openweathermap.org/data/2.5/weather'
    
params = {
        'q': 'Karkala',
        'appid': api_key,
}

response = requests.get(base_url, params=params)
data = response.json()

desc = data['weather'][0]['description']
temp = data['main']['temp']
name = data['name']
humidity = data['main']['humidity']
sea_level = data['main']['sea_level']