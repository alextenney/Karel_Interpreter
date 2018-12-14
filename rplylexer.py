import rply
from rply import LexerGenerator

def lex():
    lg = LexerGenerator()
    
    # build up a set of token names and regexes they match 
    lg.add('INDENT','\t' )
    lg.add('SPACE', '\s')
    lg.add('INTEGER', r'-?\d+')
    lg.add('IF', r'if(?!\w)')
    lg.add('ELSE', r'else(?!\w)')
    lg.add('WHILE', r'while(?!\w)')
    lg.add('FUNCTION', r'def(?!\w)')
    lg.add('MODULE', r'mod(?!\w)')
    lg.add('COLON', ':')
    lg.add('OPENPAREN', '\(')
    lg.add('CLOSEPAREN', '\)')
    #lg.add('NEWLINE', '\n')
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
    #this does work
    lg.add('IDENTIFIER', '[a-zA-Z_][a-zA-Z0-9_]*')
    
    # ignore whitespace 
    lg.ignore('[\n]')
    
    lexer = lg.build()

    return lexer