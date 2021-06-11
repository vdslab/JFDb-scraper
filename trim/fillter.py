import jsonlines


def fillter(file_name, txt_name):
    with jsonlines.open(file_name) as f:
        with jsonlines.open(txt_name, mode="w") as g:
            for i in f:
                ymd = i["公開年月日"]
                if not(ymd == "未定" or ymd == ""):  # 未定のものとデータがない場合をはじく
                    if int(ymd[:4]) >= 2003:
                        g.write(i)


fillter("jfdb.jsonlines", "jfdb_after2003.jsonlines")
fillter("jcdb.jsonlines", "jcdb_after2003.jsonlines")
