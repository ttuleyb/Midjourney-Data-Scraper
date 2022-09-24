from json import load

everything = []
with open("jsons\\" + "1.json", "r", encoding="utf-8") as inputFile:
    data = load(inputFile)
    for i in data:
        print(i["full_command"])
        everything.append(i["prompt"])