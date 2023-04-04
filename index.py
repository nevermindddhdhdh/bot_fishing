import telebot
from telebot import types
from telebot import apihelper
import re
import parcingModules
import databaseModules

apihelper.proxy = {'socks5h':'91.195.125.86:8000@Gea6AX:1YckDX'}
bot = telebot.TeleBot('6075333341:AAFrBpDs0fZqPGuifUzMDHeqcP_QjOzvkPc')

def checkMail(mail, idd):
	oMail = mail.text.replace(' ', '')
	match = re.search(r'\b\w+@\w{2,}\.\w{2,}\b', oMail) 
	if match:
		bot.send_message(idd, parcingModules.postRegRu(oMail, idd, 'mail'), parse_mode="MARKDOWN")
	else:
		msg = bot.send_message(idd, 'Ошибка! Вы неверно ввели почту\nВведите еще раз:')
		bot.register_next_step_handler(msg, checkMail, idd)


def checkPhone(phone, idd):
	oPhone = phone.text.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
	match = re.search(r'\+\d{10,}\b', oPhone) 
	if match:
		print(oPhone)
	else:
		msg = bot.send_message(idd, 'Ошибка! Вы неверно ввели номер\nВведите еще раз:')
		bot.register_next_step_handler(msg, checkPhone, idd)


def checkLink(link, idd):
	oLink = link.text.replace(' ', '')
	match = re.search(r'(https?:\/\/w{3}?.\w+\.\w+\/?|https?:\/\/\w+\.\w+\/?|\w+\.\w+)', oLink) 
	if match:
		bot.send_message(idd, parcingModules.postRegRu(oLink, idd, 'link'), parse_mode="MARKDOWN")
	else:
		msg = bot.send_message(idd, 'Ошибка! Вы неверно ввели ссылку\nВведите еще раз:')
		bot.register_next_step_handler(msg, checkLink, idd)


def fullCheck(idd):
	return 0


@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        print('err')
    text = "Привет"
    keyboard = types.InlineKeyboardMarkup()
    keyMail = types.InlineKeyboardButton(text='Проверить почту \U00002709', callback_data='checkMail')
    keyPhone = types.InlineKeyboardButton(text='Проверить номер \U0001F4DE', callback_data='checkPhone')
    keyLink = types.InlineKeyboardButton(text='Проверить Ссылку \U0001F517', callback_data='checkLink')
    keyFull = types.InlineKeyboardButton(text='Полная проверка \U0001F50E', callback_data='checkFull')
    keyboard.add(keyMail, keyPhone)
    keyboard.add(keyLink)
    keyboard.add(keyFull)
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)
 

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "checkMail":
        msg = bot.send_message(call.message.chat.id, 'Введите почту:')
        bot.register_next_step_handler(msg, checkMail, call.message.chat.id)
    elif call.data == "checkPhone":
        msg = bot.send_message(call.message.chat.id, 'Введите номер в международном формате:')
        bot.register_next_step_handler(msg, checkPhone, call.message.chat.id)
    elif call.data == "checkLink":
        msg = bot.send_message(call.message.chat.id, 'Введите ссылку:')
        bot.register_next_step_handler(msg, checkLink, call.message.chat.id)
    elif call.data == "fullCheck":
        print("full")


bot.polling(none_stop=True, interval=0)