import json, copy

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

def get_paths(wat_dict):
    paths = [s for s in extract_paths(wat_dict)]
    filtered_paths = []
    prev_path = None
    prev_len = 0
    for path in paths:
        length = len(path.split(",")) - 1
        if length <= prev_len and len(prev_path) > 0:
            filtered_paths.append(copy.deepcopy(prev_path[1:]))
        prev_path = path
        prev_len = length
    return filtered_paths


json_file = open("./parsed_json.json", "r")
wat_dict = json.loads(json_file.read())
json_file.close()
paths = get_paths(wat_dict)
for path in paths:
    print(path)
