from syn_compiler.lexer import Lexer
from syn_compiler.parser import Parser
import os, glob, sys, multiprocessing

def do_work(filename, return_dict, t_id):
    return_dict['success'] = None
    _ = os.system("cargo run --quiet " + filename + " " + str(t_id))
    f_debug = open("./__logs__/parsed_debug_{}.txt".format(t_id), "r")
    input = f_debug.read()
    f_debug.close()
    lexer = Lexer().build()
    lexer.input(input)
    parser = Parser()
    parser.build().parse(input, lexer, False)
    f_json = open("./__logs__/parsed_json_{}.json".format(t_id), "w+")
    f_json.write(parser.dictTree_string)
    f_json.close()
    return_dict['success'] = True

# target_file = './projects/abcm2ps/**/music.o'

def parse_binary_to_json(target_file, t_id):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    for filename in [glob.glob(target_file, recursive=True)[0]]:
        proc = multiprocessing.Process(target=do_work, args=(filename, return_dict, t_id))
        proc.start()
        proc.join(timeout=600)
        proc.terminate()
    return return_dict['success']
    


