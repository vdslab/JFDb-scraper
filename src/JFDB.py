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

with jsonlines.open('jfdb.jsonlines', mode='w') as writer:
    for num in range(1, 251):
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
                "id": "",
                "タイトル": "",
                "予告動画": "",
                "image": [],
                "公開年月日": "",
                "上映時間": "",
                "カテゴリー": [],
                "カラー": "",
                "フォーマット": "",
                "スタッフ": [],
                "出演者": [],
                "製作会社": [],
                "説明": "",
                "公式サイト": [],
                "映画祭・受賞歴": []
            }
            # print(elems[i].contents[0][9:-9])
            movie["タイトル"] = elems[i].contents[0][9:-9]  # 空白の取り除き
            movie["id"] = elems[i].attrs['href'][7:]  # id部分の抽出
            # ここは映画の詳細ページのurl
            Details_url = f"https://jfdb.jp{elems[i].attrs['href']}"
            Details_res = requests.get(Details_url)
            Details_soup = BeautifulSoup(Details_res.content, "html.parser")

            # 画像らへんを扱っている
            Details_elems = Details_soup.find(
                "div", attrs={"class": "col-12 col-lg-4 title-photo"})
            Details_elems_image = Details_elems.find_all(
                "img")

            Details_elems_movie = Details_elems.find("a")
            for image_index in range(len(Details_elems_image)):  # 動画のリンクになってない
                all_image = {}
                if Details_elems_movie != None and image_index == 0:
                    movie["予告動画"] = Details_elems_movie.attrs['href']
                elif Details_elems_image[image_index].attrs['src'] != "//jfdb.jp/global/images/jfdb_noimage.png":
                    all_image["url"] = Details_elems_image[image_index].attrs['src']
                    all_image["caption"] = Details_elems_image[image_index].attrs['title']
                    movie["image"].append(all_image)
            ###

            Details_elems = Details_soup.find(
                "div", attrs={"class": "col-12 col-lg-8 title-detail"})

            # 公開日らへんのデータを扱っている
            Details_elems_dl = Details_elems.find_all(
                "dl")
            movie["公開年月日"] = str(Details_elems_dl[0].contents[3])[5:-5]
            movie["上映時間"] = str(
                Details_elems_dl[1].contents[3])[11:-13]
            for genre_index in range(len(Details_elems_dl[2].contents[3].find_all("a"))):
                movie["カテゴリー"].append(
                    Details_elems_dl[2].contents[3].find_all("a")[genre_index].contents[0])
            movie["カラー"] = str(Details_elems_dl[3].contents[3])[4:-5]
            movie["フォーマット"] = str(Details_elems_dl[4].contents[3])[4:-5]
            ###

            # 監督　プロデューサーなど
            person_elems_title = Details_elems.find_all(
                "h2")
            # print("############################################################")
            for i in range(len(person_elems_title)):
                title = person_elems_title[i].string[1:-1]
                data = Details_elems.find_all(
                    "h2")[i].next_sibling.next_sibling
                # print(person_elems_title[i].string[1:-1])
                # print(Details_elems.find_all(
                #     "h2")[i].next_sibling.next_sibling)

                if title == "監督":
                    # print(data)
                    for index in range(len(data.find_all("li"))):
                        name = data.find_all("li")[index].find("a").string
                        name_id = data.find_all("li")[index].find(
                            "a").attrs["href"][8:]
                        movie["スタッフ"].append(
                            {"name": f"{name}", "name_id": f"{name_id}", "職種": "監督"})

                elif title == "プロデューサー":
                    for index in range(len(data.find_all("li"))):
                        name = data.find_all("li")[index].find("a").string
                        name_id = data.find_all("li")[index].find(
                            "a").attrs["href"][8:]
                        position = str(data.find_all("li")[
                            index].find('span'))[10:-7]
                        movie["スタッフ"].append(
                            {"名前": f"{name}", "id": f"{name_id}", "職種": "プロデューサー", "役割": f"{position}"})

                elif title == "キャスト":
                    for index in range(len(data.find_all("li"))):
                        name = data.find_all("li")[index].find("a").string
                        name_id = data.find_all("li")[index].find(
                            "a").attrs["href"][8:]
                        position = str(data.find_all("li")[
                            index].find('span'))[10:-7]
                        movie["出演者"].append(
                            {"名前": f"{name}", "id": f"{name_id}", "役割": f"{position}"})

                elif title == "スタッフ":
                    for index in range(len(data.find_all("li"))):
                        name = data.find_all("li")[index].find("a").string
                        name_id = data.find_all("li")[index].find(
                            "a").attrs["href"][8:]
                        position = str(data.find_all("li")[
                            index].find('span'))[10:-7]
                        movie["スタッフ"].append(
                            {"名前": f"{name}", "id": f"{name_id}", "職種": "スタッフ", "役割": f"{position}"})

                elif title == "製作会社":
                    # print("3333333333333333333333333333333333333333333333333333333333333")
                    # print(data)
                    # print("3333333333333333333333333333333333333333333333333333333333333")
                    # print(data.string.split())
                    # print("3333333333333333333333333333333333333333333333333333333333333")
                    # print(data.contents[0].split(","))
                    all_company = []
                    for index in range(len(data.contents[0].split(","))):
                        box = data.contents[0].split(",")[index].split()[0]
                        for space_index in range(1, len(data.contents[0].split(",")[index].split())):
                            box += " "
                            box += data.contents[0].split(
                                ",")[index].split()[space_index]
                        all_company.append(box
                                           )
                    movie["製作会社"] = all_company

                    # a for a in data.find_all("p")
                    # .split(",").stripped_string

                elif title == "解説":

                    # print(data.text.split()
                    all_explanation = ""
                    for index in range(len(data.text.split())):
                        all_explanation += data.text.split()[index]

                    movie["説明"] = all_explanation

                elif title == "公式サイト":
                    movie["公式サイト"] = data.find(
                        "a").attrs["href"]

                elif title == "映画祭・受賞歴":
                    # print(
                    #     "33333333333333333333333333333333       3333333333333333333333333333333333333333333333333333333333333333333")
                    movie["映画祭・受賞歴"] = [i.strip().replace("\u3000", " ")
                                        for i in data.text.splitlines() if i.strip() != ""]
                    # l = [i.strip() for i in data.text.splitlines()]
                    # print([i for i in l if i != ""])
                    # all_awards = ""
                    # for index in range(len(data.text.split())):
                    #     all_explanation += data.text.split()[index].split()

                    # movie["awards"] = all_awards

                    # [print(tag) for tag in person_elems_title.stripped_strings]
            person_elems_person = Details_elems.find_all(
                "ul")
            # people_index派名前変えた方がいい、実際は
            for people_index in range(len(person_elems_person)):
                for people_about_index in range(len(person_elems_person[people_index].find_all("li"))):
                    name = person_elems_person[people_index].find_all(
                        "li")[people_about_index].find("a").contents[0]
                    # print(name)
                    name_id = person_elems_person[people_index].find_all(
                        "li")[people_about_index].find("a").attrs["href"][8:]
                    # if "監督" in data:  # ここら辺の条件式はliでくくってあるデータが監督、プロデューサー、キャスト、スタッフの四つであり、目視のうちはあるから
                    #     # 追記　それぞれあるデータとないデータがあるっぽい、そこがバラバラに書かれていて途方がなくていったんショートする。ここの条件式のコードはもういらない
                    #     movie["directer"].append(
                    #         {"name": f"{name}", "name_id": f"{name_id}", })
                    # if people_index == 1:

                    #     position = str(person_elems_person[people_index].find_all(
                    #         "li")[people_about_index].find('span'))[10:-7]
                    #     movie["producer"].append(
                    #         {"name": f"{name}", "name_id": f"{name_id}", "position": f"{position}"})

                    # if people_index == 2:
                    #     official_name = str(person_elems_person[people_index].find_all(
                    #         "li")[people_about_index].find('span'))[10:-7]

                    #     movie["cast"].append(
                    #         {"name": f"{name}", "name_id": f"{name_id}", "official_name": f"{official_name}"})

                    # if people_index == 3:
                    #     role = str(person_elems_person[people_index].find_all(
                    #         "li")[people_about_index].find('span'))[10:-7]

                    #     movie["staff"].append(
                    #         {"name": f"{name}", "name_id": f"{name_id}", "role": f"{role}"})

            # print("############################################################")

            # print(person_elems_title)
            # print()
            # print(person_elems_person)
            # print()

            # print(len(person_elems_title), len(
            #     person_elems_person), )
            # print()

            ###

            all_movie.append(movie)

            writer.write(movie)

# JSONファイルのロード
with open('jfdb.jsonlines', 'r',  encoding="utf-8_sig") as f:
    json_output = json.load(f)


# print(Details_elems)

# print(len(alltitle))
# print(len(alltitle))
