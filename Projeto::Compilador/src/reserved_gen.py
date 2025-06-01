reserved = {
    'and' : 'AND',
    'array' : 'ARRAY',
    'begin' : 'BEGIN',
    'case' : 'CASE',
    'const' : 'CONST',
    'div' : 'DIV',
    'do' : 'DO',
    'downto' : 'DOWNTO',
    'else' : 'ELSE',
    'end' : 'END',
    'file' : 'FILE',
    'for' : 'FOR',
    'foward' : 'FOWARD',
    'function' : 'FUNCTION',
    'goto' : 'GOTO',
    'if' : 'IF',
    'in' : 'IN',
    'label' : 'LABEL',
    'mod' : 'MOD',
    'nil' : 'NIL',
    'not' : 'NOT',
    'of' : 'OF',
    'or' : 'OR',
    'packed' : 'PACKED',
    'procedure' : 'PROCEDURE',
    'program' : 'PROGRAM',
    'record' : 'RECORD',
    'repeat' : 'REPEAT',
    'set' : 'SET',
    'then' : 'THEN',
    'to' : 'TO',
    'type' : 'TYPE',
    'until' : 'UNTIL',
    'var' : 'VAR',
    'while' : 'WHILE',
    'with' : 'WITH'
}

code = ''

#   def t_TIPO(t):
#       r'[tT][iI][pP][oO]\b'
#       t.type = 'TIPO'
#       return t

for r, rType in reserved.items():
    code += f'\ndef t_{rType}(t):\n\t'
    code += "r'"
    for l in r:
        code += f'[{l}{l.capitalize()}]'
    code += r"\b'"
    code += f"\n\tt.type = '{rType}'"
    code += '\n\treturn t\n'

with open('./out/reserved.py', 'w') as f:
    f.write(code)
