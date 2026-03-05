from enum import Enum, auto

class TokenType(Enum):
    EOF = auto()
    ERROR = auto()

class Token:
    def __init__(self, token_type, val, line):
        self.type = token_type
        self.val = val
        self.line = line

tokenzin = Token(TokenType.EOF, "aaaaa", 1)
print(tokenzin.val)
lineno = 0
