import pyowm
import datetime
import requests


def direction(deg, language_key):
    if 348.75 < deg <= 11.25:
        if language_key == 'ru':
            return 'Направвление ветра: C;'
        else:
            return 'Direction of the wind: N;'
    elif 11.25 < deg <= 33.75:
        if language_key == 'ru':
            return 'Направвление ветра: ССВ;'
        else:
            return 'Direction of the wind: NNE;'
    elif 33.75 < deg <= 56.25:
        if language_key == 'ru':
            return 'Направвление ветра: СВ;'
        else:
            return 'Direction of the wind: NE;'
    elif 56.25 < deg <= 78.75:
        if language_key == 'ru':
            return 'Направвление ветра: ВСВ;'
        else:
            return 'Direction of the wind: ENE;'
    elif 78.75 < deg <= 101.25:
        if language_key == 'ru':
            return 'Направвление ветра: В;'
        else:
            return 'Direction of the wind: E;'
    elif 101.25 < deg <= 123.75:
        if language_key == 'ru':
            return 'Направвление ветра: ВЮВ;'
        else:
            return 'Direction of the wind: ESE;'
    elif 123.25 < deg <= 146.25:
        if language_key == 'ru':
            return 'Направвление ветра: ЮВ;'
        else:
            return 'Direction of the wind: SE;'
    elif 146.25 < deg <= 168.75:
        if language_key == 'ru':
            return 'Направвление ветра: ЮЮВ;'
        else:
            return 'Direction of the wind: SSE;'
    elif 168.75 < deg <= 191.25:
        if language_key == 'ru':
            return 'Направвление ветра: С;'
        else:
            return 'Direction of the wind: S;'

    elif 191.25 < deg <= 213.25:
        if language_key == 'ru':
            return 'Направвление ветра: ЮЮВ;'
        else:
            return 'Direction of the wind: SSW;'
    elif 213.75 < deg <= 236.25:
        if language_key == 'ru':
            return 'Направвление ветра: ЮВ;'
        else:
            return 'Direction of the wind: SW;'
    elif 236.25 < deg <= 258.75:
        if language_key == 'ru':
            return 'Направвление ветра: ВЮВ;'
        else:
            return 'Direction of the wind: WSW;'
    elif 258.75 < deg <= 281.25:
        if language_key == 'ru':
            return 'Направвление ветра: В;'
        else:
            return 'Direction of the wind: W;'
    elif 281.25 < deg <= 303.75:
        if language_key == 'ru':
            return 'Направвление ветра: ВСВ;'
        else:
            return 'Direction of the wind: WNW;'
    elif 303.75 < deg <= 326.25:
        if language_key == 'ru':
            return 'Направвление ветра: СВ;'
        else:
            return 'Direction of the wind: NW;'
    elif 326.25 < deg <= 348.75:
        if language_key == 'ru':
            return 'Направвление ветра: ССВ;'
        else:
            return 'Direction of the wind: NNW;'


