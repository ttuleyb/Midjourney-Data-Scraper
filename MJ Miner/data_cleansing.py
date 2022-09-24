from operator import index
import re

file = open("everything.txt", "r", encoding="utf-8")
data = file.read()
file.close()

data = re.sub(r'https://s.mj.run/.*? ', '', data)
data = data.replace("<", "").replace(">", "").replace("\t", "").replace("--uplight", "").replace("--upbeta", "").replace("   ", "").replace("  ", "").replace("    ", "")

data = data.split("\n")
cleanedData = []
for i in range(len(data)):
    endOfPref = data[i].find("_") + 1
    data[i] = data[i][endOfPref:]
    # if "--" in data[i]:
    #     data[i] = data[i].split("--")[0]

    if len(data[i]) < 10:
        continue

    data[i] = "\t " + data[i] + "###\n"
    cleanedData.append(data[i])

# datas = ""
# for i in data:
# datas += "	" + i + "\n"

datas = "".join(cleanedData)

file = open("data.tsv", "w", encoding="utf-8")
file.write("prompt\tcompletion\n"+ datas)
file.close()