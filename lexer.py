from globals import TokenType, Token
import globals
class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1

        self.keywords = {
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "return": TokenType.RETURN,
            "def": TokenType.DEF,
            "print": TokenType.PRINT,
            "var": TokenType.VAR,
            "set": TokenType.SET,
            "int": TokenType.INT,
            "real": TokenType.REAL,
            "bool": TokenType.BOOL,
            "void": TokenType.VOID,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "and": TokenType.AND,
            "or": TokenType.OR,
            "not": TokenType.NOT
        }