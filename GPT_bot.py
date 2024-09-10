import telebot  #pip install pyTelegramBotAPi
import requests
from telebot import types

API_TOKEN = "7017493144:AAFkS-l1MeSGa2zwoiDDBBP1Rc6XuJJjfh0"
CHANNEL_USERNAME = '@telbotTestAi'
WEB_SERVICE_URL = "https://api3.haji-api.ir/majid/gpt/4"
LICENSE_KEY = "ySqmcpbUfJc3NVNSRuwTETFvHLpeydDT3YY9AfMj9fZeiDiZPWotW5XPc"

bot = telebot.TeleBot(API_TOKEN)

def check_user_subscription(chat_id):
    try:
        answer = bot.get_chat_member(CHANNEL_USERNAME, chat_id)
        return answer.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f":خطا در بررسی عضویت {e}")
        return False

def send_requests(text):
    try:
        responce = requests.get(WEB_SERVICE_URL, params={"q":text, "license":LICENSE_KEY})
        responce.raise_for_status()
        return responce.json()
    except requests.RequestException as e:
        print(f":خطا در ارتباط با وب سرویس{e}")
        return None

@bot.message_handler(func=lambda message:True)
def handle_message(message):
    if check_user_subscription(message.chat.id):
        bot.send_chat_action(message.chat.id,'typing')
        user_input=message.text
        result = send_requests(user_input)
        if result and result['success']:
            bot.reply_to(message,f"{result['result']}")
        else:
            error_message = result['error'] if result else "خطا در دریافت پاسخ از سرویس وب"
            bot.reply_to(message,f"{error_message}:خطا")

    else:
        markup = types.InlineKeyboardMarkup()
        join_button = types.InlineKeyboardButton(text="عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        markup.add(join_button)
        bot.send_message(message.chat.id,"برای استفاده از ربات، لطفا در کانال عضو شوید.",reply_markup=markup)

bot.polling(none_stop=True)