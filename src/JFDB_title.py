import re
import requests
from bs4 import BeautifulSoup
import json
import jsonlines
# それぞれのslizeの添え字は汚い書き方しているけど合っている。ただすったっふまわりのデータの取り方に苦しむ
# h2で書かれているものに統一性はなく、<p>で空白をとっている部分があるんじょでfind_all("<p>")ではずれが生じる
# movieであらかじめdirecterなど書いているがその情報がない場合もあるので最初に書いててもそれのすり合わせがしんどい。
# scrapyでやった方がいいのだろうか、ここまでごり押しでやってきたがあまりにも無謀すぎたのかもしれない。
# スタッフ以外のデータは基本的に取れているため（字幕データは取ってない、それ以前の問題）

all_movie = []
# for num in range(0, 6237//25):  # 6237は現在の映画の数。動的にしたいなら指定して持ってくる

with jsonlines.open('jfdb_title.jsonlines', mode='w') as writer:
    for num in range(0, 251):
        print(num)
        url = f"https://jfdb.jp/search?KW=&PAGE={num}"
        res = requests.get(url)
        # print(res.text)
        soup = BeautifulSoup(res.content, "html.parser")

        elems = soup.find_all(href=re.compile("/title/\d+"))  # ここの正規表現が雑

        # print("####################################################################################")
        for i in range(1, len(elems)+1, 2):  # 214pageの時に3桁になってバグるの直さなきゃ もともと50
            print("  ", i)
            movie = {
                "タイトル": "",

            }
            title_name = ""
            # for j in range(len(elems[i].contents[0].string.split(","))):
            #     # print(elems[i].contents[0].string.split(","))
            #     for k in range(len(elems[i].contents[0].string.split(",")[j].split())):
            #         title_name += elems[i].contents[0].string.split(",")[
            #             j].split()[k]

            #     if k+1 != len(elems[i].contents[0].string.split(",")[j].split()):
            #         title_name += " "

            movie["タイトル"] = elems[i].contents[0][9:-9]  # 空白の取り除き

            all_movie.append(movie)

            writer.write(movie)

# JSONファイルのロード
with open('jfdb.jsonlines', 'r',  encoding="utf-8_sig") as f:
    json_output = json.load(f)


# print(Details_elems)

# print(len(alltitle))
# print(len(alltitle))
