from pascal_anasin import parser
from pascal_analex import tokens, literals, lexer
from pascal_exemplos import *
import sys
import os

if __name__ == "__main__":
    codigo = ""
    if len(sys.argv) < 2:
        if os.isatty(sys.stdin.fileno()):
            codigo = input()
        else:
            codigo = sys.stdin.read()
    else:
        escolha = sys.argv[1]
        if escolha in exemplos:
            print(exemplos[escolha])
            codigo = exemplos[escolha]
    if codigo != "":
        lexer.has_errors = False
        print("\033[1;93mLexical analysis:\033[0m")
        lexer.input(codigo)
        for tok in lexer:
            pass
        if lexer.has_errors:
            print(f"\033[1;31mLexical analysis ❌\033[0m")
            sys.exit()
        else:
            print(f"\033[1;92mLexical analysis ✅\033[0m")

        parser.has_errors = False
        print("\033[1;93mSyntax analysis:\033[0m")
        ast = parser.parse(codigo)
        if parser.has_errors:
            print(f"\033[1;31mSyntax analysis  ❌\033[0m")
            sys.exit()
        else:
            print(f"\033[1;92mSyntax analysis  ✅\033[0m")
        
        print("\033[1;93mSemantic analysis:\033[0m")
        has_error = ast.anasem()
        if has_error:
            print("\033[1;31mSemantic errors were found ❌\033[0m")
            sys.exit()
        else:
            print("\033[1;92mSemantic analysis completed without errors ✅\033[0m")