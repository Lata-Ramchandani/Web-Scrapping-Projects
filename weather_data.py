import requests as re
from bs4 import BeautifulSoup

def scrape_weather_data(city):
    url = f"https://weather.com/weather/today/l/{city.replace(' ', '-')}"
    response = re.get(url)
    soup = BeautifulSoup(response.content,'html.parser')

    weather = {
        'temperature' : soup.find('span',{'class' : 'CurrentConditions--tempValue--zUBSz'}).text.strip()+('°'),
        'humidity' : soup.find('div',{'class' : 'WeatherDetailsListItem--wxData--lW-7H' }).text.strip(),
        'wind' : soup.find('div' , {'class' : 'WeatherDetailsListItem--wxData--lW-7H'}).text.strip()+('km/h')
    }

    return weather

city = input("Enter the City: ")
results = scrape_weather_data(city)

print('City:',city.capitalize())
print('Temperature',results['temperature'])
print('Humidity: ',results['humidity'])
print('Wind: ',results['wind'])