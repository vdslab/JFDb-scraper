import csv
import pprint
import json
import jsonlines
all_ = 0
count = 0
with jsonlines.open('./jfdb.jsonlines') as reader:
    for obj in reader:
        if obj["公開年月日"] == "未定" or int(obj["公開年月日"][:4]) >= 2003:
            all_ += 1
            if len(obj["image"]) == 0:
                count += 1
print(all_)
print(count)
print(all_/count)
