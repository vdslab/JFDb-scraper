# coding: utf-8
import csv
import pprint
import json
# print([json.dumps(l) for l in csv.DictReader(open('data2.csv'))])

json_list = {}
for i in range(2003, 2021):
    json_list[f"{i}"] = []
# print(json_list)
count = 0
number = 0
now = -1  # 今どこの番号にいるか
# CSV ファイルの読み込み
for year in range(2003, 2021):
    data = []
    jugh = False  # 上陸してるかの判定変数
    number = 0
    now = -1  # 今どこの番号にいるか
    with open('../income/{}.csv'.format(year), 'r', encoding="utf-8_sig") as f:
        # print(f, )
        for row in csv.DictReader(f):
            data.append(row)
        print(data)
        for k in range(len(data)):
            json_list[f"{year}"].append(
                {
                    "title": data[k]["title"],
                    "revenue": float(data[k]["revenue"]),
                    "releaseDate": data[k]["releaseDate"]
                }
            )

    # JSON ファイルへの書き込み
with open('income.json', 'w',  encoding="utf-8_sig") as f:
    json.dump(json_list, f, ensure_ascii=False)

# JSONファイルのロード
with open('income.json', 'r',  encoding="utf-8_sig") as f:
    json_output = json.load(f)
