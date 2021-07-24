import json
import csv

data = None

with open('../trim/seedData.json', encoding='utf_8_sig') as f:
    data = json.load(f)

with open('../saaya/saaya.csv', mode='w', encoding='utf_8_sig', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['年', '制作会社', '個数'])
    box = {}
    for year in range(2003, 2021+1):
        box[f"{year}"] = {}
    for movie in data:
        year = movie['releaseDate'][:4]
        for company in movie['company']:
            if company not in box[year]:
                box[f"{year}"][company] = 1
            else:
                box[f"{year}"][company] += 1

    for year in range(2003, 2021+1):
        for company, count in box[f"{year}"].items():
            writer.writerow([f"{year}", company, count])
