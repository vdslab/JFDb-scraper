import pandas as pd
import datetime as dt


def sort_date(file_name, txt_name):
    datalines = pd.read_json(file_name,
                             orient="records",
                             lines=True,
                             encoding="utf-8")
    a = []
    for i in range(len(datalines["タイトル"])):
        date = datalines["公開年月日"][i]
        if len(date) == 5:
            date += "12月31日"
        elif len(date) <= 8:
            if date[5:] == "4月" or date[5:] == "6月" or date[5:] == "9月" or date[5:] == "11月":
                date += "30日"
            elif date[5:] == "2月":
                date += "28日"
            else:
                date += "31日"
        a.append((dt.datetime.strptime(
            date, "%Y年%m月%d日"), datalines["タイトル"][i]))
    a.sort()

    prev = ""
    with open(txt_name, "w", encoding="utf-8") as f:
        for data in a:
            if prev != data[0]:
                f.write(dt.date.strftime(data[0], "%Y-%m%d") + "\n")
                prev = data[0]
            f.write(data[1] + "\n")


sort_date("jfdb_after2003.jsonlines", "jfdb_sort.txt")
sort_date("jcdb_after2003.jsonlines", "jcdb_sort.txt")
