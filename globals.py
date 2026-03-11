from enum import Enum, auto
class TokenType(Enum):
    EOF = auto(); ERROR = auto()

    IF = auto(); ELSE = auto(); WHILE = auto(); RETURN = auto()
    DEF = auto(); PRINT = auto(); VAR = auto(); SET = auto()
    INT = auto(); REAL = auto(); BOOL = auto(); VOID = auto()
    TRUE = auto(); FALSE = auto(); AND = auto(); OR = auto(); NOT = auto()

    ID = auto(); NUM = auto(); REAL_NUM = auto(); STRING = auto()

    ASSIGN = auto(); EQ = auto(); NEQ = auto()
    LT = auto(); LE = auto(); GT = auto(); GE = auto()

    PLUS = auto(); MINUS = auto()
    TIMES = auto(); OVER = auto()

    LPAREN = auto(); RPAREN = auto()
    SEMI = auto(); COLON = auto(); COMMA = auto()
    LBRACE = auto(); RBRACE = auto()
class Token:
    def __init__(self, token_type, val, line):
        self.type = token_type
        self.val = val
        self.line = line

class NodeKind(Enum):
    STMT = auto()
    EXP = auto()

class StmtKind(Enum):
    IFK = auto(); WHILEK = auto(); RETK = auto()
    PRINTK = auto(); VARDK = auto(); SETK = auto(); DEFK = auto()
    BLOCKK = auto(); PARAMK = auto()

class ExpKind(Enum):
    OPK = auto(); CONSTK = auto(); IDK = auto(); CALLK = auto()

class ExpType(Enum):
    VOID = auto(); INTEGER = auto(); BOOLEAN = auto(); REAL = auto()

MAXCHILDREN = 3

lineno = 0

NOME_TOKENS = {
    TokenType.ID: "identificador (nome de variável/função)",
    TokenType.NUM: "número inteiro",
    TokenType.REAL_NUM: "número real",
    TokenType.STRING: "texto (string)",
    TokenType.ASSIGN: "'='",
    TokenType.EQ: "'=='",
    TokenType.NEQ: "'!='",
    TokenType.LT: "'<'",
    TokenType.LE: "'<='",
    TokenType.GT: "'>'",
    TokenType.GE: "'>='",
    TokenType.PLUS: "'+'",
    TokenType.MINUS: "'-'",
    TokenType.TIMES: "'*'",
    TokenType.OVER: "'/'",
    TokenType.LPAREN: "'('",
    TokenType.RPAREN: "')'",
    TokenType.SEMI: "';'",
    TokenType.COLON: "':'",
    TokenType.COMMA: "','",
    TokenType.LBRACE: "'{'",
    TokenType.RBRACE: "'}'",
    TokenType.IF: "'if'",
    TokenType.ELSE: "'else'",
    TokenType.WHILE: "'while'",
    TokenType.RETURN: "'return'",
    TokenType.DEF: "'def'",
    TokenType.PRINT: "'print'",
    TokenType.VAR: "'var'",
    TokenType.SET: "'set'",
    TokenType.INT: "'int'",
    TokenType.REAL: "'real'",
    TokenType.BOOL: "'bool'",
    TokenType.VOID: "'void'",
    TokenType.TRUE: "'true'",
    TokenType.FALSE: "'false'",
    TokenType.AND: "'and'",
    TokenType.OR: "'or'",
    TokenType.NOT: "'not'",
    TokenType.EOF: "fim do arquivo"
}