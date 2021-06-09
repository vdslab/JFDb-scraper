jfdb = open("jfdbTrim.txt", mode="r", encoding="UTF-8")
cnt = 0
with open("a.txt", mode="w", encoding="UTF-8") as f:
    for i in jfdb:
        flag = False
        for j in open("jcdbTrim.txt", mode="r", encoding="UTF-8"):
            if i == j:
                flag = True
                break
        if flag == False:
            cnt += 1
            f.write(i)
