from path import *
from to_wat import *
import os, json
import threading

hash_table = json.loads(open("./paths_set/hash_table.json", "r").read())

THREAD_SIZE = 32
DATASET_SIZE = 0

class Collector(threading.Thread):

    def __init__(self, t_id):
        super(Collector, self).__init__()
        window_size = int(DATASET_SIZE / THREAD_SIZE)
        self.t_id=t_id
        self.low=t_id*window_size
        self.high=(t_id+1)*window_size
        self.final_results = []
        self.curr_file = None
        self.curr_indices = []
        self.curr_types = []
        self.curr_len = 0

    def vector_to_path(self, vector):
        path = ""
        for i, val in enumerate(vector):
            if val != 0:
                path += "p" + str(i) + " " + str(val) + " "
        return path
    
    def mine_binary_info(self):
        success = parse_binary_to_wat(self.curr_file.replace("../../binaries/wasm-dwarf/", "./data/wasm-dwarf/"), self.t_id)
        if not success:
            return False
        wat_file = open("./__logs__/code_{}.wat".format(self.t_id), "r")
        wat_lines = wat_file.readlines()
        wat_file.close()
        for index in self.curr_indices:
            func = find_function(wat_lines, index)
            ty = None
            if len(self.curr_types) > 0:
                ty = self.curr_types.pop(0)
            vector = [0 for i in range(len(hash_table))]
            for path in get_paths(func):
                path = refine_path_line(path[6:])
                if path in hash_table:
                    vector[hash_table[path]] += 1
            self.final_results.append(self.vector_to_path(vector) + "," + ty + "\n")
        if len(self.final_results) - self.curr_len > 50:
            advance = int(len(self.final_results) / ((DATASET_SIZE/THREAD_SIZE)/50))
            print("Thread {}: [".format(self.t_id), end="")
            for i in range(advance): print("\033[91m" + "=" + "\033[0m", end="") 
            for i in range(50-advance): print("-", end="") 
            print("] ({}%)".format(advance * 2))
            self.curr_len = len(self.final_results)
        return True

    def run(self):
        for line in dataset[self.low:self.high]:
            [info, ty, s] = line.split("|delim1|")
            ty += " || " + s
            ty = ty.replace("\n", "")
            datapoint = json.loads(info)
            if self.curr_file is None:
                self.curr_file = datapoint['file']
            if self.curr_file == datapoint['file']:
                self.curr_indices.append(datapoint['function_idx'])
                self.curr_types.append(ty)
            else:
                self.mine_binary_info()
                self.curr_file = datapoint['file']
                self.curr_indices = []
                self.curr_types = []
                self.curr_indices.append(datapoint['function_idx'])
                self.curr_types.append(ty)
        if len(self.curr_indices):
            self.mine_binary_info()


exp = 'combined' 
for portion in ['test', 'dev', 'train']:
    step, end = 20000, 1
    if portion == 'test': end = 42000
    if portion == 'dev': end = 98000
    if portion == 'train': end = 650000
    for i in range(0, end, step):
        dataset = open("./benchmark/{}/{}.jsonl".format(exp, portion), "r").readlines()[i:i+step]
        DATASET_SIZE = len(dataset)
        collectors = [Collector(i) for i in range(THREAD_SIZE)]
        for c in collectors:
            c.start()
        for c in collectors:
            c.join()
        f_results = open("./__results__/{}_{}_{}.csv".format(exp, portion, i), "w+")
        for c in collectors:
            for line in c.final_results:
                f_results.write(line)
        f_results.close()

