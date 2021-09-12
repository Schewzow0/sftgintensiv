import telebot
import requests
from bs4 import BeautifulSoup as bs
import random
from telebot import types

TOKEN = ''

bot = telebot.TeleBot(TOKEN)
URL_ENG = 'https://puzzle-english.com/directory/1000-popular-words'
URL_CURRENCY = 'https://finance.rambler.ru/currencies/'


def parse_currency():
    request = requests.get(URL_CURRENCY)
    soup = bs(request.text, 'html.parser')
    currency = soup.find_all('div', class_='currency-block__marketplace-value')
    l = open('currency.txt', 'w')
    for x in currency:
        l.write(str(x).replace('<div class="currency-block__marketplace-value">', '').replace('</div>', ''))
    l.close()
    l = open('currency.txt', 'r')
    a = ['USD вчера', '', 'USD сегодня', '', 'EURO вчера', '', 'EURO сегодня', '']
    h = 0
    for x in l:
        if h == 1:
            a[1] = x
        elif h == 3:
            a[3] = x
        elif h == 9:
            a[5] = x
        elif h == 11:
            a[7] = x
        h += 1
    return ''.join(a)


def parse_words():
    request = requests.get(URL_ENG)
    soup = bs(request.text, 'html.parser')
    words = soup.find_all('li', style='font-weight: 400;')
    f = open('words.txt', 'w')
    x = 0
    for word in words:
        x += 1
        f.write(str(word) + '\n')
        if x >= 200:
            break
    f.close()
    l = open('words.txt', 'r')
    a = []
    for word in l:
        a.append(str(l.readline().replace('<li style="font-weight: 400;"><span style="font-weight: 400;">', ''))
                 .replace('</span><span style="font-weight: 400;">', '')
                 .replace('</span><span style="font-weight: 400;">', '')
                 .replace('</span></li>', ''))
    l.close()
    s = open('words.txt', 'w')
    for x in a:
        s.write(x)
    s.close()


@bot.message_handler(commands=['hi', 'start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'I\'m starting')


@bot.message_handler(content_types=['text'])
def get_currency(message):
    # if message.text == 'K':
    #     markup = types.ReplyKeyboardMarkup(row_width=2)
    #     itembtn1 = types.KeyboardButton('a')
    #     itembtn2 = types.KeyboardButton('b')
    #     itembtn3 = types.KeyboardButton('c')
    #     markup.add(itembtn1, itembtn2, itembtn3)
    #     bot.send_message(message.from_user.id, "Choose one letter:", reply_markup=markup)
    # if message.text == 'a':
    #     bot.send_message(message.from_user.id, 'letter a')
    # elif message.text == 'b':
    #     bot.send_message(message.from_user.id, 'letter b')
    # elif message.text == 'c':
    #     bot.send_message(message.from_user.id, 'letter c')

    # doc = open('currency.txt', 'rb')
    # bot.send_document(message.from_user.id, doc)
    # photo = open('img.png', 'rb')
    # bot.send_photo(message.from_user.id, photo)

    if message.text == 'Курс':
        bot.send_message(message.from_user.id, 'Курс валют:')
        bot.send_message(message.from_user.id, f'{str(parse_currency())}')
    elif message.text == 'Слова':
        bot.send_message(message.from_user.id, 'Вот слова на сегодня:')
        for s in range(0, 10):
            bot.send_message(message.from_user.id, f'{random.choice(open("words.txt").readlines())}')


# Bot repeater
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    print('Start parsing...')
    parse_words()
    print('Parsing end')
    bot.polling(none_stop=True, interval=0)
