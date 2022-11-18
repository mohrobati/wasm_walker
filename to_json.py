from syn_compiler.lexer import Lexer
from syn_compiler.parser import Parser
import os

os.system("cargo run")

f_debug = open("./parsed_debug.txt", "r")
input = f_debug.read()
f_debug.close()
lexer = Lexer().build()
lexer.input(input)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
parser = Parser()
parser.build().parse(input, lexer, False)
# f_json.write(parser.dictTree_string)