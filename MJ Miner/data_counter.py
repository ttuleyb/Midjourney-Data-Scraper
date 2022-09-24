from collections import Counter

contents = ""
with open("everything.txt", "r", encoding="utf-8") as f:
    contents = f.read()

everything = contents.split("\n")
for i in range(len(everything)):
    if "_" in everything[i] and everything[i].find("_") < 4:
        everything[i] = everything[i].split("_")[1]

counter_object = Counter(everything)
keys = counter_object.keys()
num_values = len(keys)
print(str(num_values) + " unique items found!")
print(str(len(everything)) + " total number of items found")

with open("everything_nodupe.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(keys))

everythingBeta = []

for i in range(len(everything)):
    if "--beta" in everything[i]:
        everythingBeta.append(everything[i])

counter_object = Counter(everythingBeta)
keys = counter_object.keys()
num_values = len(keys)
print(str(num_values) + " unique beta items found!")
print(str(len(everythingBeta)) + " total number of beta items found")