from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv

import telebot
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup

import requests
import json
import phonenumbers
import time

from pfnl.choices import ARTEMISIA_PRODUCTS, PRODUCT_TYPES, YES_NO
# from bot.tts import SpeakMoore
from bot.num_to_text import NumToWords
from bot.num_to_text_bm import NumToWordsBambara
from bot.util import *

load_dotenv()

# =========================================================================================>

MODE = "PFNL"
LANG = "fr"
BOT_TOKEN = ""
ADDITION_URL_MEMBER = "member/"
ADDITION_URL_PRODUCT = "product/"
PHONE_COUNTRY = "BF"
if MODE == "PFNL":
    # speaker = SpeakMoore()
    transcriber = NumToWords()
    BOT_TOKEN = os.getenv("PFNL_BOT_TOKEN")
    LANG = "mo"
else:
    BOT_TOKEN = os.getenv("ARTEMISIA_BOT_TOKEN")
    transcriber = NumToWordsBambara()
    ADDITION_URL_MEMBER = "seller/"
    ADDITION_URL_PRODUCT = "artemisia_product/"
    PHONE_COUNTRY = "ML"
    PRODUCT_TYPES = ARTEMISIA_PRODUCTS
    LANG = "bm"
BASIC_AUTH = os.getenv("BASIC_AUTH")
BASE_URL = "https://lou.pythonanywhere.com/pnfl_api/"

EXPIRATION_MINUTES = 20

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, threaded=False, state_storage=state_storage)

@csrf_exempt
def run_bot(request):
    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])

        return HttpResponse("")

    else:
        raise PermissionDenied

# =========================================================================================>

class MyStates(StatesGroup):
    """
    States to store in between messages
    """
    contact = State() # waiting to get contact information
    product_list = State() # waiting to display the list of products available
    product = State() # waiting to get product name that needs to be changed
    quantity = State() # waiting to get the quantity to be edited
    price = State() # waiting to get the price to be edited
    confirm = State() # waiting for user to confirm changes are right
    generate_communique = State() # waiting for user to generate communique if yes or show products if no


def send_voice_message(filename, path, chat_id):
    """
    Sends a voice message from a file name to the relevant chat
    """
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendVoice?chat_id={chat_id}'
    files=[
        ('voice',(filename,open(path,'rb'),'application/octet-stream'))
    ]
    headers = {}

    return requests.request("POST", url, headers=headers, data={}, files=files)


@bot.message_handler(state="*", commands=['cancel'])
def cancel_state(message):
    """
    Cancel state
    """
    # bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(commands=['start'])
def start(message):
    """
    First interaction with bot, asks to share phone number to link to database
    """
    cancel_state(message)
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    share_button = telebot.types.KeyboardButton(text="Partager contact 📞", request_contact=True)
    keyboard.add(share_button)
    filename = f'welcome_{LANG}.opus'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, "audio", filename)
    send_voice_message(filename, path, message.chat.id)
    bot.send_message(message.chat.id, "📞", reply_markup=keyboard)
    bot.set_state(message.from_user.id, MyStates.contact, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['time_set'] = time.time()