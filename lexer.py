from globals import TokenType, Token
import globals

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1

    
    