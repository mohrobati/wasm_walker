from path import *
from to_wat import *
import os, json, random
import threading

THREAD_SIZE = 1
DATASET_SIZE = 0

class Collector(threading.Thread):

    def __init__(self, t_id):
        super(Collector, self).__init__()
        window_size = int(DATASET_SIZE / THREAD_SIZE)
        self.t_id=t_id
        self.low=t_id*window_size
        self.high=(t_id+1)*window_size
        self.final_results = set()
        self.cumulative = []
        self.curr_file = None
        self.curr_indices = []
        self.curr_types = []
        self.curr_len = 0
        self.counter = 0
    
    def mine_binary_info(self):
        success = parse_binary_to_wat(self.curr_file.replace("../../binaries/wasm-dwarf/", "./data/wasm-dwarf/"), self.t_id)
        if not success:
            return False
        wat_file = open("./__logs__/code_{}.wat".format(self.t_id), "r")
        wat_lines = wat_file.readlines()
        wat_file.close()
        for index in self.curr_indices:
            func = find_function(wat_lines, index)
            for path in get_paths(func):
                path = refine_path_line(path[6:])
                self.final_results.add(path)
            self.counter += 1
        print(self.counter, "/", DATASET_SIZE)
        self.cumulative.append(len(self.final_results))
        return True

    def run(self):
        for line in dataset[self.low:self.high]:
            [info, ty, s] = line.split("|DELIMETER973d1544f1|")
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

exp = 'eklavya'
portion = 'train'
dataset = open("./benchmark/{}/{}.jsonl".format(exp, portion), "r").readlines()
DATASET_SIZE = len(dataset)
collectors = [Collector(i) for i in range(THREAD_SIZE)]
for c in collectors:
    c.start()
for c in collectors:
    c.join()
f_results = open("./__results__/accumulative.txt", "w+")
for c in collectors:
    for line in c.cumulative:
        f_results.write(str(line) + "\n")
f_results.close()