import json

tokens = []
with open("tokens_listas.json") as f:
    tokens = json.load(f)

tokens_regex = '|'.join([f'(?P<{t["id"]}>{t["expreg"]})' for t in tokens])

code = f"""import sys
import re

def tokenize(input_string):
    reconhecidos = []
    linha = 1
    mo = re.finditer(r'{tokens_regex}', input_string, re.IGNORECASE)
    for m in mo:
        dic = m.groupdict()
        if dic['{tokens[0]['id']}']:
            t = ("{tokens[0]['id']}", dic['{tokens[0]['id']}'], linha, m.span())
"""

for t in tokens[1:]:
    code += f"""
        elif dic['{t['id']}']:
            t = ("{t['id']}", dic['{t['id']}'], linha, m.span())
    """
    if t['id'] == 'NEWLINE':
        code += f"""        linha+=1"""
code += f"""
        if not dic['SKIP']: reconhecidos.append(t)
    return reconhecidos

if sys.stdin.isatty():
    for linha in sys.stdin:
        for tok in tokenize(linha):
            print(tok)
else:
    for tok in tokenize(sys.stdin.read()):
        print(tok)"""
print(code)