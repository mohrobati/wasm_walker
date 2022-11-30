from path import *
from to_json import *
import os, json

final_set = set()
dataset = open("./data.jsonl", "r")
final_set_file = open("./__logs__/paths.txt", "w+")
curr_file = None
curr_indices = []

def mine_binary_info():
    print("Starting to mine:", curr_file)
    parse_binary_to_json(curr_file.replace("../../binaries/wasm-dwarf/", "../data/wasm-dwarf/"))
    json_file = open("./__logs__/parsed_json.json", "r")
    wat_dict = json.loads(json_file.read())
    json_file.close()
    paths = get_paths(wat_dict)
    import_count, import_done_idx = count_import_functions(paths)
    functions = get_function_paths(paths[import_done_idx:], curr_indices, import_count)
    for func in functions:
        for path in func:
            final_set.add(path[5:])
    print("Mining done!\n===")

try:
    for line in dataset:
        datapoint = json.loads(line)
        if curr_file is None:
            curr_file = datapoint['file']
        if curr_file == datapoint['file']:
            curr_indices.append(datapoint['function_idx'])
        else:
            mine_binary_info()
            curr_file = datapoint['file']
            curr_indices = []
            curr_indices.append(datapoint['function_idx'])

    if len(curr_indices):
        mine_binary_info()

    for item in final_set:
        final_set_file.write(item + "\n")
        
    dataset.close()
    final_set_file.close()
except:
    for item in final_set:
        final_set_file.write(item + "\n")
        
    dataset.close()
    final_set_file.close()