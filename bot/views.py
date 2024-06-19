from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

import os
from dotenv import load_dotenv

import telebot

import requests
import json
import phonenumbers
import time
from datetime import datetime, timedelta
import pytz

from pfnl.choices import PRODUCT_TYPES, YES_NO
from pfnl.models import Cooperative, Member, Product
# from bot.tts import SpeakMoore
from bot.num_to_text import NumToWords
from bot.num_to_text_bm import NumToWordsBambara
from bot.util import *
from .models import State

import logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


load_dotenv()

# =========================================================================================>

MODE = "PFNL"
LANG = "mo"
# LANG = "fr"
BOT_TOKEN = ""
PHONE_COUNTRY = "BF"
# speaker = SpeakMoore()
transcriber = NumToWords()
BOT_TOKEN = os.getenv("PFNL_BOT_TOKEN")

timezone = pytz.timezone('Africa/Abidjan')
EXPIRATION_MINUTES = 20

dir_path = os.path.dirname(os.path.realpath(__file__))

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

inverted_prod = {value: key for key, value in PRODUCT_TYPES[LANG].items()}

@csrf_exempt
def run_bot(request):
    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])

        return HttpResponse("", status=200)

    else:
        raise PermissionDenied

# =========================================================================================>

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


def test_phone_number(phone_number, message):
    """
    Checks if the phone number exists in the database,
    if yes, adds the chat_id to the db (if needed)
    otherwise, prompts the user to first get registered in the system through the radio
    """

    member = Member.objects.filter(Q(member_phone__icontains=phone_number)).first()
    telegram_id = message.chat.id
    if member == None:
        # bot.send_message(telegram_id, "Une erreur est survenue. Il semble que votre numéro n'est pas enregistré dans le system. Veuillez vous addressez à la radio pour qu'il vous y ajoute.")
        filename = f'error_number_{LANG}.opus'
        path = os.path.join(dir_path, "audio", filename)
        send_voice_message(filename, path, telegram_id)
        return
    if member.telegram_id != telegram_id:
        member.telegram_id = telegram_id
        member.save()

    show_products(message)


