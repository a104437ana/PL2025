from pascal_anasin import parser
from pascal_analex import tokens, literals, lexer
from pascal_exemplos import *
from run_code import runCode
import asyncio
import sys
import os
import re

if __name__ == "__main__":
    cwd = os.getcwd()
    if (len(sys.argv) <= 4 or len(sys.argv) >= 2) and not bool(re.match(r"\d", sys.argv[1])):
        f_in = open(f"{cwd}/{sys.argv[1]}", 'r')
        lines = f_in.readlines()
        codigo = "".join(lines)
        f_in.close()
    elif (len(sys.argv) <= 4 or len(sys.argv) >= 2) and bool(re.match(r"\d", sys.argv[1])):
        escolha = sys.argv[1]
        if escolha in exemplos:
            print(exemplos[escolha])
            codigo = exemplos[escolha]
    elif (len(sys.argv)==1):
        if os.isatty(sys.stdin.fileno()):
            codigo = input()
        else:
            codigo = sys.stdin.read()
    else:
        print("Incorrect arguments")
        print("py pascal_compiler.py <input file>")
        print("py pascal_compiler.py <input file> <output file>")
        print("py pascal_compiler.py <input file> -vm")
        sys.exit()

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
        print("\033[1;31mSemantic analysis ❌\033[0m")
        sys.exit()
    else:
        print("\033[1;92mSemantic analysis ✅\033[0m")
    code = ast.generateVmCode()
    if len(sys.argv) == 3 and sys.argv[2] != "-vm":
        if os.path.isdir(f"{cwd}/out"):
            out_dir = f"{cwd}/out"
        elif os.path.isdir(f"{cwd}/../out"):
            out_dir = f"{cwd}/../out"
        f_out = open(f"{out_dir}/{sys.argv[2]}", 'w')
        f_out.writelines(code)
        f_out.close()
    elif len(sys.argv) == 2 or len(sys.argv) == 1:
        print(code)
    elif (len(sys.argv) == 3 or len(sys.argv) == 4) and sys.argv[2] == "-vm":
        asyncio.run(runCode(code, sys.argv[3] if len(sys.argv) > 3 else None))
    else:
        print("Incorrect arguments")
        sys.exit()
