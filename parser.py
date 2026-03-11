from globals import *
import ast as ast_module
import json
import sys
from error import SyntaxErrors, print_error

token = None
lexer = None

def newStmtNode(kind):
    t = ast_module.newStmtNode(kind)
    t.lineno = token.line
    return t

def newExpNode(kind):
    t = ast_module.newExpNode(kind)
    t.lineno = token.line
    return t

def match(expected):
    global token
    if token.type == expected:
        token = lexer.getToken()
    else:
        exp_str = NOME_TOKENS.get(expected, expected.name)
        found_str = NOME_TOKENS.get(token.type, f"'{token.val}'") if token.val else token.type.name
        print_error(SyntaxErrors.EXPECTED.format(exp_str, found_str))

def parse(lex_instance):
    """
    <program> ::= <statement_list>
    """
    global lexer, token
    lexer = lex_instance
    token = lexer.getToken()
    return stmt_sequence()

def stmt_sequence():
    """
    <statement_list> ::= <statement> <statement_list> | ε
    """
    t = statement()
    p = t
    while token.type != TokenType.EOF and token.type != TokenType.RBRACE:
        q = statement()
        if q is not None:
            if t is None: t = p = q
            else:
                p.sibling = q
                p = q
    return t

def statement():
    """
    <statement> ::= <variable-decl> ";" | <assignment> ";" | <print-statement> ";"
                  | <if-statement> | <while-statement> | <return-statement> ";" | <function-decl>
    """
    if token.type == TokenType.VAR: return var_decl()
    elif token.type == TokenType.SET: return assign_stmt()
    elif token.type == TokenType.PRINT: return print_stmt()
    elif token.type == TokenType.IF: return if_stmt()
    elif token.type == TokenType.WHILE: return while_stmt()
    elif token.type == TokenType.RETURN: return return_stmt()
    elif token.type == TokenType.DEF: return func_decl()
    else: 
        encontrado = NOME_TOKENS.get(token.type, f"'{token.val}'")
        print_error(SyntaxErrors.INVALID_CMD.format(encontrado))

def parse_type():
    """
    <type> ::= "int" | "real" | "bool" | "void"
    """
    global token
    if token.type in (TokenType.INT, TokenType.REAL, TokenType.BOOL, TokenType.VOID):
        t = token.type
        match(token.type)
        return t
    print_error(SyntaxErrors.INVALID_TYPE.format(token.val))

def block():
    """
    <block> ::= "{" <statement_list> "}"
    """
    match(TokenType.LBRACE)
    t = newStmtNode(StmtKind.BLOCKK)
    t.child[0] = stmt_sequence()
    match(TokenType.RBRACE)
    return t

def var_decl():
    """
    <variable-decl> ::= "var" TK_ID ":" <type> "=" <expression>
    """
    t = newStmtNode(StmtKind.VARDK)
    match(TokenType.VAR)
    t.attr = token.val
    match(TokenType.ID)
    match(TokenType.COLON)
    t.type = parse_type()
    match(TokenType.ASSIGN)
    t.child[0] = expr()
    match(TokenType.SEMI)
    return t

def assign_stmt():
    """
    <assignment> ::= "set" TK_ID "=" <expression>
    """
    t = newStmtNode(StmtKind.SETK)
    match(TokenType.SET)
    t.attr = token.val
    match(TokenType.ID)
    match(TokenType.ASSIGN)
    t.child[0] = expr()
    match(TokenType.SEMI)
    return t

def print_stmt():
    """
    <print-statement> ::= "print" <expression> ";"
    """
    t = newStmtNode(StmtKind.PRINTK)
    match(TokenType.PRINT)
    t.child[0] = expr()
    match(TokenType.SEMI)
    return t

def func_decl():
    """
    <function-decl> ::= "def" TK_ID "(" <opt_formal_params> ")" ":" <type> <block>
    <opt_formal_params> ::= <formal-params> | ε
    """
    t = newStmtNode(StmtKind.DEFK)
    match(TokenType.DEF)
    t.attr = token.val
    match(TokenType.ID)
    match(TokenType.LPAREN)
    if token.type != TokenType.RPAREN:
        t.child[0] = formal_params()
    match(TokenType.RPAREN)
    match(TokenType.COLON)
    t.type = parse_type()
    t.child[1] = block()
    return t

def formal_params():
    """
    <formal-params> ::= <formal-param> <formal_param_tail>
    <formal_param_tail> ::= "," <formal-param> <formal_param_tail> | ε
    <formal-param> ::= TK_ID ":" <type>
    """
    t = newStmtNode(StmtKind.PARAMK)
    t.attr = token.val
    match(TokenType.ID)
    match(TokenType.COLON)
    t.type = parse_type()
    p = t
    while token.type == TokenType.COMMA:
        match(TokenType.COMMA)
        q = newStmtNode(StmtKind.PARAMK)
        q.attr = token.val
        match(TokenType.ID)
        match(TokenType.COLON)
        q.type = parse_type()
        p.sibling = q
        p = q
    return t

def if_stmt():
    """
    <if-statement> ::= "if" "(" <expression> ")" <block> <opt_else>
    <opt_else> ::= "else" <block> | ε
    """
    t = newStmtNode(StmtKind.IFK)
    match(TokenType.IF)
    match(TokenType.LPAREN)
    t.child[0] = expr()
    match(TokenType.RPAREN)
    t.child[1] = block()
    if token.type == TokenType.ELSE:
        match(TokenType.ELSE)
        t.child[2] = block()
    return t

