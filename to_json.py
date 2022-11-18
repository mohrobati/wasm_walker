from syn_compiler.lexer import Lexer
from syn_compiler.parser import Parser
import os
import glob

for filename in glob.glob('./*.wasm', recursive=True):
    os.system("cargo run " + filename)
    f_debug = open("./parsed_debug.txt", "r")
    input = f_debug.read()
    f_debug.close()
    lexer = Lexer().build()
    lexer.input(input)
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print(tok)
    parser = Parser()
    parser.build().parse(input, lexer, False)
    f_json = open("./parsed_json.json", "w+")
    f_json.write(parser.dictTree_string)
    f_json.close()

