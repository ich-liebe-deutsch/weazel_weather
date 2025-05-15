# подключение для тг
import telebot
# подключение для запросов
import requests
# подключение модуля времени
import time

# токен бота в тг
bot = telebot.TeleBot("7640232674:AAEsmmNIvEoADTV0R9g1dPCblYI_Fckiqwo")

# приветствие
start_txt = ('Приветствуем! Это бот прогноза погоды. '
             '\n\nВведите название города для получения информации о температуре и как она ощущается.')

# словари для перевода на русский
# дни недели
days_of_week = {
    'Mon': 'Понедельник',
    'Tue': 'Вторник',
    'Wed': 'Среда',
    'Thu': 'Четверг',
    'Fri': 'Пятница',
    'Sat': 'Суббота',
    'Sun': 'Воскресенье'
}
# месяцы
months = {
    'Jan': 'Января',
    'Feb': 'Февраля',
    'Mar': 'Марта',
    'Apr': 'Апреля',
    'May': 'Мая',
    'Jun': 'Июня',
    'Jul': 'Июля',
    'Aug': 'Августа',
    'Sep': 'Сентября',
    'Oct': 'Октября',
    'Nov': 'Ноября',
    'Dec': 'Декабря'
}


# обрабатываем старт бота
@bot.message_handler(commands=['start'])
def start(message):
    # вывод вышеуказанного сообщения
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')


# узнать время (не ну а вдруг)
@bot.message_handler(commands=['time'])
def get_time(message):
    time_data = time.asctime().split()  # узнаёт общую инфу о времени
    txt = f'Сейчас {time_data[3]} по местному времени.'
    bot.send_message(message.from_user.id, txt)


# узнать дату (не ну а вдруг)
@bot.message_handler(commands=['date'])
def get_date(message):
    date_data = time.asctime().split()  # узнаёт общую инфу о времени
    day_rus = days_of_week[date_data[0]]  # переводит дни на русский
    month_rus = months[date_data[1]]  # переводит месяцы на русский
    txt = f'Сегодня {day_rus}, {date_data[2]} {month_rus}.'
    bot.send_message(message.from_user.id, txt)


# узнать последний город, который искали
@bot.message_handler(commands=['last_city'])
def last_city(message):
    with open("last_city.txt", 'r', encoding='utf-8') as f:  # открывает тхтшник
        data = f.readlines()  # считывает
    txt = f'Последний город, температуру по которому вы запрашивали - {data[0]}'
    bot.send_message(message.from_user.id, txt)


# обрабатываем любой текстовый запрос
@bot.message_handler(content_types=['text'])
def weather(message):
    # город, который прислал пользователь
    city = message.text
    with open("last_city.txt", 'w', encoding='utf-8') as f:  # открывает тхтшник
        f.write(city)  # сохраняет город
    try:
        # формирование запрос
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        # отправка запроса на сервер openweather и получение результата
        weather_data = requests.get(url).json()
        # получаем данные о температуре и о том, как она ощущается
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        # формируем ответы
        w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
        w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
        # отправляем значения
        bot.send_message(message.from_user.id, w_now)
        bot.send_message(message.from_user.id, w_feels)
        # получаем данные о ветре
        wind_speed = round(weather_data['wind']['speed'])
        if wind_speed < 5:
            bot.send_message(message.from_user.id, '✅ Погода хорошая, ветра почти нет')
        elif wind_speed < 10:
            bot.send_message(message.from_user.id, '🤔 На улице ветрено, оденьтесь чуть теплее')
        elif wind_speed < 20:
            bot.send_message(message.from_user.id, '❗️ Ветер очень сильный, будьте осторожны, выходя из дома')
        else:
            bot.send_message(message.from_user.id, '❌ На улице шторм, на улицу лучше не выходить')
    except Exception:  # обработка, если кто-то неграмотный или не знает города
        err_message = '❌ Город не найден. Возможно, вы ошиблись в написании. ❌'
        bot.send_message(message.from_user.id, err_message)
        return


# запуск бота
if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e:
            print(f'❌ Непредвиденная ошибка: {e} ❌')
