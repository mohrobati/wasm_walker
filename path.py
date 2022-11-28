import json, copy, hashlib

def summarize_path(path):
    s_path = []
    for item in path.split(",")[4:]:
        if len(item) > 0 and item[0].isupper():
            s_path.append(item)
    return ",".join([*dict.fromkeys(s_path)])

def extract_paths(d):
    if isinstance(d, dict):
        for key, value in d.items():
            yield f',{key}'
            yield from (f',{key}{p}' for p in extract_paths(value))
    elif isinstance(d, list):
        for value in d:
            yield from (f'{p}' for p in extract_paths(value))
    elif isinstance(d, str):
        yield f',{d}'
    elif isinstance(d, type(None)):
        yield f',None'

def count_import_functions(paths):
    count = 0 
    active = False
    index = -1
    for path in paths:
        index += 1
        if count > 0 and not path.startswith("Import"):
            return count, index
        if path == "Import,Span":
            active = True
        if active and "Func,TypeUse" in path:
            active = False
            count += 1
    return count, index

def get_function_paths(paths, function_indices, offset):
    count = offset - 1
    active = False
    final_paths = []
    curr_func_paths = []
    for path in paths:
        if not path.startswith("Func"):
            break
        if path == "Func,Span":
            if active:
                active = False
                final_paths.append(copy.deepcopy(curr_func_paths))
                curr_func_paths = []
            count += 1
            if count in function_indices:
                active = True
        if active:
            curr_func_paths.append(path)
    if len(curr_func_paths) > 0: final_paths.append(copy.deepcopy(curr_func_paths))
    return final_paths

def get_paths(wat_dict):
    paths = [s for s in extract_paths(wat_dict)]
    filtered_paths = []
    prev_path = None
    prev_len = 0
    for path in paths:
        length = len(path.split(",")) - 1
        if length <= prev_len and len(prev_path) > 0:
            s_path = summarize_path(prev_path[1:])
            if s_path: filtered_paths.append(s_path)
        prev_path = path
        prev_len = length
    return filtered_paths
