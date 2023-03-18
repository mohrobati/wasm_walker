import collections
f = open("names.txt", "r")

counts = collections.defaultdict(int)

for name in f:
    counts[name.replace("\n", "")] += 1

counts_array = sorted([(counts[key], key) for key in counts], reverse=True)
c = 0
for item in counts_array:
    if item[0] >= 5:
        print(item)
        c+=item[0]
    else:
        break