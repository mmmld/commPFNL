from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

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
from pfnl.models import Cooperative, Member, Product, ArtemisiaSeller, ArtemisiaProduct
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

def test_phone_number(phone_number, message):
    """
    Checks if the phone number exists in the database,
    if yes, adds the chat_id to the db (if needed)
    otherwise, prompts the user to first get registered in the system through the radio
    """

    # TODO add option for seller when in artemisia mode

    member = Member.objects.filter(Q(member_phone__icontains=phone_number)).first()
    telegram_id = message.chat.id
    if member == None:
        # bot.send_message(telegram_id, "Une erreur est survenue. Il semble que votre numéro n'est pas enregistré dans le system. Veuillez vous addressez à la radio pour qu'il vous y ajoute.")
        send_voice_message(f'error_number_{LANG}', f'./audio/error_number_{LANG}.opus', telegram_id)
        return
    if MODE == "PFNL":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['comm_name'] = member['coop']['coop_name']
            data['comm_phone'] = member['coop']['coop_phone']
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['seller_name'] = member['name']
            data['seller_phone'] = member['phone']

    if member.telegram_id != telegram_id:
        # response = requests.request("PUT", url + member_id + '/', headers=headers, data={'telegram_id':telegram_id})
        # data = {
        #          'telegram_id': 'telegram_id',
        #     }
        member.telegram_id = telegram_id
        member.save()
    show_products(message)
        


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

@bot.message_handler(commands=['hello'])
def greet(message):
    """
    Start of an interaction with a user, assumes telegram ID is known
    """
    telegram_id = message.chat.id
    # bot.send_message(telegram_id, "Bonjour, voici une liste de vos produits")
    send_voice_message(f'intro_products_{LANG}', f'./audio/intro_products_{LANG}.opus', message.chat.id)
    bot.set_state(message.from_user.id, MyStates.product_list, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['time_set'] = time.time()
    # bot.add_data(message.from_user.id,message.chat.id, {'time_set': time.time()})
    show_products(message)


def show_products(message):
    bot.send_message(message.chat.id, "show products OK")