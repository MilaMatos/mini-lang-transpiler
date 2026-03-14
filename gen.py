from globals import NodeKind, StmtKind, ExpKind

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

            elif t.kind == StmtKind.PRINTK:
                val = self.gen_exp(t.child[0])
                self.emit(f"print({val})")

    def gen_exp(self, t):
        if not t:
            return ""

        if t.kind == ExpKind.CONSTK:
            return str(t.attr)

        elif t.kind == ExpKind.IDK:
            return t.attr

        return ""
