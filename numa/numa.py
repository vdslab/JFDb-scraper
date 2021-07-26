import json
import csv

data = None

with open('trim/seedData.json') as f:
    data = json.load(f)

with open('numa/numa.csv', mode='w', encoding='utf_8_sig') as f:
    writer = csv.writer(f)
    writer.writerow(['年', '俳優名'])

    for movie in data:
        year = movie['releaseDate'][:4]
        for actor in movie['cast']:
            name = actor['name']
            writer.writerow([year, name])