@bot.message_handler(commands=['start'])
def start(message):
    """
    First interaction with bot, asks to share phone number to link to database
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    share_button = telebot.types.KeyboardButton(text="Partager contact 📞", request_contact=True)
    keyboard.add(share_button)
    filename = f'welcome_{LANG}.opus'
    path = os.path.join(dir_path, "audio", filename)
    send_voice_message(filename, path, message.chat.id)
    bot.send_message(message.chat.id, "📞", reply_markup=keyboard)
    try:
        state = State.objects.get(telegram_id=message.chat.id)
        state.state = "contact"
        state.save()
    except State.DoesNotExist:
        state = State(telegram_id=message.chat.id, state="contact")
        state.save()


@bot.message_handler(commands=['hello'])
def greet(message):
    """
    Start of an interaction with a user, assumes telegram ID is known
    """
    telegram_id = message.chat.id
    try:
        state = State.objects.get(telegram_id=telegram_id)
        state.state = "product_list"
        state.save()

        filename = f'intro_products_{LANG}.opus'
        path = os.path.join(dir_path, "audio", filename)
        send_voice_message(filename, path, message.chat.id)

        show_products(message)
    except State.DoesNotExist:
        start(message)


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """
    Upon receiving contact info, checks if the phone number exists in the database,
    if yes, adds the chat_id to the db (if needed)
    otherwise, prompts the user to first get registered in the system through the radio
    """
    phone_number = message.contact.phone_number
    filename = f'thanks_sharing_{LANG}.opus'
    path = os.path.join(dir_path, "audio", filename)
    send_voice_message(filename, path, message.chat.id)
    bot.send_message(message.chat.id, "⏳⌛️")
    try:
        test_phone_number(phone_number, message)
    except:
        filename = f'error_number_{LANG}.opus'
        path = os.path.join(dir_path, "audio", filename)
        send_voice_message(filename, path, message.chat.id)
        print("error with phone number")


def is_phone_number(message):
    """
    Looks for a phone number in the message to match the user in the db,
    if no phone number, prompts to give it
    """
    try:
        phone_number = phonenumbers.parse(message.text, PHONE_COUNTRY)
        if phonenumbers.is_valid_number(phone_number):
            phone_number = str(phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164))
            test_phone_number(phone_number, message)
        else:
            raise ValueError
    except:
        filename = f'share_contact_{LANG}.opus'
        path = os.path.join(dir_path, "audio", filename)
        send_voice_message(filename, path, message.chat.id)
        bot.send_message(message.chat.id, "📞")


def show_products(message):
    """
    fetches products from a member in the db and if available send a voice note in Mooré to recap the stocks
    """
    chat_id = message.chat.id

    try:
        member = Member.objects.get(telegram_id=chat_id)
        products = member.product_set.all()
        product_ids = dict() # storing product IDs if the user chooses to edit quantities
        keyboard = telebot.types.ReplyKeyboardMarkup() # keyboard to choose which product to edit
        filename = str(chat_id) + '_quantities'
        path = os.path.join(dir_path, "output", filename + 'ogg')

        text = "yam ‘b paama "
        for prod in products:
            prod_type = prod.prod_type
            if prod_type != "None":
                prod_name = PRODUCT_TYPES[LANG][prod_type]
                prod_quantity = prod.quantity
                text += transcriber.transcribe(prod_quantity)
                text += " "
                text += prod_name + ", "
                prod_button = telebot.types.KeyboardButton(text=prod_name)
                keyboard.add(prod_button)
                product_ids[prod_name] = (prod.id, prod_type, prod_quantity)
        # speaker.speak(text, filename)


        # send_voice_message(filename, path, chat_id)
        bot.send_message(chat_id, text)

        if os.path.exists(path):
            os.remove(path)

    except Member.DoesNotExist:
        filename = f'error_try_again_{LANG}.opus'
        path = os.path.join(dir_path, "audio", filename)
        send_voice_message(filename, path, chat_id)
        start(message)
        return


    try:
        state = State.objects.get(telegram_id=chat_id)
        state.state = "product"
        state.save()

        # Prompt for next action
        bot.send_message(chat_id, "📚", reply_markup=keyboard)
        filename = f'select_product_{LANG}.opus'
        path = os.path.join(dir_path, "audio", filename)
        send_voice_message(filename, path, message.chat.id)

    except State.DoesNotExist:
        filename = f'error_try_again_{LANG}.opus'
        path = os.path.join(dir_path, "audio", filename)
        send_voice_message(filename, path, chat_id)
        start(message)
        return


def send_yes_no_keyboard(chat_id):
    """
    Send a simple keyboard to the user to answer yes or no
    Also send a voice message to say that the first button corresponds to yes and the second one to no
    """
    keyboard = telebot.types.ReplyKeyboardMarkup()
    yes_button = telebot.types.KeyboardButton(text=YES_NO[LANG]["yes"])
    no_button = telebot.types.KeyboardButton(text=YES_NO[LANG]["no"])
    keyboard.add(yes_button)
    keyboard.add(no_button)
    bot.send_message(chat_id, "❔", reply_markup=keyboard)

    filename = f'select_button_yes_no_{LANG}.opus'
    path = os.path.join(dir_path, "audio", filename)
    send_voice_message(filename, path, chat_id)


@bot.message_handler(func=lambda msg: msg.text in list(PRODUCT_TYPES[LANG].values()))
def edit_product(message):
    """
    Select a product to edit
    """
    chat_id = message.chat.id
    prod = message.text
    state = State.objects.get(telegram_id=chat_id)


    prod_type = inverted_prod[prod]

    filename = str(chat_id) + '_change_product.opus'
    path = os.path.join(dir_path, 'output', filename)
    if LANG == "fr" or LANG == "bm":
        concat_audios([os.path.join(dir_path, 'audio', f'change_quantity_of_{LANG}.opus'), os.path.join(dir_path, 'audio' , f'{prod_type}_{LANG}.opus')], path)
    if LANG == "mo":
        concat_audios([os.path.join(dir_path, 'audio', 'change_quantity_of_1mo.opus'), os.path.join(dir_path, 'audio', f'{prod_type}_mo.opus'), os.path.join(dir_path, 'audio', 'change_quantity_of_2mo.opus')], path)
    send_voice_message(filename, path, message.chat.id)
    send_voice_message(f'enter_quantity_{LANG}', os.path.join(dir_path, 'audio', f'enter_quantity_{LANG}.opus'), message.chat.id)

    if os.path.exists(path):
        os.remove(path)


    # Storing name of product to change
    state.state = "quantity"
    state.product = message.text
    state.save()


def edit_quantity(message):
    """
    Quantity for a product has been correctly inputed, asking for the user if they are sure about the change
    """
    try:
        state = State.objects.get(telegram_id=message.chat.id)
        state.quantity = message.text
        state.state = "confirm"
        state.save()
        if LANG == "fr":
                bot.send_message(message.chat.id, "Est-vous sûr de vouloir changer la quantité de " + state.product + " pour une quantité de " + message.text)
        if LANG == "mo":
            txt = "Yam’b rat n’teka a sombl ma " + state.product
            bot.send_message(message.chat.id, txt)
            filename = str(message.chat.id) + '_ensure_change'
            path = os.path.join(dir_path, 'output', filename + '.ogg')
            # speaker.speak(txt, filename)
            # send_voice_message(filename, path, message.chat.id)
            if os.path.exists(path):
                os.remove(path)

        send_yes_no_keyboard(message.chat.id)

    except State.DoesNotExist:
        start(message)


def quantity_incorrect(message):
    """
    Prompts the user to only input number for quantity
    """
    try:
        state = State.objects.get(telegram_id=message.chat.id)
        filename = f'error_quantity_{LANG}.opus'
        path = os.path.join(dir_path, 'audio', filename)
        send_voice_message(filename, path, message.chat.id)

    except State.DoesNotExist:
        start(message)


def edit_product(message):
    """
    Quantity for a product has been correctly inputed and confirmed, now recording it in the database
    """
    try:
        chat_id = message.chat.id
        state = State.objects.get(telegram_id=chat_id)
        prod_name = state.product
        prod_type = inverted_prod[prod_name]
        prod = Member.objects.get(telegram_id=chat_id).product_set.filter(prod_type=prod_type).first()
        if prod == None:
            raise Product.DoesNotExist
        quantity = state.quantity
        prod.quantity = quantity
        prod.save()

        filename = str(chat_id) + '_confirm_change'
        path = os.path.join(dir_path, 'output', f'{filename}.ogg')
        if LANG == "fr" or LANG == "bm":
            concat_audios([os.path.join(dir_path, 'audio', f'confirm_change1_{LANG}.ogg'), os.path.join(dir_path, 'audio', f'{prod_type}_{LANG}.opus'), os.path.join(dir_path, 'audio', f'confirm_change2_{LANG}.ogg')], path)
        if LANG == "mo":
            concat_audios([os.path.join(dir_path, 'audio', 'change_quantity_of_1mo.opus'), os.path.join(dir_path, 'audio', f'{prod_type}_mo.opus') ,os.path.join(dir_path, 'audio', 'change_quantity_of_2mo.opus')], path)
            bot.send_message(message.chat.id, "La quantité de " + prod_name + " a bien été changé. Voulez-vous changer un autre stock ?")
            # text =  prod_name  + " kosma zislma sid tekamé. Yam’b  n’dati toema bumb a too bi ?"
            # speaker.speak(text, filename)
        send_voice_message(filename, path, message.chat.id)
        if os.path.exists(path):
            os.remove(path)

        state.state = "generate_communique"
        state.save()
        send_yes_no_keyboard(chat_id)



    except (State.DoesNotExist, Product.DoesNotExist):
        filename = f'error_try_again_{LANG}.opus'
        path = os.path.join(dir_path, 'audio', filename)
        send_voice_message(filename, path, message.chat.id)
        start(message)


def generate_communique(message):
    """
    User wants to generate a communique
    """
    try:
        state = State.objects.get(telegram_id=message.chat.id)
        audios_to_concat = []
        coop = Member.objects.get(telegram_id=message.chat.id).coop
        product_list = []
        if coop.get_total_quantity_first_product() > 0:
            product_list.append(coop.offered_product_1)
        if coop.get_total_quantity_second_product() > 0:
            product_list.append(coop.offered_product_2)
        if coop.get_total_quantity_third_product() > 0:
            product_list.append(coop.offered_product_3)

        audios_to_concat = make_commpfnl_communique(LANG, coop.coop_name, coop.coop_phone, product_list)

        filename = str(message.chat.id) + '_communique'
        path = os.path.join(dir_path, 'output', f'{filename}.opus')
        concat_audios(audios_to_concat, path)
        send_voice_message(filename, path, message.chat.id)
        if os.path.exists(path):
            os.remove(path)

        state.state = "None"
        state.save()


    except (State.DoesNotExist, Member.DoesNotExist, Cooperative.DoesNotExist):
        filename = f'error_try_again_{LANG}.opus'
        path = os.path.join(dir_path, 'audio', filename)
        send_voice_message(filename, path, message.chat.id)
        start(message)


@bot.message_handler(func=lambda msg: True)
def intercept_message(message):
    telegram_id = message.chat.id
    try:
        state = State.objects.get(telegram_id=telegram_id)
        state_name = state.state
        if state.time_set + timedelta(minutes=EXPIRATION_MINUTES) < datetime.now(timezone): # expires after 20 minutes
            state.state = "product_list"
            state.save()

        if state_name == "contact":
            is_phone_number(message)
        elif state_name == "None" or state_name == "product_list":
            show_products(message)
        elif state_name == "product":
            if message.text in list(PRODUCT_TYPES[LANG].values()):
                edit_product(message)
            else:
                filename = f'select_product_{LANG}.opus'
                path = os.path.join(dir_path, "audio", filename)
                send_voice_message(filename, path, message.chat.id)
        elif state_name == "quantity":
            if message.text.isnumeric():
                edit_quantity(message)
            else:
                quantity_incorrect(message)
        elif state_name == "confirm":
            if YES_NO[LANG]["yes"] in message.text.lower():
                edit_product(message)
            elif YES_NO[LANG]["no"] in message.text.lower():
                show_products(message)
            else:
                send_yes_no_keyboard(message.chat.id)
        elif state_name == "generate_communique":
            if YES_NO[LANG]["yes"] in message.text.lower():
                show_products(message)
            elif YES_NO[LANG]["no"] in message.text.lower():
                generate_communique(message)
            else:
                send_yes_no_keyboard(message.chat.id)


    except State.DoesNotExist:
        new_state = State(telegram_id=telegram_id, state="product_list")
        new_state.save()
        show_products(message)


