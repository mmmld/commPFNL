import telebot
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv

import requests
import json
import phonenumbers
import time

from ..choices import ARTEMISIA_PRODUCTS, PRODUCT_TYPES, YES_NO
from tts import SpeakMoore
from num_to_text import NumToWords
from num_to_text_bm import NumToWordsBambara
from util import *

load_dotenv()

# =========================================================================================>

TOKEN = os.getenv("PFNL_BOT_TOKEN")
tbot = telebot.TeleBot(TOKEN, threaded=False)


# For free PythonAnywhere accounts
# tbot = telebot.TeleBot(TOKEN, threaded=False)

@csrf_exempt
def bot(request):
    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])

        return HttpResponse("")

    else:
        raise PermissionDenied

# =========================================================================================>

@tbot.message_handler(commands=['start'])
def greet(m):
    tbot.send_message(m.chat.id, "Hello")