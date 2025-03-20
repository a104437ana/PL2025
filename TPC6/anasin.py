import sys
from analex import lexer

prox_simb = ('Erro', '', 0, 0)

# função de erro
def parserError(simb,t):
    print('Erro sintático, token inesperado:', simb, 'Esperavamos um', t)
    print("A encerrar o programa...")
    sys.exit(1)

# função auxiliar
def rec_SubOp():
    global prox_simb
    if getattr(prox_simb,"type",None)=="NUMBER":
        value = prox_simb.value
        prox_simb = lexer.token()
        res = (value, rec_Operacao())
    else:
        if getattr(prox_simb,"value",None):
            parserError(prox_simb.value,"NUMBER")
        else:
            parserError("None","NUMBER")
    return res

# P2: Op -> PLUS NUMBER Op
# P3: Op -> MINUS NUMBER Op
# P4: Op -> TIMES NUMBER Op
# P5: Op -> ε
def rec_Operacao():
    global prox_simb
    if not prox_simb:
        print("Derivando por P5: Op -> ε")
        prox_simb = lexer.token()
        res = (None)
        print("Reconheci P5: Op -> ε")
    elif getattr(prox_simb,"type",None)=="PLUS":
        print("Derivando por P2: Op -> PLUS NUMBER Op")
        value = prox_simb.value
        prox_simb = lexer.token()
        res = (value,rec_SubOp())
        print("Reconheci P2: Op -> PLUS NUMBER OP")
    elif getattr(prox_simb,"type",None)=="MINUS":
        print("Derivando por P3: Op -> MINUS NUMBER OP")
        value = prox_simb.value
        prox_simb = lexer.token()
        res = (value,rec_SubOp())
        print("Reconheci P3: Op -> MINUS NUMBER Op")
    elif getattr(prox_simb,"type",None)=="TIMES":
        print("Derivando por P4: Op -> TIMES NUMBER Op")
        value = prox_simb.value
        prox_simb = lexer.token()
        res = (value,rec_SubOp())
        print("Reconheci P4: Op -> TIMES NUMBER Op")
    else:
        parserError(prox_simb.value,"PLUS | MINUS | TIMES | ε")
    return res

# P1: Expr -> NUMBER Op
def rec_Expressao():
    global prox_simb
    if getattr(prox_simb,"type",None)=="NUMBER":
        print("Derivando por P1: Expr -> NUMBER Op")
        value = prox_simb.value
        prox_simb = lexer.token()
        res = (value, rec_Operacao())
        print("Reconheci P1: Expr -> NUMBER Op")
    else:
        if getattr(prox_simb,"value",None):
            parserError(prox_simb.value,"NUMBER")
        else:
            parserError("None","NUMBER")
    return res

# função principal da análise sintática
def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    return rec_Expressao()