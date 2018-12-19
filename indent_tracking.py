from rplylexer import lex
from rply import *

'''

The idea from the indent tracker was adapted from Andrew Dalke / Dalke Scientific Software, LLC in his 
program "GardenSnake"

GardenSnake : http://www.dalkescientific.com/writings/diary/GardenSnake.py?fbclid=IwAR0TdEifx2lWO2ZMOFpDOpEdfiH1tJzLkEX3FrJUKkK1ixZUufMBBSEZxgY

'''

class IndentTracker:
    def __init__(self):
        self.NO_INDENT = 0
        self.MAY_INDENT = 1
        self.MUST_INDENT = 2

    def track_tokens_filter(self, lexer, tokens):
        lexer.at_line_start = at_line_start = True         
        indent = self.NO_INDENT
        lineno = 0
        for token in tokens:
            token.at_line_start = at_line_start
            token.lineno = lineno

            if token.name == "COLON":
                at_line_start = False
                indent = self.MAY_INDENT
                token.must_indent = False
                
            elif token.name == "NEWLINE":
                at_line_start = True
                if indent == self.MAY_INDENT:
                    indent = self.MUST_INDENT
                token.must_indent = False
                lineno += 1

            elif token.name == "WHITESPACE":
                token.must_indent = False
            
            elif token.name == 'IF':
                at_line_start = False
                if indent == self.MUST_INDENT:
                    token.must_indent = True
                else:
                    token.must_indent = False
                indent = self.NO_INDENT

            elif token.name == 'WHILE':
                at_line_start = False
                if indent == self.MUST_INDENT:
                    token.must_indent = True
                else:
                    token.must_indent = False
                indent = self.NO_INDENT 

            elif token.name == 'ELSE':
                at_line_start = False
                if indent == self.MUST_INDENT:
                    token.must_indent = True
                else:
                    token.must_indent = False
                indent = self.NO_INDENT
         
            elif token.name == 'DEF':
                at_line_start = False
                if indent == self.MUST_INDENT:
                    token.must_indent = True
                else:
                    token.must_indent = False
                indent = self.NO_INDENT

            else:
                # A real token; only indent after COLON NEWLINE
                if indent == self.MUST_INDENT:
                    token.must_indent = True
                else:
                    token.must_indent = False
                at_line_start = False
                indent = self.NO_INDENT

            yield token
            lexer.at_line_start = at_line_start

    def _new_token(self, name, lineno):
        tok = Token(name, None, lineno)
        return tok

    # Synthesize a DEDENT tag
    def DEDENT(self, lineno):
        return self._new_token("DEDENT", lineno)

    # Synthesize an INDENT tag
    def INDENT(self, lineno):
        return self._new_token("INDENT", lineno)

    def indentation_filter(self, tokens):
        # A stack of indentation levels; will never pop item 0
        levels = [0]
        token = None
        depth = 0
        prev_was_ws = False
        for token in tokens:
            if token.name == "WHITESPACE":
                depth = len(token.value)
                prev_was_ws = True
                # WS tokens are never passed to the parser
                continue

            if token.name == "NEWLINE":
                depth = 0
                if prev_was_ws or token.at_line_start:
                    # ignore blank lines
                    continue
                # pass the other cases on through
                continue

            prev_was_ws = False
            if token.must_indent:
                # The current depth must be larger than the previous level
                if not (depth > levels[-1]):
                    raise IndentationError("expected an indented block on line "+ str(token.lineno + 1))

                levels.append(depth)
                yield self.INDENT(token.lineno)

            elif token.at_line_start:
                # Must be on the same level or one of the previous levels
                if depth == levels[-1]:
                    # At the same level
                    pass
                elif depth > levels[-1]:
                    raise IndentationError("indentation increase but not in new block on line "+ str(token.lineno + 1))
                else:
                    # Back up; but only if it matches a previous level
                    try:
                        i = levels.index(depth)
                    except ValueError:
                        raise IndentationError("inconsistent indentation on line "+ str(token.lineno + 1))
                    for _ in range(i+1, len(levels)):
                        yield self.DEDENT(token.lineno)
                        levels.pop()

            yield token
