import csv
import pprint
import json
import re
import jsonlines
all_ = 0
count = 0
with jsonlines.open('jfdb_db.jsonlines', mode='w') as writer:
    with jsonlines.open('./jfdb.jsonlines') as reader:
        for obj in reader:
            movie = {
                "id": None,
                "title": None,
                "release": None,
                "time": None,
                "staff": [],
                "cast": [],
                "company": [],
                "example": None,
                "site": None,
                "awards": []
            }
            movie["id"] = obj["id"]
            movie["title"] = obj["タイトル"]
            date = re.split('[年月]', obj["公開年月日"][:-1])
            for i in range(len(date)):
                if len(date[i]) == 1:
                    date[i] = "0"+date[i]
            movie["release"] = "-".join(date)

            # print("1", obj["スタッフ"])
            if obj["上映時間"] == "未定":
                movie["time"] = obj["上映時間"]
            else:
                movie["time"] = int(obj["上映時間"][:-1])
            for i in range(len(obj["スタッフ"])):
                dust = obj["スタッフ"][i].pop("id")
                if obj["スタッフ"][i]["職種"] != "監督":
                    if obj["スタッフ"][i]["役割"] != "":
                        obj["スタッフ"][i]["職種"] = obj["スタッフ"][i]["役割"]
                    dust = obj["スタッフ"][i].pop("役割")
                obj["スタッフ"][i]["name"] = obj["スタッフ"][i]["名前"]
                obj["スタッフ"][i]["occupation"] = obj["スタッフ"][i]["職種"]
                dust = obj["スタッフ"][i].pop("名前")
                dust = obj["スタッフ"][i].pop("職種")
            movie["staff"] = obj["スタッフ"]
            company = []
            company_ = []
            for i in range(len(obj["制作会社"])):
                company_.append(obj["制作会社"][i])
            company.append({"title": company_, "type": "制作会社"})
            company_ = []
            for i in range(len(obj["製作会社"])):
                company_.append(obj["製作会社"][i])
            company.append({"title":  company_, "type": "製作会社"})

            company_ = []
            for i in range(len(obj["配給会社（国内）"])):
                company_.append(obj["配給会社（国内）"][i])
            company.append(
                {"title":  company_, "type": "配給会社"})

            movie["company"] = company
            for i in range(len(obj["出演者"])):
                obj["出演者"][i]["name"] = obj["出演者"][i]["名前"]
                obj["出演者"][i]["occupation"] = obj["出演者"][i]["役割"]
                dust = obj["出演者"][i].pop("名前")
                dust = obj["出演者"][i].pop("役割")
            movie["cast"] = obj["出演者"]

            # print(movie["])
            movie["example"] = obj["説明"]
            movie["site"] = obj["公式サイト"]
            movie["award"] = obj["映画祭・受賞歴"]
            # print("2", movie["staff"])

            writer.write(movie)

    # print(count)
