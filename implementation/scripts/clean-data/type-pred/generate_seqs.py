import math, json, sys

parts = ["eklavya","names-all","names-filtered","names-filtered-no-wasm-ty","no-names-class-const"]
portions = ['test', 'dev', 'train']
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
    if path_line == "": return ""
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

for portion in portions:
    for part_i, part in enumerate(parts):
        file = open("{}.csv".format(portion), "r")
        f_seq1_x = open("seqs/{}/seq1/x_{}.txt".format(part, portion), "w+")
        f_seq1_y = open("seqs/{}/seq1/y_{}.txt".format(part, portion), "w+")
        f_seq2_x = open("seqs/{}/seq2/x_{}.txt".format(part, portion), "w+")
        f_seq2_y = open("seqs/{}/seq2/y_{}.txt".format(part, portion), "w+")
        f_seq3_x = open("seqs/{}/seq3/x_{}.txt".format(part, portion), "w+")
        f_seq3_y = open("seqs/{}/seq3/y_{}.txt".format(part, portion), "w+")
        f_seq4_x = open("seqs/{}/seq4/x_{}.txt".format(part, portion), "w+")
        f_seq4_y = open("seqs/{}/seq4/y_{}.txt".format(part, portion), "w+")
        f_seq5_x = open("seqs/{}/seq5/x_{}.txt".format(part, portion), "w+")
        f_seq5_y = open("seqs/{}/seq5/y_{}.txt".format(part, portion), "w+")
        for line in file:
            path_line = line.split(",")[0].rstrip()
            paths_summarized_line = summarize_path(path_line)
            path_seq = "p0 d30" if path_line == "" else get_path_seq(path_line)
            path_summarized_seq = "p0 d30" if paths_summarized_line == "" else get_path_seq(paths_summarized_line)
            i, j = line.find(",")+1, line.rfind(" || ")
            labels = line[i:j].split("|delim2|")[1:]
            series = line[j+4:].replace("\n", "")
            if part == "names-filtered-no-wasm-ty": series = series[len("i32 <begin> "):]
            f_seq1_x.write(path_seq + "\n")
            f_seq1_y.write(labels[part_i] + "\n")
            f_seq2_x.write(series + "\n")
            f_seq2_y.write(labels[part_i] + "\n")
            f_seq3_x.write(series + " ; <path_seq_begin> " + path_seq + "\n")
            f_seq3_y.write(labels[part_i] + "\n")
            f_seq4_x.write(path_summarized_seq + "\n")
            f_seq4_y.write(labels[part_i] + "\n")
            f_seq5_x.write(series + " ; <path_seq_begin> " + path_summarized_seq + "\n")
            f_seq5_y.write(labels[part_i] + "\n")
        f_seq1_x.close()
        f_seq1_y.close()
        f_seq2_x.close()
        f_seq2_y.close()
        f_seq3_x.close()
        f_seq3_y.close()
        f_seq4_x.close()
        f_seq4_y.close()
        f_seq5_x.close()
        f_seq5_y.close()

