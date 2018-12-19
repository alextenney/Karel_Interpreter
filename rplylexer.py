import rply
from rply import LexerGenerator

'''
Content adapted from both the RPLY documentation and Josh Sharp's blog post "Using RPython and RPly to build a language interpreter, part 1".

RPLY: https://media.readthedocs.org/pdf/rply/latest/rply.pdf and https://rply.readthedocs.io/en/latest/

Josh Sharp: http://joshsharp.com.au/blog/rpython-rply-interpreter-1.html

'''

def lex():
    lg = LexerGenerator()
    
    # build up a set of token names and regexes they match 
    lg.add('WHITESPACE', r'[ ]+' )
    lg.add('INTEGER', r'-?\d+')
    lg.add('IF', r'if(?!\w)')
    lg.add('ELSE', r'else(?!\w)')
    lg.add('WHILE', r'while(?!\w)')
    lg.add('FOR', 'for i in range')
    lg.add('FUNCTION', r'def(?!\w)')
    lg.add('COLON', ':')
    lg.add('OPENPAREN', '\(')
    lg.add('CLOSEPAREN', '\)')
    lg.add('NEWLINE', r'\n')
    lg.add('IMPORT','from karel import \*')
    lg.add('BEGIN', 'begin_karel_program')
    lg.add('END', 'end_karel_program')
    lg.add('NOT', r'not(?!\w)')
    #commands
    lg.add('MOVE','move')
    lg.add('LEFTTURN', 'turn_left')
    lg.add('PUTBEEPER', 'put_beeper')
    lg.add('PICKBEEPER','pick_beeper')
    #conditions 
    lg.add('FACENORTH', 'facing_north')
    lg.add('FACESOUTH', 'facing_south')
    lg.add('FACEWEST', 'facing_west')
    lg.add('FACEEAST', 'facing_east')
    lg.add('FRONTCLEAR', 'front_is_clear')
    lg.add('LEFTCLEAR', 'left_is_clear')
    lg.add('RIGHTCLEAR', 'right_is_clear')
    lg.add('PRESENT', 'beepers_present')
    lg.add('INBAG', 'beepers_in_bag')
    lg.add('NOTCHECK', 'not')
    lg.add('IDENTIFIER', '[a-zA-Z_][a-zA-Z0-9_]*')
    
    # ignore whitespace 
    lg.ignore('#.*\n')
    lg.ignore('"""(.|\n)*?"""')
    lg.ignore("'''(.|\n)*?'''")
    
    lexer = lg.build()

    return lexer
