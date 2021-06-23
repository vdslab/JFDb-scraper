import pandas as pd
import re


def trim(file_name, txt_name):
    ZEN = "".join(chr(0xff01 + i) for i in range(94))
    HAN = "".join(chr(0x21 + i) for i in range(94))
    ZEN2HAN = str.maketrans(ZEN, HAN)

    data_lines = pd.read_json(file_name, orient='records', lines=True)
    with open(txt_name, mode="w", encoding="UTF-8") as f:
        for i in range(len(data_lines["タイトル"])):
            text = data_lines["タイトル"][i] + "\n"
            text = text.translate(ZEN2HAN)
            text = text.lower()
            text = re.sub(
                r'　| |\・|\「|\」|\【|\】|\『|\』|\<|\>|\〈|\〉|\/|\[|\]|\.|\,|\_|\-|\−|\―|\‐|\‐|\‐|\{|\}|\ー|\、|\?|\!|\。|\〜|\～|\~|\(\d+.*\)', "", text)
            f.write(text)


trim("jfdb_after2003.jsonlines", "jfdb_trim.txt")
trim("jcdb_after2003.jsonlines", "jcdb_trim.txt")
