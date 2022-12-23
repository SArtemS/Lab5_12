def get_weather_data(api_key=None):
    import json
    import requests
    import time
    city, lat, lon = "Saint Petersburg, RU", 59.57, 30.19

    if api_key:
        day_diff = 86400
        day_amount = 4
        dt = int(time.time()) - day_diff * day_amount
        result = dict()
        result['city'] = city
        result['temps'] = []
        avg_temps = dict()
        avg_temps['days'] = []
        for i in range(day_amount + 1):
            avg_temp = 0
            avg_div = 0
            req = requests.get(f'http://api.openweathermap.org/data/2.5/'
                            f'onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&'
                            f'appid={api_key}&lang=ru&units=metric')
            req_obj = json.loads(
                req.text) 
            measures = [{
                "dt": str(time.strftime("%d/%m %H", time.gmtime(measure['dt']))) + 'h',
                "temp": (measure['temp'])
            } for measure in req_obj["hourly"]]
            result['temps'].extend(measures)
            for i in req_obj["hourly"]:
                avg_temp += i['temp']
                avg_div += 1
            avg_temps['days'].extend([{"dt": str(time.strftime("%d/%m 12", time.gmtime(dt))) + 'h',
                                        "avg_temp": float(format(avg_temp/avg_div, ".2f"))}])
            dt += day_diff

        with open('data.json', 'w') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        return json.dumps(result), avg_temps


def visualise_data(json_data='', avg_ts = None):

    if json_data:
        import matplotlib.pyplot as pplt
        import pandas
        data = pandas.read_json(json_data)
        dates = [_d['dt'] for _d in data['temps'][:]]
        temps = [_t['temp'] for _t in data['temps'][:]]
        pplt.title(f"Температура за последние 5 дней:")
        pplt.scatter(dates, temps)
        pplt.xticks(rotation = 90, fontsize = 5)
        avg_dates = [_d['dt'] for _d in avg_ts['days'][:]]
        avg_temps = [_t['avg_temp'] for _t in avg_ts['days'][:]]
        pplt.plot(avg_dates, avg_temps, '-')
        pplt.show()
