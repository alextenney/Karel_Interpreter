from rply import ParserGenerator
from rply.token import BaseBox
from rplylexer import lex
import rply

class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names, accepted by the parser. 
            ['STRING', 'INTEGER', 'IDENTIFIER', 'IF', 'ELSE', 'COLON', 'NOT', 'WHILE',  
            'END', 'NEWLINE', 'FUNCTION', 'OPENPAREN', 'CLOSEPAREN', 'NOT', 'MODULE', 'IMPORT', 'BEGIN', 'MOVE',
            'LEFTTURN', 'PUTBEEPER', 'PICKBEEPER', 'FACENORTH', 'FACESOUTH', 'FACEWEST', 
            'LEFTCLEAR', 'RIGHTCLEAR', 'PRESENT', 'INBAG', 'NOTCHECK', 'SPACE' 
            ],
            # A list of precedence rules with ascending precedence, to 
            # disambiguate ambiguous production rules. 
            precedence=[ 
                ('left', ['FUNCTION',]), 
                ('left', ['LET',]), 
                ('left', ['=']), 
                ('left', ['[',']',',']), 
                ('left', ['IF', 'COLON', 'ELSE', 'NEWLINE','WHILE',])
            ] 
        )

    def parse(self):
        @self.pg.production('program : IMPORT lotsdef BEGIN parentheses lots END parentheses')
        def program(p):
            print('This program works!"')
        @self.pg.production('parentheses : OPENPAREN CLOSEPAREN')
        def parentheses(p):
            print('I matched ()')
        @self.pg.production('lots : ')
        def lots(p):
            print('I matched something empty')
        @self.pg.production('lots : statement lots')
        def bigone(p):
            print('i found either a statment or nothing')
        @self.pg.production('statement : MOVE parentheses')
        @self.pg.production('statement : LEFTTURN parentheses')
        @self.pg.production('statement : PUTBEEPER parentheses')
        @self.pg.production('statement : PICKBEEPER parentheses')
        def statement(p):
            print('found a statment')
        @self.pg.production('lotsdef : definition lotsdef')
        @self.pg.production('lotsdef : ')
        @self.pg.production('definition : FUNCTION SPACE IDENTIFIER parentheses COLON indent lots')
        def definition(p):
            print('found a definition')
        @self.pg.production('indent : SPACE SPACE SPACE SPACE')

        @self.pg.error
        def error_handler(token):
            raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())
        '''
        def error_handler(token):
            raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())

    parser = pg.build()
    '''
    
    def get_parser(self):
        return self.pg.build()

#SO WE ARE IGNORING NOTHING, WE HAVE A TOKEN FOR SPACE AND FOR NEW LINES. iF WE CAN DO A: IF # SPACE %4 == 0: SPACE = INDENT// IGNORE ALL OTHERS