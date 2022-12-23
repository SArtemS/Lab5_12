from owm_key import owm_api_key
from getweatherdata import get_weather_data, visualise_data

key = owm_api_key

if __name__ == '__main__':
    weather_data_json, average_temps = get_weather_data(key)
    print(average_temps)
    visualise_data(weather_data_json, average_temps)
    