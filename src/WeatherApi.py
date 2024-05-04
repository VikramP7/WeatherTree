import urequests as requests
import utime as time
import json

class WeatherApi():
    
    #url = 'http://api.weatherapi.com/v1/forecast.json'
    #url = 'http://api.weatherapi.com/v1/current.json'
    # https://www.weatherapi.com/docs/weather_conditions.json
    
    weather = {}
    weather_births = {}
    
    def __init__(self, cities, api_key, alerts = False):
        self.url = 'http://api.weatherapi.com/v1/current.json'
        self.url_with_params = ''
        self.params = {}
        self.params['key'] = api_key
        self.params['q'] = cities[0]
        self.params['alerts'] = 'yes' if alerts else 'no'
        self.weather = {}
        self.weather_births = {}
        for city in cities:
            try:
                self.fetch_weather_data(city)
            except:
                print("Failed to fetch weather for " + city)
        
        
    def create_url(self):
        # find parameter labels
        identifiers = self.params.keys()
        # create string to append to url
        param_add = "?"
        # append each parameter split by a '&'
        for identifier in identifiers:
            param_add += f"{identifier}={self.params[identifier].replace(' ', '%20')}&"
        
        # remove the last unneccesary '&'
        param_add = param_add[:-1]
        
        # concatinate url with parameters
        self.url_with_params = self.url + param_add
    
    def fresh_weather(self, city):
        # attempt to gather information on weather based on pre-fetched store
        try:
            cur_weather = self.weather[city]
            cur_age = time.time() - self.weather_births[city]
        except KeyError:
            # the city doesn't exist yet in the pre-fetched store
            # initialise this city
            try:
                self.fetch_weather_data(city)
            except:
                print("That city is really not good: " + city)
            
        if cur_age > 10*60: # over ten minutes old
            try:
                self.fetch_weather_data(city)
            except:
                print("Failed to refresh old weather, weather remains as old values")
        
    
    def get_city_temp(self, city):
        # check if current weather is new enough for the city
        self.fresh_weather(city)
        return self.weather[city].get("current").get("temp_c")
    
    
    def get_city_feels_like_temp(self, city):
        # check if current weather is new enough for the city
        self.fresh_weather(city)
        return self.weather[city].get("current").get("feelslike_c")
        
    
    def get_city_wind_dir(self, city):
        # check if current weather is new enough for the city
        self.fresh_weather(city)
        return self.weather[city].get("current").get("wind_degree")
    
    def get_city_condition(self, city):
        # check if current weather is new enough for the city
        self.fresh_weather(city)
        return self.weather[city].get("current").get("condition").get("text")
    
    def get_city_precipitation(self, city):
        # check if current weather is new enough for the city
        self.fresh_weather(city)
        return self.weather[city].get("current").get("precip_mm")
    
    def get_city_weather(self, city):
        # check if current weather is new enough for the city
        self.fresh_weather(city)
        return self.get_city_temp(city), self.get_city_wind_dir(city), self.get_city_condition(city), self.get_city_precipitation(city)
    
    def fetch_weather_data(self, city):
        self.params['q'] = city
        self.create_url()
        response = requests.get(self.url_with_params)
        weather_fetch = {}
        if response.status_code == 200:
            weather_fetch = response.json()
            print("Fetched: " + self.url_with_params)
            #print(weather_fetch)
        else:
            print('Request failed with status code:', response.status_code)
            raise Exception("Weather Request Failed")
        try:
            weather_fetch['location']
        except KeyError:
            print("Weather query returned error response")
        self.weather[city] = weather_fetch
        self.weather_births[city] = time.time()
        response.close()
        
    
        