from path import *
from to_json import *
import os, json

dataset = open("./benchmark/data.jsonl", "r")
final_results_file = open("./__logs__/results.txt", "w+")
hash_table = json.loads(open("./embedding/hash_table.json", "r").read())
curr_file = None
curr_indices = []
curr_types = []

def mine_binary_info():
    print("Starting to mine:", curr_file)
    success = parse_binary_to_json(curr_file.replace("../../binaries/wasm-dwarf/", "../data/wasm-dwarf/"))
    if not success:
        print("Mining timed out!\n===")
        return False
    json_file = open("./__logs__/parsed_json.json", "r")
    wat_dict = json.loads(json_file.read())
    json_file.close()
    paths = get_paths(wat_dict)
    import_count, import_done_idx = count_import_functions(paths)
    functions = get_function_paths(paths[import_done_idx:], curr_indices, import_count)
    for func in functions:
        ty = None
        if len(curr_types) > 0:
            ty = curr_types.pop(0)
        vector = [0 for i in range(len(hash_table))]
        for path in func:
            if path[5:] in hash_table:
                vector[hash_table[path[5:]]] += 1
        final_results_file.write(str([vector, ty]) + "\n")
    print("Mining done!\n===")
    return True

try:
    for line in dataset:
        [info, ty] = line.split("|DELIMETER973d1544f1|")
        ty = ty.replace("\n", "")
        datapoint = json.loads(info)
        if curr_file is None:
            curr_file = datapoint['file']
        if curr_file == datapoint['file']:
            curr_indices.append(datapoint['function_idx'])
            curr_types.append(ty)
        else:
            mine_binary_info()
            curr_file = datapoint['file']
            curr_indices = []
            curr_types = []
            curr_indices.append(datapoint['function_idx'])
            curr_types.append(ty)

    if len(curr_indices):
        mine_binary_info()
        
        
    dataset.close()
    final_results_file.close()
except:
        
    dataset.close()
    final_results_file.close()