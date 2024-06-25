from pydub import AudioSegment
from bot.num_to_text import NumToWords
from bot.num_to_text_bm import NumToWordsBambara
from pfnl.models import Cooperative

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def concat_audios(filenames, output_file):
    """
    Concatenates audio files from a list of names and saves the result in the specified output file,
    format ogg
    """
    # print(filenames)
    combined_audio = AudioSegment.from_file(filenames[0], format="ogg")
    for filename in filenames[1:]:
        sound = AudioSegment.from_file(filename, format="ogg")
        combined_audio += sound

    # simple export
    file_handle = combined_audio.export(output_file, format="ogg")

def get_cooperative_audio_name(name):
    try:
        file_path = Cooperative.objects.get(coop_name=name).name_audio
        return [file_path]
    except:
        return []

def make_commpfnl_communique(lang, name, phone, list_products):
    audios = [os.path.join(dir_path, "audio", f"communique1_{lang}.opus")]

    audios += get_cooperative_audio_name(name)

    audios.append(os.path.join(dir_path, "audio", f"communique2_{lang}.opus"))
    for prod_type in list_products:
        audios.append(os.path.join(dir_path, "audio", f'{prod_type}_{lang}.opus'))
    audios.append(os.path.join(dir_path, "audio", f"communique3_{lang}.opus"))
    speaker = NumToWords()
    spoken_phone_number = speaker.speak_phone_number(phone)
    audios += spoken_phone_number
    return audios


def make_artemisia_commmunique(lang, name, phone, list_products):
    audios = [f"./audio/communique1_{lang}.opus"]
    # TODO: add name

    audios.append(f"./audio/communique2_{lang}.opus")
    for prod in list_products.values():
        qtty = int(prod[2])
        if (qtty > 0):
            prod_type = prod[1]
            audios.append(f'./audio/{prod_type}_{lang}.opus')
    audios.append(f"./audio/communique3_{lang}.opus")
    speaker = NumToWordsBambara()
    spoken_phone_number = speaker.speak_phone_number(phone)
    audios += spoken_phone_number
    audios.append(f"./audio/communique4_{lang}.opus")
    audios += spoken_phone_number
    return audios