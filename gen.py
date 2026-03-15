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
            if t.kind == StmtKind.VARDK:
                self.emit(f"{t.attr} = {self.gen_exp(t.child[0])}")

            elif t.kind == StmtKind.SETK:
                self.emit(f"{t.attr} = {self.gen_exp(t.child[0])}")

            elif t.kind == StmtKind.PRINTK:
                val = self.gen_exp(t.child[0])
                self.emit(f"print({val})")

    def gen_exp(self, t):
        if not t:
            return ""

        if t.kind == ExpKind.CONSTK:
            if t.attr == "true":
                return "True"
            if t.attr == "false":
                return "False"
            return str(t.attr)

        elif t.kind == ExpKind.IDK:
            return t.attr

        elif t.kind == ExpKind.OPK:

            if t.attr == TokenType.NOT:
                return f"(not {self.gen_exp(t.child[0])})"

            if t.attr == TokenType.MINUS and not t.child[1]:
                return f"(-{self.gen_exp(t.child[0])})"

            op_map = {
                TokenType.PLUS: "+",
                TokenType.MINUS: "-",
                TokenType.TIMES: "*",
                TokenType.OVER: "//",
                TokenType.AND: "and",
                TokenType.OR: "or"
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