from math import floor
# import phonenumbers
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class NumToWords:
    """
    Simple class to get the written out version of number in Mooré
    """
    one = "yembre"
    units = ["zaalem", "yen", "yiibu", "tãabo", "naase", "nu", "yoobe", "yopoe", "nii", "wɛ"]
    ten = "piiga"
    tens = ["", "pig", "pisi", "pista", "pis nasse", "pis nu", "pis yoobe", "pis yopoe", "pis nii", "pis wɛ"]
    hundred = "koabga"
    hundreds = ["", "koabg", "kobisi", 'kobis tã', 'kobis nasse', 'kobis nu', 'kobis yoobe', 'kobis yopoe', 'kobis nii', 'kobis wɛ']
    thousand = 'tusri'
    thousands = 'tusr'


    def transcribe(self, num):
        """
        Writes out a number in Mooré, ONLY FROM 0 TO 999 999
        """
        if num == 1:
            return [self.one]
        if num < 10:
            return [self.units[num]]
        if num == 10:
            return [self.ten]
        if num < 100:
            unit = num%10
            dec = floor(num/10)
            if unit == 0:
                return [self.tens[dec]]
            return [self.tens[dec], "la", self.units[unit]]
        if num == 100:
            return [self.hundred]
        if num < 1000:
            unit = num%10
            hun = floor(num/100)
            dec = floor((num-hun*100)/10)
            if dec == 0 and unit ==0:
                return [self.hundreds[hun]]
            rest = str(dec) + str(unit)
            return [self.hundreds[hun], "la"] + self.transcribe(int(rest))
        if num == 1000:
            return [self.thousand]
        if num < 1000000:
            thou = floor(num/1000)
            rest = num % 1000
            if (rest == 0):
                return [self.thousands, "a"] + self.transcribe(thou)
            else:
                if (thou == 1):
                    return [self.thousands, "la"] + self.transcribe(rest)
                return [self.thousands, "a"] +  self.transcribe(thou) + ["la"] + self.transcribe(rest)

    def transcribe_for_phone(self, num):
        """
        Returns a list of numbers, to be read out
        """
        if num == 1:
            return [self.units[0], self.one]
        if num < 10:
            return [self.units[0], self.units[num]]
        if num == 10:
            return [self.ten]
        if num < 100:
            unit = num%10
            dec = floor(num/10)
            if unit == 0:
                return [self.tens[dec]]
            return [self.tens[dec], "la", self.units[unit]]

    def speak_phone_number(self, phone_number):
        phone_number = phone_number.as_national
        formatted_number = phone_number.split(' ')
        number_audios = []
        for sub_number in formatted_number:
            sub_res = self.transcribe_for_phone(int(sub_number))
            number_audios += [os.path.join(dir_path, "audio", "numbers_moore" , x + ".opus") for x in sub_res]
            number_audios.append(os.path.join(dir_path, "audio", "pause.opus"))
        return number_audios