def while_stmt():
    """
    <while-statement> ::= "while" "(" <expression> ")" <block>
    """
    t = newStmtNode(StmtKind.WHILEK)
    match(TokenType.WHILE)
    match(TokenType.LPAREN)
    t.child[0] = expr()
    match(TokenType.RPAREN)
    t.child[1] = block()
    return t

def return_stmt():
    """
    <return-statement> ::= "return" <expression>
    """
    t = newStmtNode(StmtKind.RETK)
    match(TokenType.RETURN)
    t.child[0] = expr()
    match(TokenType.SEMI)
    return t

def expr():
    """
    <expression> ::= <simple-expression> ( <relational-op> <simple-expression> )*
    <relational-op> ::= "<" | ">" | "==" | "!=" | "<=" | ">="
    """
    t = simple_exp()
    while token.type in (TokenType.LT, TokenType.GT, TokenType.EQ, TokenType.NEQ, TokenType.LE, TokenType.GE):
        p = newExpNode(ExpKind.OPK)
        p.child[0] = t
        p.attr = token.type
        match(token.type)
        p.child[1] = simple_exp()
        t = p
    return t

def simple_exp():
    """
    <simple-expression> ::= <term> ( <additive-op> <term> )*
    <additive-op> ::= "+" | "-" | "or"
    """
    t = term()
    while token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.OR):
        p = newExpNode(ExpKind.OPK)
        p.child[0] = t
        p.attr = token.type
        match(token.type)
        p.child[1] = term()
        t = p
    return t

def term():
    """
    <term> ::= <factor> ( <multiplicative-op> <factor> )*
    <multiplicative-op> ::= "*" | "/" | "and"
    """
    t = factor()
    while token.type in (TokenType.TIMES, TokenType.OVER, TokenType.AND):
        p = newExpNode(ExpKind.OPK)
        p.child[0] = t
        p.attr = token.type
        match(token.type)
        p.child[1] = factor()
        t = p
    return t

def factor():
    """
    <factor> ::= TK_LIT_INT | TK_LIT_REAL | TK_LIT_TRUE | TK_LIT_FALSE | TK_LIT_STRING
               | TK_ID <id_tail> | "(" <expression> ")" | <unary_op> <factor>
    <id_tail> ::= "(" <opt_actual_params> ")" | ε
    <unary_op> ::= "+" | "-" | "not"
    """
    t = None
    if token.type == TokenType.NUM or token.type == TokenType.REAL_NUM:
        t = newExpNode(ExpKind.CONSTK)
        t.attr = token.val
        t.type = TokenType.INT if token.type == TokenType.NUM else TokenType.REAL
        match(token.type)
    elif token.type in (TokenType.TRUE, TokenType.FALSE):
        t = newExpNode(ExpKind.CONSTK)
        t.attr = token.val
        t.type = TokenType.BOOL
        match(token.type)
    elif token.type == TokenType.STRING:
        t = newExpNode(ExpKind.CONSTK)
        t.attr = token.val
        t.type = TokenType.VOID
        match(token.type)
    elif token.type == TokenType.ID:
        name = token.val
        match(TokenType.ID)
        if token.type == TokenType.LPAREN: # Call
            t = newExpNode(ExpKind.CALLK)
            t.attr = name
            match(TokenType.LPAREN)
            if token.type != TokenType.RPAREN:
                t.child[0] = actual_params()
            match(TokenType.RPAREN)
        else:
            t = newExpNode(ExpKind.IDK)
            t.attr = name
    elif token.type == TokenType.LPAREN:
        match(TokenType.LPAREN)
        t = expr()
        match(TokenType.RPAREN)
    elif token.type in (TokenType.NOT, TokenType.MINUS, TokenType.PLUS):
        t = newExpNode(ExpKind.OPK)
        t.attr = token.type
        match(token.type)
        t.child[0] = factor()
    else:
        encontrado = NOME_TOKENS.get(token.type, f"'{token.val}'")
        print_error(SyntaxErrors.INVALID_FACTOR.format(encontrado))
    return t

def actual_params():
    """
    <actual-params> ::= <expression> <actual_params_tail>
    <actual_params_tail> ::= "," <expression> <actual_params_tail> | ε
    """
    t = expr()
    p = t
    while token.type == TokenType.COMMA:
        match(TokenType.COMMA)
        q = expr()
        p.sibling = q
        p = q
    return t

def ast_to_dict(t):
    if t is None: return None
    nodes = []
    
    while t:
        d = {
            "node": t.nodekind.name if t.nodekind else None,
            "kind": t.kind.name if t.kind else None,
            "linha": t.lineno
        }
        
        if t.attr is not None:
            d["attr"] = t.attr.name if hasattr(t.attr, 'name') else str(t.attr)
        if t.type is not None:
            d["type"] = t.type.name if hasattr(t.type, 'name') else str(t.type)
        
        children = [ast_to_dict(c) for c in t.child if c is not None]
        if children:
            d["children"] = children
            
        nodes.append(d)
        t = t.sibling
        
    return nodes if len(nodes) > 1 else (nodes[0] if nodes else None)

if __name__ == "__main__":
    from lexer import Lexer
    
    if len(sys.argv) < 2:
        print("Uso: python parser.py <arquivo.mini>")
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            code = f.read()
        
        lexer = Lexer(code)
        ast = parse(lexer)
        
        print("\n\nÁRVORE SINTÁTICA (JSON):\n")
        print(json.dumps(ast_to_dict(ast), indent=2))