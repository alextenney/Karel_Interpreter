from rplylexer import lex
import sys
from rplyparser import Parser
from indent_tracking import IndentTracker

'''
A syntax lexer and parser for the language of "Karel", created for CPSC 231 at University of Calgary, which is a restricted
version of Python. 

Author: Alexandra Tenney, December 18th 2018
'''

source_code = sys.argv[1]

file = open(source_code)
source = file.read()
file.close()

lexer = lex()
tokens = lexer.lex(source)

indent_tracker = IndentTracker()
tokens = indent_tracker.track_tokens_filter(lexer, tokens)
tokens = indent_tracker.indentation_filter(tokens)

pg = Parser()
pg.setup()
result = pg.parse(tokens)

if result == None:
    print ('This is a valid Karel Program.')
else:
    result.eval()
