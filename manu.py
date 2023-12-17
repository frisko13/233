import telebot
import sqlite3
from dotenv import dotenv_values
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os
import random



config = dotenv_values(".env")
bot = telebot.TeleBot(config.get("TELEGRAM_TOKEN"))






@bot.message_handler(commands=['start', ''])
def start(message):
    bot.send_message(message.chat.id, 'чтобы получить помощь по командам бота напишите или нажмите /help')



@bot.message_handler(commands=['help', ''])
def start(message):
    bot.send_message(message.chat.id, 'вот команды этого бота  добавление пользователя в базу /baza удаление из базы /deletebaza чтобы узнать о товаре намите /towar отзовы о нас /infa только для определнных личностей /imba ')


@bot.message_handler(commands=['imba'])
def start(message):
    bot.send_message(message.chat.id, 'Наша гильдия ХвостФе')





@bot.message_handler(commands=['baza'])
def baza(message):
    connect = sqlite3.connect('users.db') 
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
           id INTEGER        
    )""")

    people_id = message.chat.id
    cursor.execute("SELECT id FROM login_id WHERE id = ?", (people_id,)) 
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO login_id(id) VALUES(?);", (people_id,))  
        connect.commit()
        bot.send_message(message.chat.id, 'Пользователь добавлен')
    else:
        bot.send_message(message.chat.id, 'Такой пользователь уже существует')

@bot.message_handler(commands=['deletebaza'])
def delete(message):
    connect = sqlite3.connect('users.db') 
    cursor = connect.cursor() 
    people_id = message.chat.id
    cursor.execute("DELETE FROM login_id WHERE id = ?", (people_id,))  
    connect.commit()
    if cursor.rowcount > 0:
        bot.send_message(message.chat.id, 'Пользователь удален')
    else:
        bot.send_message(message.chat.id, 'Пользователь не найден')




 

import requests

@bot.message_handler(commands=['towar'])
def send_ware(message):
    # Отправить сообщение с описанием товара и инлайн-клавиатурой с кнопками
    bot.send_message(message.chat.id, "Название товара: шкаф \nОписание: Шкаф - это многофункциональная мебельная единица, предназначенная для хранения и организации различных предметов. Он обычно имеет несколько отделений, полок и ящиков, которые обеспечивают удобство и функциональность. Шкафы могут быть разных размеров и форм, от небольших прикроватных шкафчиков до больших гардеробных систем. Они могут быть изготовлены из разных материалов, таких как дерево, металл или пластик, и иметь различные стили и дизайны, чтобы соответствовать интерьеру помещения. Шкафы являются неотъемлемой частью меблировки дома или офиса, предоставляя удобное и эстетически приятное решение для хранения и организации вещей.", reply_markup=get_inline_zxcv())

def get_inline_zxcv():
    markup = InlineKeyboardMarkup()
    buy_button = InlineKeyboardButton(text="Купить", callback_data='buy')
    info_button = InlineKeyboardButton(text="Информация", callback_data='info')
    cancel_button = InlineKeyboardButton(text="Отмена", callback_data='cancel')
    markup.row(buy_button, info_button, cancel_button)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'buy':
        # Удалить все кнопки и добавить новые кнопки "Перейти к оплате" и "Отмена"
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_payment_keyboard())
    elif call.data == 'info':
        # Показать описание товара и добавить кнопку "Отмена"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Название товара: шкаф\nОписание: купите этот шкаф деньги пойдут мне в карман",
                              reply_markup=get_cancel_button())
        # Отправить фотографию товара
        send_ware_photo(call.message.chat.id)
    elif call.data == 'cancel':
        # Обновить предыдущее сообщение с описанием товара и инлайн-клавиатурой
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Название товара: шкаф\nОписание: чтобы его купить вам надо оформить кредит",
                              reply_markup=get_inline_zxcv())

def get_payment_keyboard():
    markup = InlineKeyboardMarkup()
    payment_button = InlineKeyboardButton(text="Перейти к оплате", url='https://youtu.be/97H0dHhOqcY?si=lpe3QRfKcclTMev2')
    cancel_button = InlineKeyboardButton(text="Отмена", callback_data='cancel')
    markup.row(payment_button, cancel_button)
    return markup

def get_cancel_button():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="Отмена", callback_data='cancel')
    markup.row(cancel_button)
    return markup

def send_ware_photo(chat_id):
    photo_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcReetqSBSbr8HPwV7sXTkK3SmYM14F8U2O0KfPtFbVZtQ&s'  # Замените ссылку на фактическую
    response = requests.get(photo_url)
    if response.status_code == 200:
        photo_bytes = response.content
        bot.send_photo(chat_id, photo_bytes)
    else:
        bot.send_message(chat_id, "Не удалось загрузить фотографию товара.")












@bot.message_handler(commands=['infa'])
def send_wares(message):
    
    bot.send_message(message.chat.id, "ОТЗОВЫ: перейдти по ссылке чтобы узнать у отзывах о нашей работе ", reply_markup=get_inline_qwer())


def get_inline_qwer():
    markup = InlineKeyboardMarkup()
   
    info_butto = InlineKeyboardButton(text="Информация",url='https://www.tinkoff.ru/baf/93a4Gb5WvP1', callback_data='info')
 
    markup.row( info_butto, )
    return markup








# # Путь к папке с фотографиями
# PHOTO_FOLDER = 'C:\Users\PC\Desktop\фотки'



# # Обработчик команды /randomphoto
# def random_photo(update, context):
#     # Получаем список файлов в папке
#     photo_files = os.listdir(PHOTO_FOLDER)
    
#     # Выбираем случайное имя файла
#     random_file = random.choice(photo_files)
    
#     # Отправляем фотографию пользователю
#     chat_id = update.effective_chat.id
#     context.bot.send_photo(chat_id=chat_id, photo=open(os.path.join(PHOTO_FOLDER, random_file), 'rb'))

# # Создание обработчика команды
# random_photo_handler = CommandHandler('randomphoto', random_photo)

# # Добавление обработчика в бота
# dispatcher = bot.dispatcher
# dispatcher.add_handler(random_photo_handler)
















bot.polling(none_stop=True)