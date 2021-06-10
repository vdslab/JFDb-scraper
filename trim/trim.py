import pandas as pd
import re


def trim(file_name, txt_name):
    ZEN = "".join(chr(0xff01 + i) for i in range(94))
    HAN = "".join(chr(0x21 + i) for i in range(94))
    ZEN2HAN = str.maketrans(ZEN, HAN)

    data_lines = pd.read_json(file_name, orient='records', lines=True)
    with open(txt_name, mode="w", encoding="UTF-8") as f:
        for i in range(len(data_lines["タイトル"])):
            ymd = data_lines["公開年月日"][i]
            if ymd == "未定" or ymd == "" or int(ymd[:4]) >= 2003:
                text = str(data_lines["タイトル"][i] + "\n")
                text = text.translate(ZEN2HAN)
                text = re.sub(
                    r'　| |・|「|」|【|】|『|』|<|>|〈|〉|\/|\[|\]|\.|,|_|-|−|ー|、|。|〜|～|~|\(\d+\)', "", text)
                f.write(text)
            elif int(ymd[:4]) < 2003:
                pass
            else:
                print("error")


trim("jfdb.jsonlines", "jfdbTrim.txt")
trim("jcdb.jsonlines", "jcdbTrim.txt")
