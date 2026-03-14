from globals import NodeKind, StmtKind, ExpKind, TokenType
from error import semantic_error

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]
        self.funcs = {}

    def push(self): self.scopes.append({})
    def pop(self): self.scopes.pop()

    def declare(self, name, typ, line):
        if name in self.scopes[-1]:
            semantic_error(line, f"Variável '{name}' já declarada neste escopo.")
        self.scopes[-1][name] = typ

    def lookup(self, name, line):
        for s in reversed(self.scopes):
            if name in s: return s[name]
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
                if t.child[i]: self.traverse(t.child[i])
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
                # Salva os tipos dos parametros para validar depois
                self.symtab.funcs[t.attr] = {'ret': t.type, 'params': params}
                self.symtab.push()
            elif t.kind == StmtKind.PARAMK:
                self.symtab.declare(t.attr, t.type, t.lineno)

    def post_visit(self, t):
        if t.nodekind == NodeKind.STMT:
            if t.kind in (StmtKind.BLOCKK, StmtKind.DEFK):
                self.symtab.pop()
            elif t.kind == StmtKind.VARDK:
                self.symtab.declare(t.attr, t.type, t.lineno)
                if t.child[0] and t.child[0].type != t.type:
                    if not (t.type == TokenType.REAL and t.child[0].type == TokenType.INT):
                        semantic_error(t.lineno, f"Atribuição inválida. '{t.attr}' recebeu tipo incompatível.")
            elif t.kind == StmtKind.SETK:
                var_type = self.symtab.lookup(t.attr, t.lineno)
                if t.child[0] and t.child[0].type != var_type:
                    if not (var_type == TokenType.REAL and t.child[0].type == TokenType.INT):
                        semantic_error(t.lineno, f"Atribuição inválida. Tipos incompatíveis em '{t.attr}'.")
        
        elif t.nodekind == NodeKind.EXP:
            if t.kind == ExpKind.IDK:
                t.type = self.symtab.lookup(t.attr, t.lineno)
            elif t.kind == ExpKind.OPK:
                t0 = t.child[0].type if t.child[0] else None
                t1 = t.child[1].type if t.child[1] else None
                
                # Bloqueia matemática com booleanos
                if t.attr in (TokenType.PLUS, TokenType.MINUS, TokenType.TIMES, TokenType.OVER):
                    if t0 == TokenType.BOOL or t1 == TokenType.BOOL:
                        semantic_error(t.lineno, "Operador matemático inválido para booleanos.")
                    t.type = TokenType.REAL if (t0 == TokenType.REAL or t1 == TokenType.REAL) else TokenType.INT
                
                # Bloqueia relacionais incompatíveis (ex: bool <= int)
                elif t.attr in (TokenType.LT, TokenType.GT, TokenType.EQ, TokenType.NEQ, TokenType.LE, TokenType.GE):
                    if t0 == TokenType.BOOL or t1 == TokenType.BOOL:
                        if t.attr not in (TokenType.EQ, TokenType.NEQ) or t0 != t1:
                            semantic_error(t.lineno, "Operador relacional inválido para os tipos fornecidos.")
                    t.type = TokenType.BOOL
                
                # Operadores lógicos (and, or, not)
                else:
                    t.type = TokenType.BOOL
                    
            elif t.kind == ExpKind.CALLK:
                if t.attr not in self.symtab.funcs:
                    semantic_error(t.lineno, f"Função '{t.attr}' não declarada.")
                
                f_info = self.symtab.funcs[t.attr]
                t.type = f_info['ret']
                
                args = []
                a = t.child[0]
                while a:
                    args.append(a.type)
                    a = a.sibling
                    
                if len(args) != len(f_info['params']):
                    semantic_error(t.lineno, f"A função '{t.attr}' espera {len(f_info['params'])} argumentos.")
                for i in range(len(args)):
                    if args[i] != f_info['params'][i]:
                        semantic_error(t.lineno, f"Argumento {i+1} da função '{t.attr}' tem tipo incompatível.")