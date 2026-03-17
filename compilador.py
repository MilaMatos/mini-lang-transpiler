import sys
import os
from lexer import Lexer
from parser import parse
from symtable import SemanticAnalyzer
from gen import Generator

def main():
    if len(sys.argv) < 2:
        print("Uso: python compilador.py <arquivo.mini>")
        return

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    try:
        lexer = Lexer(code)
        ast = parse(lexer)

        SemanticAnalyzer().analyze(ast)

        python_code = Generator().generate(ast)
        print("\n===== CÓDIGO PYTHON GERADO =====\n")
        print(python_code)

        print("\n===== EXECUTANDO O CÓDIGO =====\n")
        env = {"__builtins__": __builtins__}
        exec(python_code, env, env)

    except SystemExit:
        pass
    except Exception as e:
        print(f"\n[ERRO INTERNO] {e}")

if __name__ == "__main__":
    main()