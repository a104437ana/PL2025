import sys

def somador(texto):
    soma = 0
    somar = True
    i = 0
    while i < len(texto):
        if (texto[i] == '='):
            print(soma)
            i = i + 1
        elif (texto[i].lower() == 'o'):
            i = i + 1
            if (i < len(texto)):
                if (texto[i].lower() == 'n'):
                    somar = True
                    i = i + 1
                elif (texto[i].lower() == 'f'):
                    i = i + 1
                    if (i < len(texto)):
                        if (texto[i].lower() =='f'):
                            somar = False
                            i = i + 1
        elif (texto[i] in "0123456789" and somar == True):
            valor = 0
            while (i < len(texto)):
                if (texto[i] in "0123456789"):
                    valor = valor * 10 + int(texto[i])
                    i = i + 1
                else:
                    break
            soma += valor
        else:
            i = i + 1
            
if sys.stdin.isatty():
    for linha in sys.stdin:
        somador(linha)
else:
    somador(sys.stdin.read())