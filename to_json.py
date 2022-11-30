from syn_compiler.lexer import Lexer
from syn_compiler.parser import Parser
import os, glob, sys, multiprocessing

def do_work(filename):
    _ = os.system("cargo run --quiet " + filename)
    f_debug = open("./__logs__/parsed_debug.txt", "r")
    input = f_debug.read()
    f_debug.close()
    lexer = Lexer().build()
    lexer.input(input)
    parser = Parser()
    parser.build().parse(input, lexer, False)
    f_json = open("./__logs__/parsed_json.json", "w+")
    f_json.write(parser.dictTree_string)
    f_json.close()

# target_file = './projects/abcm2ps/**/music.o'

def parse_binary_to_json(target_file):
    for filename in [glob.glob(target_file, recursive=True)[0]]:
        proc = multiprocessing.Process(target=do_work, args=(filename, ))
        proc.start()
        proc.join(timeout=60)
        proc.terminate()


