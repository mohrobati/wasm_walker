import sys, math, json

DIM_NUM = 3352
paths_collection = {v: k for k, v in json.load(open('paths.json', 'r')).items()}
paths_summarized_collection = json.load(open('paths_summarize.json', 'r'))

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

def summarize_path(path_line):
    if path_line == "None": return "None"
    path_seq = ""
    paths, vals = [], []
    for i, item in enumerate(path_line.split(" ")):
        paths.append(item) if i % 2 == 0 else vals.append(int(item))
    summarized_vec = [0 for i in range(len(paths_summarized_collection))]
    for (p, v) in zip(paths, vals):
        summarized_vec[paths_summarized_collection[paths_collection[int(p[1:])].split(",")[-1]]] += v
    for i, item in enumerate(summarized_vec):
        if item != 0:
            path_seq += "p" + str(i) + " " + str(item) + " "
    return path_seq.rstrip()

for exp in ['10', '20', '50', '100']:
    for por in ['train', 'test', 'dev']:
        f = open('res/' + exp + '_' + por + ".csv", 'r')
        paths, paths_summarized, types, series = [], [], [], []
        c = 0
        for line in f:
            parts = line.split(",")
            path_line = parts[0]
            paths_summarized_line = summarize_path(path_line)
            path_seq = "p0 d30" if path_line == "None" else get_path_seq(path_line)
            path_summarized_seq = "p0 d30" if paths_summarized_line == "None" else get_path_seq(paths_summarized_line)
            paths.append(path_seq)
            paths_summarized.append(path_summarized_seq)
            ty, ser = parts[1], parts[2]
            types.append(ty)
            series.append(ser.replace("\n", ""))
            c += 1
            if c % 1000 == 0: print(c, exp, por)

        f_seq1_x = open("./seqs/"+exp+"/seq1/x_"+por+".txt", "w+")
        f_seq1_y = open("./seqs/"+exp+"/seq1/y_"+por+".txt", "w+")
        f_seq2_x = open("./seqs/"+exp+"/seq2/x_"+por+".txt", "w+")
        f_seq2_y = open("./seqs/"+exp+"/seq2/y_"+por+".txt", "w+")
        f_seq3_x = open("./seqs/"+exp+"/seq3/x_"+por+".txt", "w+")
        f_seq3_y = open("./seqs/"+exp+"/seq3/y_"+por+".txt", "w+")
        f_seq4_x = open("./seqs/"+exp+"/seq4/x_"+por+".txt", "w+")
        f_seq4_y = open("./seqs/"+exp+"/seq4/y_"+por+".txt", "w+")
        f_seq5_x = open("./seqs/"+exp+"/seq5/x_"+por+".txt", "w+")
        f_seq5_y = open("./seqs/"+exp+"/seq5/y_"+por+".txt", "w+")

        for path in paths: f_seq1_x.write(path + "\n")
        for ty in types: f_seq1_y.write(ty + "\n")
        for ser in series: f_seq2_x.write(ser + "\n")
        for ty in types: f_seq2_y.write(ty + "\n")
        for ser, path in zip(series, paths): f_seq3_x.write(ser + " ; <path_seq_begin> " + path + "\n")
        for ty in types: f_seq3_y.write(ty + "\n")
        for path in paths_summarized: f_seq4_x.write(path + "\n")
        for ty in types: f_seq4_y.write(ty + "\n")
        for ser, path in zip(series, paths_summarized): f_seq5_x.write(ser + " ; <path_seq_begin> " + path + "\n")
        for ty in types: f_seq5_y.write(ty + "\n")
