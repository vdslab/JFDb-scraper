import csv
import pprint
import json
import re
import jsonlines
all_ = 0
count = 0
with open('./income.json', encoding='utf_8_sig', mode='r') as f:
    json_open = json.load(f)
    # print(json_open)
    income_data = []
    for year in range(2003, 2021):
        for year_data in json_open[f"{year}"]:
            text = year_data["title"]
            text = re.sub(
                r'　| |\・|\「|\」|\【|\】|\『|\』|\<|\>|\〈|\〉|\/|\[|\]|\.|\,|\_|\-|\−|\―|\‐|\‐|\‐|\{|\}|\ー|\、|\?|\!|\。|\〜|\～|\~|\(\d+.*\)', "", text)

            income_data.append(text)

    income_count = 0
    income_judge = [0]*len(income_data)
    with jsonlines.open('./jfdb.jsonlines') as reader:
        for obj in reader:
            title = obj["タイトル"]
            title = re.sub(
                r'　| |\・|\「|\」|\【|\】|\『|\』|\<|\>|\〈|\〉|\/|\[|\]|\.|\,|\_|\-|\−|\―|\‐|\‐|\‐|\{|\}|\ー|\、|\?|\!|\。|\〜|\～|\~|\(\d+.*\)', "", title)
            for i in range(len(income_data)):
                if title == income_data[i]:
                    income_count += 1
                    income_judge[i] += 1

        for i in range(len(income_judge)):
            if income_judge[i] == 0:
                print(income_data[i])

        print(len(income_data))
        print(income_count)

    income_count = 0
    income_judge = [0]*len(income_data)
    with jsonlines.open('../trim/jcdb_after2003.jsonlines') as reader:
        for obj in reader:
            title = obj["タイトル"]
            title = re.sub(
                r'　| |\・|\「|\」|\【|\】|\『|\』|\<|\>|\〈|\〉|\/|\[|\]|\.|\,|\_|\-|\−|\―|\‐|\‐|\‐|\{|\}|\ー|\、|\?|\!|\。|\〜|\～|\~|\(\d+.*\)', "", title)
            for i in range(len(income_data)):
                if title == income_data[i]:
                    income_count += 1
                    income_judge[i] += 1

        for i in range(len(income_judge)):
            if income_judge[i] == 0:
                print(income_data[i])

        print(len(income_data))
        print(income_count)
