from globals import NodeKind, StmtKind, ExpKind, TokenType
from error import semantic_error

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]
        self.funcs = {}

    def push(self):
        self.scopes.append({})

    def pop(self):
        self.scopes.pop()

    def declare(self, name, typ, line):
        if name in self.scopes[-1]:
            semantic_error(line, f"Variável '{name}' já declarada neste escopo.")
        self.scopes[-1][name] = typ

    def lookup(self, name, line):
        for s in reversed(self.scopes):
            if name in s:
                return s[name]
        semantic_error(line, f"Variável '{name}' não declarada.")