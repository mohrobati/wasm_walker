from path import *
from to_json import *
import os, json
import threading

dataset = open("./benchmark/test.jsonl", "r").readlines()
hash_table = json.loads(open("./embedding/hash_table.json", "r").read())

THREAD_SIZE = 32

class Collector(threading.Thread):

    def __init__(self, t_id):
        super(Collector, self).__init__()
        window_size = int(len(dataset) / THREAD_SIZE)
        self.t_id=t_id
        self.low=t_id*window_size
        self.high=(t_id+1)*window_size
        self.final_results = []
        self.curr_file = None
        self.curr_indices = []
        self.curr_types = []
    
    def mine_binary_info(self):
        print("Starting to mine:", self.curr_file)
        success = parse_binary_to_json(self.curr_file.replace("../../binaries/wasm-dwarf/", "../data/wasm-dwarf/"), self.t_id)
        if not success:
            print("Mining timed out!\n===")
            return False
        json_file = open("./__logs__/parsed_json_{}.json".format(self.t_id), "r")
        wat_dict = json.loads(json_file.read())
        json_file.close()
        paths = get_paths(wat_dict)
        import_count, import_done_idx = count_import_functions(paths)
        functions = get_function_paths(paths[import_done_idx:], self.curr_indices, import_count)
        for func in functions:
            ty = None
            if len(self.curr_types) > 0:
                ty = self.curr_types.pop(0)
            vector = [0 for i in range(len(hash_table))]
            for path in func:
                if path[5:] in hash_table:
                    vector[hash_table[path[5:]]] += 1
            self.final_results.append(str([vector, ty]) + "\n")
        print("Mining done!\n===")
        return True

    def run(self):
        for line in dataset[self.low:self.high]:
            [info, ty] = line.split("|DELIMETER973d1544f1|")
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

collectors = [Collector(i) for i in range(THREAD_SIZE)]
for c in collectors:
    c.start()
for c in collectors:
    c.join()
f_results = open("./__logs__/results.csv", "w+")
for c in collectors:
    for line in c.final_results:
        f_results.write(line.replace("[[","").replace(" ","").replace("],'",",").replace("']",""))