def obs(language_key, obs_type, api_key):
    owm = pyowm.OWM(api_key, language=language_key)
    if obs_type == '0':
        observation = owm.weather_at_place('Moscow,RU')
        w = observation.get_weather()

        if language_key == 'ru':
            text = 'Текущая погода \u2935\ufe0f:\n'

        else:
            text = 'The current weather \u2935\ufe0f:\n'

        temp = (lambda language_key: 'Температура: {} С;'.format(str(round(w.get_temperature('celsius')['temp'], 1)))
        if language_key == 'ru' else 'Temperature: {} C;'.format(str(w.get_temperature('celsius')['temp'])))

        if w.get_wind().get('speed'): #Проверки для ветра. Не всегда можно получить оба значения
            speed = (lambda language_key: 'Скорость ветра: {} м/сек.;'.format(str(round(w.get_wind()['speed'], 1)))
            if language_key == 'ru' else 'Wind speed: {} m/sec.;'.format(str(w.get_wind()['speed'])))
        else:
            speed = ''

        if w.get_wind().get('deg'):
            direct = direction(w.get_wind()['deg'], language_key) # Место для ключа. Этот ключ определяет язык в функции выше
        else:
            direct = ''

        humidity = (lambda language_key: 'Влажность воздуха: {}%;'.format(str(w.get_humidity())) if language_key == 'ru'
        else 'Air humidity: {}%;'.format(str(w.get_humidity())))

        weather_discr = w.get_detailed_status().capitalize()+'{}.'.format(weather_type(w.get_weather_code()))

        text += temp(language_key)+'\n'+speed(language_key)+'\n'+direct+'\n'+humidity(language_key)+'\n'+weather_discr
        return text

    elif obs_type == '1':
        now = str(datetime.date.today())
        next_day = str((datetime.date.today() + datetime.timedelta(1))) + ' 00:00:00+00'
        line = ''
        text = ''

        owm = pyowm.OWM(api_key, language=language_key)
        fc = owm.three_hours_forecast('Moscow,RU')
        f = fc.get_forecast()

        if language_key == 'ru':
            text += 'Погода сегодня \u2935\ufe0f:\n'
            line += 'Время: {}. Темп.: {} С. Ветер: {} м/с. {}.'
        else:
            text += 'The weather is today \u2935\ufe0f:\n'
            line += 'Time: {}. Temp.: {} C. Wind: {} m/s. {}.'

        for w in f:
            if w.get_reference_time('iso').split()[0] == now or w.get_reference_time('iso') == next_day:
                time = w.get_reference_time('iso').split()[1][:5]
                temp = round(w.get_temperature('celsius')['temp'], 1)
                wind = round(w.get_wind()['speed'], 1)
                weather = w.get_detailed_status().capitalize() + weather_type(w.get_weather_code())
                text += line.format(time, temp, wind, weather) + '\n'
        return text

    elif obs_type == '2':
        next_day = str((datetime.date.today() + datetime.timedelta(1)))
        line = ''
        text = ''

        owm = pyowm.OWM(api_key, language=language_key)
        fc = owm.three_hours_forecast('Moscow,RU')
        f = fc.get_forecast()

        if language_key == 'ru':
            text += 'Погода завтра \u2935\ufe0f:\n'
            line += 'Время: {}. Темп.: {} С. Ветер: {} м/с. {}.'
        else:
            text += 'Weather tomorrow \u2935\ufe0f:\n'
            line += 'Time: {}. Temp.: {} C. Wind: {} m/s. {}.'

        for w in f:
            if w.get_reference_time('iso').split()[0] == next_day: #and int(w.get_reference_time('iso').split()[1][:2]) % 3 == 0:
                time = w.get_reference_time('iso').split()[1][:5]
                temp = round(w.get_temperature('celsius')['temp'], 1)
                wind = round(w.get_wind()['speed'], 1)
                weather = w.get_detailed_status().capitalize() + weather_type(w.get_weather_code())
                text += line.format(time, temp, wind, weather) + '\n'
        return text

    elif obs_type == '3':
        morning = dict(ru='Температура утром: {} C;\n', en='Temperature in the morning: {} C;\n')
        day = dict(ru='Температура днем: {} C;\n', en='Temperature during the day: {} C;\n')
        evening = dict(ru='Температура вечером: {} C;\n', en='Temperature in the evening: {} C;\n')
        night = dict(ru='Температура ночью: {} C;\n', en='Temperature at night: {} C;\n')

        url = 'https://api.openweathermap.org/data/2.5/onecall?exclude=current,minutely,hourly'
        params = {'lat': 55.7522, 'lon': 37.6156, 'units': 'metric', 'lang': language_key, 'APPID': api_key}

        response = requests.get(url, params)
        res = response.json()
        text = ''

        if language_key == 'ru':
            text += 'Ваш прогноз на 7 дней \u2935\ufe0f:\n'
            text += '\n'
        else:
            text += 'Your weather forecast for 7 days \u2935\ufe0f:\n'
            text += '\n'

        for next_day in range(1, 8):
            text += str(datetime.date.today() + datetime.timedelta(next_day)) + ':\n'
            text += morning[language_key].format(round(res['daily'][next_day]['temp']['morn'], 1))
            text += day[language_key].format(round(res['daily'][next_day]['temp']['day'], 1))
            text += evening[language_key].format(round(res['daily'][next_day]['temp']['eve'], 1))
            text += night[language_key].format(round(res['daily'][next_day]['temp']['night'], 1))
            text += res['daily'][next_day]['weather'][0]['description'].capitalize() + \
                    '{}.\n'.format(weather_type(res['daily'][next_day]['weather'][0]['id']))
            text += '\n'

        return text


def weather_type(index):
    emoji = {200: '\ud83c\udf29', 201: '\ud83c\udf29', 202: '\ud83c\udf29', 210: '\ud83c\udf29', 211: '\ud83c\udf29',
             212: '\ud83c\udf29', 221: '\ud83c\udf29', 230: '\ud83c\udf29', 231: '\ud83c\udf29', 232: '\ud83c\udf29',
            300: '\ud83c\udf27', 301: '\ud83c\udf27', 302: '\ud83c\udf27', 310: '\ud83c\udf27', 311: '\ud83c\udf27',
             312: '\ud83c\udf27', 313: '\ud83c\udf27', 314: '\ud83c\udf27', 321: '\ud83c\udf27',
            500: '\ud83c\udf27', 501: '\ud83c\udf27', 502: '\ud83c\udf27', 503: '\ud83c\udf27', 504: '\ud83c\udf27',
             511: '\ud83c\udf27', 520: '\ud83c\udf27', 521: '\ud83c\udf27', 522: '\ud83c\udf27', 531: '\ud83c\udf27',
            600: '\u2744\ufe0f', 601: '\u2744\ufe0f', 602: '\u2744\ufe0f', 611: '\u2744\ufe0f', 612: '\u2744\ufe0f',
             613: '\u2744\ufe0f', 615: '\u2744\ufe0f', 616: '\u2744\ufe0f', 620: '\u2744\ufe0f', 621: '\u2744\ufe0f',
             622: '\u2744\ufe0f', 701: '\ud83c\udf2b', 711: '\ud83c\udf2b', 721: '\ud83c\udf2b',
             731: '\ud83c\udf2b', 741: '\ud83c\udf2b', 771: '\ud83c\udf2c', 781: '\ud83c\udf2a', 800: '\u2600\ufe0f',
             801: '\ud83c\udf24', 802: '\u26c5\ufe0f', 803: '\ud83c\udf25', 804: '\u2601\ufe0f'}
    if emoji.get(index):
        return emoji[index]
    #751:, 761:, 762:,