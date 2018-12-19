from rply import ParserGenerator
from rply.token import BaseBox
from rplylexer import lex
import rply

'''
Content adapted from both the RPLY documentation and Josh Sharp's blog post "Using RPython and RPly to build a language interpreter, part 1".

RPLY: https://media.readthedocs.org/pdf/rply/latest/rply.pdf and https://rply.readthedocs.io/en/latest/

Josh Sharp: http://joshsharp.com.au/blog/rpython-rply-interpreter-1.html

'''

class Parser:
    def __init__(self):
        self.indent_count = 0;
        self.definition_list = []

        self.pg = ParserGenerator(
            # A list of all token names, accepted by the parser. 
            ['INTEGER', 'IDENTIFIER', 'IF', 'ELSE', 'COLON', 'NOT', 'WHILE',  
            'END', 'FUNCTION', 'OPENPAREN', 'CLOSEPAREN', 'NOT', 'IMPORT', 'BEGIN', 'MOVE',
            'LEFTTURN', 'PUTBEEPER', 'PICKBEEPER', 'FACENORTH', 'FACESOUTH', 'FACEWEST', 
            'LEFTCLEAR', 'RIGHTCLEAR', 'FRONTCLEAR', 'PRESENT', 'INBAG', 'FOR',
            'FACEEAST', 'INDENT', 'DEDENT'
            ],
            # A list of precedence rules with ascending precedence, to 
            # disambiguate ambiguous production rules. 
            precedence=[ 
                ('left', ['FUNCTION',]),  
                ('left', ['[',']',',']), 
                ('left', ['IF', 'COLON', 'ELSE', ' ','WHILE',])
            ] 
        )

    def setup(self):
        @self.pg.production('program : IMPORT lotsdef BEGIN parentheses lots END parentheses')
        def program(p):
            pass

        @self.pg.production('parentheses : OPENPAREN CLOSEPAREN')
        def parentheses(p):
            pass

        @self.pg.production('lots : ')
        def lots(p):
            pass

        @self.pg.production('lots : statement lots')
        def bigone(p):
            pass

        @self.pg.production('call : IDENTIFIER parentheses')
        def call(p):
            if p[0].value in self.definition_list:
                pass
            else:
                raise ValueError('The definition '+ str(p[0].value)+ ' has been called before defined on line '+ str(p[0].lineno + 1))

        @self.pg.production('statement : MOVE parentheses  ')
        @self.pg.production('statement : LEFTTURN parentheses  ')
        @self.pg.production('statement : PUTBEEPER parentheses')
        @self.pg.production('statement : PICKBEEPER parentheses')
        @self.pg.production('statement : call')
        @self.pg.production('statement : IF condition  COLON INDENT lots DEDENT')
        #it for some reason does not recognize this kind of statement
        @self.pg.production('statement : IF condition  COLON INDENT lots DEDENT ELSE  COLON INDENT lots DEDENT')
        @self.pg.production('statement : WHILE condition  COLON INDENT lots DEDENT')
        #the for loop is broken because the identifier is broken
        @self.pg.production('statement : FOR OPENPAREN INTEGER CLOSEPAREN  COLON INDENT lots DEDENT')
        def statement(p):
            pass

        @self.pg.production('condition : FACENORTH parentheses')
        @self.pg.production('condition : FACESOUTH parentheses')
        @self.pg.production('condition : FACEEAST parentheses')
        @self.pg.production('condition : FACEWEST parentheses')
        @self.pg.production('condition : FRONTCLEAR parentheses')
        @self.pg.production('condition : LEFTCLEAR parentheses')
        @self.pg.production('condition : RIGHTCLEAR parentheses')
        @self.pg.production('condition : PRESENT parentheses')
        @self.pg.production('condition : INBAG parentheses')
        @self.pg.production('condition : NOT condition')
        def condition(p):
            pass

        @self.pg.production('lotsdef : definition lotsdef')
        @self.pg.production('lotsdef : ')
        def lotsdef(p):
            pass
        @self.pg.production('definition : FUNCTION IDENTIFIER parentheses COLON INDENT lots DEDENT')
        def definition(p):
            self.definition_list.append(p[1].value)
            pass
        

        @self.pg.error
        def error_handler(token):
            raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype()+ " at line "+ str(token.lineno + 1))

    def parse(self, tokens):
        return self.pg.build().parse(tokens)
