import json
import datetime
import re
import pprint


regexp = r'\(.*\)|\(\d+・.*・.*\)$|\s|　| |\「|\」|\【|\】|\『|\』|\<|\>|\〈|\〉|\/|\[|\]|\.|\,|\_|\-|\−|\―|\‐|\‐|\‐|\{|\}|\ー|\、|\?|\!|\。|\〜|\～|\~|\・'


def create_titles():
    titles = {}

    with open('../trim/jfdb_after2003.jsonlines') as f:
        for row in f.readlines():
            obj = json.loads(row)
            title = re.sub(regexp, "", obj['タイトル']).translate(
                str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
            f = '%Y年%m月%d日'
            r = obj['公開年月日']
            if '月' not in r:
                r += '1月'
            if '日' not in r:
                r += '1日'
            date = datetime.datetime.strptime(r, f)
            release_date = f'{date.date()}'
            if title in titles:
                if release_date not in titles[title]:
                    titles[title].append(release_date)
            if title not in titles:
                titles[title] = [release_date]

    with open('../trim/jcdb_after2003.jsonlines') as f:
        for row in f.readlines():
            obj = json.loads(row)
            title = re.sub(regexp, "", obj['タイトル']).translate(
                str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
            release_date = obj['公開年月日'].replace(
                '年', '-').replace('月', '-').replace('日', '')
            if title in titles:
                if release_date not in titles[title]:
                    titles[title].append(release_date)
            if title not in titles:
                titles[title] = [release_date]

    with open('titles.json', mode='w', encoding='utf_8') as f:
        json.dump(titles, f, ensure_ascii=False)


def create_better_revenue():
    with open('income.json', encoding='utf_8') as f_r:
        data = json.load(f_r)
        for year in data.keys():
            for d in data[year]:
                releaseDate = d['releaseDate']
                if len(releaseDate) == 6:
                    d['releaseDate'] = releaseDate[:5] + '0' + releaseDate[5:]
                d['title'] = re.sub(regexp, "", d['title']).translate(
                    str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        with open('revenue_better_date.json', mode='w', encoding='utf_8') as f_w:
            json.dump(data, f_w, ensure_ascii=False)


def search():
    revenue = None
    titles = None
    revenue_count = 0
    count = 0
    title_not_included = []
    same_title_different_date = []
    with open('./revenue_better_date.json') as fi:
        revenue = json.load(fi)
    with open('./titles.json') as ft:
        titles = json.load(ft)
    for year in revenue.keys():
        for item in revenue[year]:
            revenue_count += 1
            title = item['title']
            release_date = item['releaseDate']
            if title in titles:
                t = []
                for d in titles[title]:
                    t.append(d[:7])
                if release_date in t:
                    count += 1
                else:
                    same_title_different_date.append(
                        {'title': title, 'revenue_date': release_date, 'detected_date': titles[title]})
            else:
                title_not_included.append(title)

    print('\ntitles not included')
    pprint.pprint(title_not_included)
    print('\ntitles same title different date')
    pprint.pprint(same_title_different_date)
    print('rate', count / revenue_count)
    print('included count', count)
    print('revenue count', revenue_count)
    print('titles not included count:', len(title_not_included))
    print('titles same title different date count:',
          len(same_title_different_date))


create_titles()
create_better_revenue()
search()
