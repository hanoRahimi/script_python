import telebot
from googletrans import Translator

bot = telebot.TeleBot('7000717804:AAFyfRAGF-M6nf5_xabnA25JeeZd3smP7F0')
traslator = Translator()

help_button = telebot.types.InlineKeyboardButton("راهنما", callback_data='help')
restart_button = telebot.types.InlineKeyboardButton("شروع مجدد", callback_data='restart')
fallow_button = telebot.types.InlineKeyboardButton("کانال را فالو کنید!", url="https://t.me/")

inline_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
inline_markup.add(help_button, restart_button, fallow_button)

key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
key_markup.add("English", "فارسی")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام دوست من. به ربات ترجمه فارسی به انگلیسی خوش آمدید.", reply_markup=inline_markup)

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    if call.data == 'help':
        bot.send_message(call.message.chat.id, "اینجا محیطی برای ترجمه متن است، متن خود را بفرستید و آن را به زبان انگلیسی تحویل بگیرید.", reply_markup=key_markup)
    elif call.data == 'restart':
        send_welcome(call.message)

@bot.message_handler()
def keyboard_message(message):
    translate_text = traslator.translate(message.text, src='fa', dest='en').text
    bot.send_message(message.chat.id, translate_text)
bot.infinity_polling()