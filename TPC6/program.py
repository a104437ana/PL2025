from anasin import rec_Parser

def mult(acc, arvore):
    if arvore is None:
        return acc, None

    op, (r1, r2) = arvore
    if op == '*':
        acc = int(acc) * int(r1)
        res = mult(acc, r2)
        return res
    else:
        return (acc, (op, mult(r1, r2)))

def add_sub(acc, arvore):
    if arvore is None:
        return acc, None

    op, (r1, r2) = arvore

    if op == '+':
        acc = int(acc) + int(r1)
        res = add_sub(acc, r2)
        return res
    if op == '-':
        acc = int(acc) - int(r1)
        res = add_sub(acc, r2)
        return res
    else:
        return (acc, (op, add_sub(r1, r2)))

def calculate(arvore):
    acc, r = arvore
    arvore = mult(acc, r)

    acc, r = arvore
    arvore = add_sub(acc, r)

    return arvore[0]

linha = input("Introduza uma expressão aritmética simples: ")
arvore = rec_Parser(linha)
print(arvore)
print("-------------------------")
print("Expressão:", linha)
print("O valor correto da expressão é", calculate(arvore))