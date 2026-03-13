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


class SemanticAnalyzer:
    def __init__(self):
        self.symtab = SymbolTable()

    def analyze(self, tree):
        self.traverse(tree)

    def traverse(self, t):
        while t is not None:
            self.pre_visit(t)

            for i in range(3):
                if t.child[i]:
                    self.traverse(t.child[i])

            self.post_visit(t)
            t = t.sibling

    def pre_visit(self, t):
        if t.nodekind == NodeKind.STMT:

            if t.kind == StmtKind.BLOCKK:
                self.symtab.push()

            elif t.kind == StmtKind.DEFK:
                params = []
                p = t.child[0]

                while p:
                    params.append(p.type)
                    p = p.sibling

                self.symtab.funcs[t.attr] = {
                    'ret': t.type,
                    'params': params
                }

                self.symtab.push()

            elif t.kind == StmtKind.PARAMK:
                self.symtab.declare(t.attr, t.type, t.lineno)

    def post_visit(self, t):
        if t.nodekind == NodeKind.STMT:

            if t.kind in (StmtKind.BLOCKK, StmtKind.DEFK):
                self.symtab.pop()

            elif t.kind == StmtKind.VARDK:
                self.symtab.declare(t.attr, t.type, t.lineno)

        elif t.nodekind == NodeKind.EXP:

            if t.kind == ExpKind.IDK:
                t.type = self.symtab.lookup(t.attr, t.lineno)

            elif t.kind == ExpKind.CALLK:
                if t.attr not in self.symtab.funcs:
                    semantic_error(t.lineno, f"Função '{t.attr}' não declarada.")

                f_info = self.symtab.funcs[t.attr]
                t.type = f_info['ret']