from rplylexer import lex
import sys
from rplyparser import Parser

file = open('kareltest.py')
source = file.read()
file.close()

lexer = lex()

tokens = lexer.lex(source)


for token in tokens:
    space = 0 

    if token == "SPACE":
        space += 1
    else:
        space = 0

    print(token)


pg = Parser()
pg.parse()
parser = pg.get_parser()

result = parser.parse(tokens)

if result == None:
    print ('This program is valid.')
else:
    result.eval()
