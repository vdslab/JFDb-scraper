import csv
import pprint
import json
import jsonlines
z = 1
co_play_count = {}  # 共演者自体の数
count_dict = {}  # 共演回数
id_list = set()
id_name_dict = {}
with jsonlines.open('./jfdb.jsonlines') as reader:
    for obj in reader:
        allcast = []
        z += 1
        if z == 10:
            print(count_dict)
        if len(obj["出演者"]) != 0:
            for cast in obj["出演者"]:
                id_list.add(cast["id"])
                id_name_dict[cast["id"]] = cast["名前"]
                allcast.append(cast["id"])
            allcast.sort()
            for i in range(len(allcast)-1):  # ここらへん添え字だから許して
                if f"{allcast[i]}" not in count_dict:
                    count_dict[f"{allcast[i]}"] = {}
                for j in range(i+1, len(allcast)):
                    if f"{allcast[j]}" in count_dict[f"{allcast[i]}"]:
                        count_dict[f"{allcast[i]}"][f"{allcast[j]}"] += 1
                    else:
                        count_dict[f"{allcast[i]}"][f"{allcast[j]}"] = 1

                        if f"{allcast[i]}" not in co_play_count:  # 次数とエッジの数のため
                            co_play_count[f"{allcast[i]}"] = 1
                        else:
                            co_play_count[f"{allcast[i]}"] += 1
                        if f"{allcast[j]}" not in co_play_count:
                            co_play_count[f"{allcast[j]}"] = 1
                        else:
                            co_play_count[f"{allcast[j]}"] += 1

with open('jfdb_network_info.csv', encoding='utf_8_sig', mode='w', newline="") as f_w:
    writer = csv.writer(f_w)
    write_data = [['次数', '個数']]
    data = [0]*10001
    for id, num in co_play_count.items():
        data[num] += 1
        if num == 164:
            print(id_name_dict[f"{id}"])

    for i in range(1, 164+1):
        write_data.append([i, data[i]])
    writer.writerows(write_data)

with open('jfdb_release.csv', encoding='utf_8_sig', mode='w', newline="") as f_w:
    with jsonlines.open('./jfdb.jsonlines') as reader:
        writer = csv.writer(f_w)
        write_data = [['年',  '個数']]
        release = [0]*2050
        for obj in reader:
            if "年" in obj["公開年月日"] and "月" in obj["公開年月日"]:
                year = obj["公開年月日"].split("年")
                month_date = year[1]
                year = year[0]
                month, date = month_date.split("月")
                release[int(year)] += 1
        for year in range(1941, 2021+1):
            write_data.append([year, release[year]])

    writer.writerows(write_data)
id_count = 1
header2 = ["Source", "Target", "Type", "Weight", "Label"]
header1 = ["id", "Label"]
takeru_strring = set()
with open('./jfdb_edgh_pinko.csv', encoding='utf_8_sig', mode='w', newline="") as f_w:
    writer = csv.writer(f_w)
    w = [header2]
    for id1, dict_ in count_dict.items():
        for id2, count_ in dict_.items():
            if "8106" == id1 or "8106" == id2:
                r1 = []
                r1.append(id1)
                takeru_strring.add(id1)
                takeru_strring.add(id2)
                r = []
                r.append(id1)
                r.append(id2)
                r.append("Undirected")
                r.append(count_)
                r.append(id_count)
                w.append(r)

                id_count += 1
    for id1, dict_ in count_dict.items():
        for id2, count_ in dict_.items():
            if id1 in takeru_strring and id2 in takeru_strring:
                r1 = []
                r1.append(id1)
                r = []
                r.append(id1)
                r.append(id2)
                r.append("Undirected")
                r.append(count_)
                r.append(id_count)
                w.append(r)
    writer.writerows(w)

with open('./jfdb_node_pinko.csv', encoding='utf_8_sig', mode='w', newline="") as f_w:
    writer = csv.writer(f_w)
    w = [header1]
    for id_, name in id_name_dict.items():
        if id_ in takeru_strring:
            w.append([id_, name])

    writer.writerows(w)


# print(co_play_count)
# print(count_dict)

# json_load = json.load(f_r)
# print(json_load)
