from globals import TokenType, Token
import globals
import error

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.keywords = {
            "if": TokenType.IF, "else": TokenType.ELSE, "while": TokenType.WHILE,
            "return": TokenType.RETURN, "def": TokenType.DEF, "print": TokenType.PRINT,
            "var": TokenType.VAR, "set": TokenType.SET, "int": TokenType.INT,
            "real": TokenType.REAL, "bool": TokenType.BOOL, "void": TokenType.VOID,
            "true": TokenType.TRUE, "false": TokenType.FALSE, "and": TokenType.AND,
            "or": TokenType.OR, "not": TokenType.NOT
        }

    def get_char(self):
        if self.pos < len(self.code):
            c = self.code[self.pos]
            self.pos += 1
            if c == '\n': globals.lineno += 1
            return c
        return ''

    def unget_char(self, c):
        if c != '':
            self.pos -= 1
            if c == '\n': globals.lineno -= 1

    def getToken(self):
        token_str = ""
        state = "START"
        globals.lineno = self.line

        while state != "DONE":
            c = self.get_char()
            save = True

            if state == "START":
                if c in (' ', '\t', '\n', '\r'):
                    save = False
                    if c == '\n': self.line += 1
                elif c == '/':
                    save = False
                    state = "INSLASH"
                elif c.isdigit():
                    state = "INNUM"
                elif c.isalpha() or c == '_':
                    state = "INID"
                elif c == '"':
                    state = "INSTRING"
                    save = False
                elif c == '=':
                    state = "INASSIGN"
                elif c in ('<', '>', '!'):
                    state = "INREL"
                elif c == '':
                    save = False
                    state = "DONE"
                    return Token(TokenType.EOF, "", self.line)
                else:
                    state = "DONE"
                    if c == '+': return Token(TokenType.PLUS, c, self.line)
                    elif c == '-': return Token(TokenType.MINUS, c, self.line)
                    elif c == '*': return Token(TokenType.TIMES, c, self.line)
                    elif c == '(': return Token(TokenType.LPAREN, c, self.line)
                    elif c == ')': return Token(TokenType.RPAREN, c, self.line)
                    elif c == '{': return Token(TokenType.LBRACE, c, self.line)
                    elif c == '}': return Token(TokenType.RBRACE, c, self.line)
                    elif c == ';': return Token(TokenType.SEMI, c, self.line)
                    elif c == ':': return Token(TokenType.COLON, c, self.line)
                    elif c == ',': return Token(TokenType.COMMA, c, self.line)
                    else: 
                        error.lexical_error(self.line, c)

            elif state == "INSLASH":
                if c == '/':
                    save = False
                    state = "INCOMMENT"
                    token_str = ""
                else:
                    self.unget_char(c)
                    return Token(TokenType.OVER, "/", self.line)

            elif state == "INCOMMENT":
                save = False
                if c == '\n' or c == '':
                    state = "START"
                    self.line += 1

            elif state == "INNUM":
                if c == '.':
                    state = "INREAL"
                elif not c.isdigit():
                    self.unget_char(c)
                    save = False
                    state = "DONE"
                    return Token(TokenType.NUM, token_str, self.line)

            elif state == "INREAL":
                if not c.isdigit():
                    self.unget_char(c)
                    save = False
                    state = "DONE"
                    return Token(TokenType.REAL_NUM, token_str, self.line)

            elif state == "INID":
                if not (c.isalnum() or c == '_'):
                    self.unget_char(c)
                    save = False
                    state = "DONE"
                    ttype = self.keywords.get(token_str, TokenType.ID)
                    return Token(ttype, token_str, self.line)

            elif state == "INSTRING":
                if c == '"':
                    save = False
                    state = "DONE"
                    return Token(TokenType.STRING, f'"{token_str}"', self.line)

            elif state == "INASSIGN":
                state = "DONE"
                if c == '=': return Token(TokenType.EQ, "==", self.line)
                else:
                    self.unget_char(c)
                    save = False
                    return Token(TokenType.ASSIGN, "=", self.line)

            elif state == "INREL":
                state = "DONE"
                if c == '=':
                    return Token(getattr(TokenType, ("GE" if token_str==">" else "LE" if token_str=="<" else "NEQ")), token_str+"=", self.line)
                else:
                    self.unget_char(c)
                    save = False
                    if token_str == '<': return Token(TokenType.LT, "<", self.line)
                    elif token_str == '>': return Token(TokenType.GT, ">", self.line)
                    else: 
                        error.lexical_error(self.line, token_str)

            if save: token_str += c
            
            

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python lexer.py <arquivo.mini>")
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            code = f.read()
        
        lexer = Lexer(code)
        print("\n===== LISTA DE TOKENS =====")
        token = lexer.getToken()
        
        while token.type.name != "EOF":
            # Imprime no formato <TIPO, "valor"> (linha)
            print(f"<{token.type.name}, '{token.val}'> (linha {token.line})")
            token = lexer.getToken()