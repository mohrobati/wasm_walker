import json, copy, hashlib

def find_function(lines, target):
    count = 0
    active = False
    function = []
    for line in lines:
        if line.lstrip().startswith("(func "):
            if active:
                break
            if count == target:
                active = True  
                function.append(line)
            count += 1
        elif line.lstrip().startswith("(import") and "(func " in line:
            count += 1
        else:
            if active:
                function.append(line)
    return function

def collapse(paths, target):
    i = 0
    while i < len(paths):
        if paths[i] == target:
            count = 0
            j = i
            while j < len(paths) and paths[j] == target:
                count += 1
                j += 1
            if count > 1:
                paths[i:j] = [target]
            i += 1
        else:
            i += 1
    return ",".join(paths)

def refine_path_line(line):
    line = line.replace("\n", "").replace(",block", "").replace("block,", "").replace(")", "").replace("(", "")
    line = collapse(line.split(","), "loop")
    line = collapse(line.split(","), "if")
    return line

def get_paths(lines):
    stack = []
    paths = []
    prev_ins = None
    prev_spaces = None
    for line in lines:
        curr_spaces = len(line) - len(line.lstrip())
        curr_ins = line.lstrip().split(" ")[0].replace("\n", "")  
        if prev_spaces is not None and prev_spaces < curr_spaces:
            stack.append(prev_ins)
        if prev_spaces is not None and prev_spaces > curr_spaces:
            if len(stack) > 0: stack.pop()
        if len(stack) > 0:
            paths.append(",".join(stack) + "," + curr_ins)
        else:
            paths.append(curr_ins)
        prev_ins = curr_ins
        prev_spaces = curr_spaces
    return paths