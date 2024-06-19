from math import floor
import phonenumbers

class NumToWordsBambara:
    """
    Simple class to get the written out version of number in Bambara
    """

    units = ["", "kelen", "fila", "saba", "naani", "duuru", "wɔɔrɔ", "wolonwula", "seegin", "kɔnɔntɔn"]
    tens = ["", "tan", "mugan", "bi saba", "bi naani", "bi duuru", "bi wɔɔrɔ", "bi wolonwula", "bi seegin", "bi kɔnɔntɔn"]
    hundred = "kɛmɛ" 
    thousand = 'waa'
    million = "mílyɔn"

    def preprocess_number(self, num):
        """
        Spells a number in Bambara for audio creation
        """
        if num < 10:
            return [str(num)]
        if num <= 100:
            unit = num%10
            dec = floor(num/10)
            if unit == 0:
                return [str(dec) + "0"]
            return [str(dec) + "0", "and", str(unit)]
        if num <= 1000:
            unit = num%10
            hun = floor(num/100)
            dec = floor((num-hun*100)/10)
            if dec == 0 and unit ==0:
                return ["100", str(hun)]
            rest = str(dec) + str(unit)
            if hun ==1:
                return ["100", "and"] + self.preprocess_number(int(rest))
            return ["100",  str(hun), "and"] + self.preprocess_number(int(rest))
        if num < 1000000:
            thou = floor(num/1000)
            rest = num % 1000
            if (rest == 0):
                return ["1000"] + self.preprocess_number(thou)
            return ["1000"] +  self.preprocess_number(thou) + ["and"] + self.preprocess_number(rest)
        
    def speak(self, num):
        raw_res = self.preprocess_number(num)
        res = ["./audio/numbers_bambara/" + x + "_bm.opus" for x in raw_res]
        # concat_audios(res, f"./output/{file_name}.opus")
        return res
    
    def speak_phone_number(self, phone):
        phone_number = phonenumbers.parse(phone, "ML")
        formatted_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL).split(' ')
        number_audios = []
        for sub_number in formatted_number:
            sub_number = int(sub_number)
            if sub_number < 10:
                number_audios.append("./audio/numbers_bambara/0_bm.opus")
            sub_res = self.preprocess_number(int(sub_number))
            number_audios += ["./audio/numbers_bambara/" + x + "_bm.opus" for x in sub_res]
            number_audios.append("./audio/pause.opus")
        return number_audios


    def transcribe(self, num):
        """
        Writes out a number in Bambara, ONLY FROM 0 TO 999 999
        """
        if num < 10:
            return self.units[num]
        if num <= 100:
            unit = num%10
            dec = floor(num/10)
            if unit == 0:
                return self.tens[dec]
            return self.tens[dec] + " ni " + self.units[unit]
        if num <= 1000:
            unit = num%10
            hun = floor(num/100)
            dec = floor((num-hun*100)/10)
            if dec == 0 and unit ==0:
                return self.hundred + " " + self.units[hun]
            rest = str(dec) + str(unit)
            if hun ==1:
                return self.hundred + " ni " + self.transcribe(int(rest))
            return self.hundred + " " + self.units[hun] + " ni " + self.transcribe(int(rest))
        if num < 1000000:
            thou = floor(num/1000)
            rest = num % 1000
            if (rest == 0):
                return self.thousand + " " + self.transcribe(thou)
            return self.thousand + " " +  self.transcribe(thou) + " ni " + self.transcribe(rest)
