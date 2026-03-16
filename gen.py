from globals import NodeKind, StmtKind, ExpKind, TokenType

class Generator:
    def __init__(self):
        self.out = []
        self.indent = 0

    def emit(self, s):
        self.out.append(("    " * self.indent) + s)

    def generate(self, tree):
        self.traverse(tree)
        return "\n".join(self.out)

    def traverse(self, t):
        while t is not None:
            self.gen_node(t)
            t = t.sibling

    def gen_node(self, t):
        if t.nodekind == NodeKind.STMT:
            if t.kind == StmtKind.VARDK or t.kind == StmtKind.SETK:
                self.emit(f"{t.attr} = {self.gen_exp(t.child[0])}")
            elif t.kind == StmtKind.PRINTK:
                val = self.gen_exp(t.child[0]) if t.child[0] else ""
                self.emit(f"print({val})")
            elif t.kind == StmtKind.IFK:
                self.emit(f"if {self.gen_exp(t.child[0])}:")
                self.gen_block(t.child[1])
                if t.child[2]:
                    self.emit("else:")
                    self.gen_block(t.child[2])
            elif t.kind == StmtKind.WHILEK:
                self.emit(f"while {self.gen_exp(t.child[0])}:")
                self.gen_block(t.child[1])
            elif t.kind == StmtKind.DEFK:
                params = self.gen_params(t.child[0]) if t.child[0] else ""
                self.emit(f"def {t.attr}({params}):")
                self.gen_block(t.child[1])
            elif t.kind == StmtKind.RETK:
                self.emit(f"return {self.gen_exp(t.child[0])}")

    def gen_block(self, t):
        self.indent += 1
        if t and t.child[0]:
            self.traverse(t.child[0])
        else:
            self.emit("pass")
        self.indent -= 1

    def gen_params(self, t):
        p = []
        while t is not None:
            p.append(t.attr)
            t = t.sibling
        return ", ".join(p)

    def gen_exp(self, t):
        if not t: return ""
        if t.kind == ExpKind.CONSTK:
            return "True" if t.attr == "true" else "False" if t.attr == "false" else str(t.attr)
        elif t.kind == ExpKind.IDK:
            return t.attr
        elif t.kind == ExpKind.OPK:
            if t.attr == TokenType.NOT: return f"(not {self.gen_exp(t.child[0])})"
            if t.attr == TokenType.MINUS and not t.child[1]: return f"(-{self.gen_exp(t.child[0])})"
            op_map = {
                TokenType.PLUS: "+", TokenType.MINUS: "-", TokenType.TIMES: "*", 
                TokenType.OVER: "//", TokenType.EQ: "==", TokenType.NEQ: "!=", 
                TokenType.LT: "<", TokenType.GT: ">", TokenType.LE: "<=", TokenType.GE: ">=",
                TokenType.AND: "and", TokenType.OR: "or"
            }
            op = op_map.get(t.attr, "")
            return f"({self.gen_exp(t.child[0])} {op} {self.gen_exp(t.child[1])})"
        elif t.kind == ExpKind.CALLK:
            args = []
            p = t.child[0]
            while p is not None:
                args.append(self.gen_exp(p))
                p = p.sibling
            return f"{t.attr}({', '.join(args)})"
        return ""