from globals import NodeKind, MAXCHILDREN

class TreeNode:
    def __init__(self):
        self.child = [None] * MAXCHILDREN
        self.sibling = None
        self.lineno = 0
        self.nodekind = None
        self.kind = None
        self.attr = None 
        self.type = None 

def newStmtNode(kind):
    t = TreeNode()
    t.nodekind = NodeKind.STMT
    t.kind = kind
    return t

def newExpNode(kind):
    t = TreeNode()
    t.nodekind = NodeKind.EXP
    t.kind = kind
    return t