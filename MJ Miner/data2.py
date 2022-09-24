files = ["largedata1.txt", "largedata2.txt", "largedata3.txt", "largedata4.txt", "largedata5.txt", "largedata6.txt"]
everything = []

for x in files:
    file = open(x, "r", encoding="utf-8")

    for i in file.read().replace("\\n", "\n").split("\n"):
        everything.append(i)
    file.close()

file = open("everything.txt", "a", encoding="utf-8")
for i in everything:
    file.write(i + "\n")
file.close()