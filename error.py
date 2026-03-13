import globals

class SyntaxErrors:
    EXPECTED = "Esperado {0}, encontrado {1}"
    INVALID_CMD = "Comando inválido. Token inesperado: {0}"
    INVALID_TYPE = "Tipo inválido. Esperado 'int', 'real', 'bool' ou 'void', encontrado '{0}'"
    INVALID_FACTOR = "Fator inválido na expressão. Encontrado: {0}"

def print_error(msg):
    print(f"Erro Sintático na linha {globals.lineno}: {msg}")
    exit(1)

def semantic_error(linha, msg):
    print(f"Erro Semântico na linha {linha}: {msg}")
    exit(1)