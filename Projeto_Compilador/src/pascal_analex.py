import sys
import os
import ply.lex as lex
from pascal_exemplos import *

reserved = [
    'AND',
    'ARRAY',
    'BEGIN',
    'CASE',
    'CONST',
    'DIV',
    'DO',
    'DOWNTO',
    'ELSE',
    'END',
    'FILE',
    'FOR',
    'FOWARD',
    'FUNCTION',
    'GOTO',
    'IF',
    'IN',
    'LABEL',
    'MOD',
    'NIL',
    'NOT',
    'OF',
    'OR',
    'PACKED',
    'PROCEDURE',
    'PROGRAM',
    'RECORD',
    'REPEAT',
    'SET',
    'THEN',
    'TO',
    'TYPE',
    'UNTIL',
    'VAR',
    'WHILE',
    'WITH'
]

tokens = [
    'NOT_EQUAL',
    'LESS_EQUAL',
    'GREATER_EQUAL',
    'ASSIGNMENT',
    'RANGE',
    'LPA','ARP','LPP','PRP',
    'BOOL',
    'DATATYPE',
    'ID',
    'INT',
    'REAL',
    'CHAR',
    'STRING',
    'COMMENT'
    
] + reserved

literals = [
    '+',
    '-',
    '*',
    '/',
    '=',
    '<',
    '>',
    '[',
    ']',
    '.',
    ',',
    ':',
    ';',
    '^',
    '(',
    ')']

t_NOT_EQUAL = r'<>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_ASSIGNMENT = r":="
t_RANGE = r'\.\.'

t_LPA = r'\(\*'
t_ARP = r'\*\)'
t_LPP = r'\(\.'
t_PRP = r'\.\)'

def t_AND(t):
	r'[aA][nN][dD]\b'
	return t

def t_ARRAY(t):
	r'[aA][rR][rR][aA][yY]\b'
	return t

def t_BEGIN(t):
	r'[bB][eE][gG][iI][nN]\b'
	return t

def t_CASE(t):
	r'[cC][aA][sS][eE]\b'
	return t

def t_CONST(t):
	r'[cC][oO][nN][sS][tT]\b'
	return t

def t_DIV(t):
	r'[dD][iI][vV]\b'
	return t

def t_DO(t):
	r'[dD][oO]\b'
	return t

def t_DOWNTO(t):
	r'[dD][oO][wW][nN][tT][oO]\b'
	return t

def t_ELSE(t):
	r'[eE][lL][sS][eE]\b'
	return t

def t_END(t):
	r'[eE][nN][dD]\b'
	return t

def t_FILE(t):
	r'[fF][iI][lL][eE]\b'
	return t

def t_FOR(t):
	r'[fF][oO][rR]\b'
	return t

def t_FOWARD(t):
	r'[fF][oO][wW][aA][rR][dD]\b'
	return t

def t_FUNCTION(t):
	r'[fF][uU][nN][cC][tT][iI][oO][nN]\b'
	return t

def t_GOTO(t):
	r'[gG][oO][tT][oO]\b'
	return t

def t_IF(t):
	r'[iI][fF]\b'
	return t

def t_IN(t):
	r'[iI][nN]\b'
	return t

def t_LABEL(t):
	r'[lL][aA][bB][eE][lL]\b'
	return t

def t_MOD(t):
	r'[mM][oO][dD]\b'
	return t

def t_NIL(t):
	r'[nN][iI][lL]\b'
	return t

def t_NOT(t):
	r'[nN][oO][tT]\b'
	return t

def t_OF(t):
	r'[oO][fF]\b'
	return t

def t_OR(t):
	r'[oO][rR]\b'
	return t

def t_PACKED(t):
	r'[pP][aA][cC][kK][eE][dD]\b'
	return t

def t_PROCEDURE(t):
	r'[pP][rR][oO][cC][eE][dD][uU][rR][eE]\b'
	return t

def t_PROGRAM(t):
	r'[pP][rR][oO][gG][rR][aA][mM]\b'
	return t

def t_RECORD(t):
	r'[rR][eE][cC][oO][rR][dD]\b'
	return t

def t_REPEAT(t):
	r'[rR][eE][pP][eE][aA][tT]\b'
	return t

def t_SET(t):
	r'[sS][eE][tT]\b'
	return t

def t_THEN(t):
	r'[tT][hH][eE][nN]\b'
	return t

def t_TO(t):
	r'[tT][oO]\b'
	return t

def t_TYPE(t):
	r'[tT][yY][pP][eE]\b'
	return t

def t_UNTIL(t):
	r'[uU][nN][tT][iI][lL]\b'
	return t

def t_VAR(t):
	r'[vV][aA][rR]\b'
	return t

def t_WHILE(t):
	r'[wW][hH][iI][lL][eE]\b'
	return t

def t_WITH(t):
	r'[wW][iI][tT][hH]\b'
	return t

def t_BOOL(t):
    r'([tT][rR][uU][eE]|[fF][aA][lL][sS][eE])\b'
    return t

def t_DATATYPE(t):
    r"([iI][nN][tT][eE][gG][eE][rR]|[rR][eE][aA][lL]|[cC][hH][aA][rR]|[bB][oO][oO][lL][eE][aA][nN]|[sS][tT][rR][iI][nN][gG])\b"
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_REAL(t):
    r'[+-]?(\d+\.\d+([eE][+-]?\d+)?|\d+[eE][+-]?\d+)'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'[+-]?\d+'
    t.value = int(t.value)
    return t

def t_CHAR(t):
    r"'(.)'"
    return t

def t_STRING(t):
    r'\'[^\']+\'|\"[^\"]*\"'
    return t

t_ignore_COMMENT = r"\{(.|\n)*?\}|\(\*(.|\n)*?\*\)"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("\033[1;31mIllegal character ('%s',%s,%s)\033[0m"% (t.value[0], t.lineno, t.lexpos))
    t.lexer.has_errors = True
    t.lexer.skip(1)

lexer = lex.lex()
lexer.has_errors = False

if __name__ == "__main__":
    texto = ""
    if len(sys.argv) < 2:
        if os.isatty(sys.stdin.fileno()):
            texto = input()
        else:
            texto = sys.stdin.read()
    else:
        escolha = sys.argv[1]
        if escolha in exemplos:
            print(exemplos[escolha])
            texto = exemplos[escolha]
    if texto != "":
        print("\033[1;93mLexical analysis:\033[0m")
        lexer.input(texto)
        for tok in lexer:
            print(tok)
        if lexer.has_errors:
            print("\033[1;31mLexical errors were found ❌\033[0m")
        else:
            print("\033[1;92mLexical analysis completed without errors ✅\033[0m")
