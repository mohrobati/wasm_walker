import math 

def normalize_array(arr, n):
    min_value = 0
    max_value = max(arr)
    normalized_arr = []
    for value in arr:
        normalized_value = math.ceil((value - min_value) * (n / (max_value - min_value)))
        normalized_arr.append(normalized_value)
    return normalized_arr

def get_path_seq(path_line):
    path_seq = ""
    paths, vals = [], []
    for i, item in enumerate(path_line.split(" ")):
        paths.append(item) if i % 2 == 0 else vals.append(int(item))
    vals = normalize_array(vals, 30)
    for (p, v) in zip(paths, vals):
        path_seq += "p" + str(int(p[1:])+1) + " d" + str(v) + " "
    return path_seq.rstrip()

DIM_NUM = 3352
paths, names, series = [], [], []
c = 0
for line in open("name.csv"):
    parts = line.split(",")
    paths.append(parts[0])
    n = (",".join(parts[1:])).split("|delim2|")[0]
    s = line.split(" || ")[-1]
    names.append(n)
    series.append(s.replace("\n", ""))
    c += 1
    if c % 1000 == 0: print(c)

vec_file = open("vectors.txt", "w+")
for path in paths:
    if path == "":
        path = "None"
    vec_file.write(path + "\n")

ty = open("names.txt", "w+")
for name in names:
    gen_start = name.find("<")
    if gen_start > 0: name = name[:gen_start]
    if name.startswith("__"): name = name[2:]
    if name.startswith("_"): name = name[1:]
    name = name.lower()
    ty.write(name + "\n")

se = open("series.txt", "w+")
for ser in series:
    se.write(ser + "\n")