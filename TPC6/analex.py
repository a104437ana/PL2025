import ply.lex as lex

tokens = (
'NUMBER',
'PLUS',
'MINUS',
'TIMES',
)

t_NUMBER = r'\d+'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = '\t '

def t_error(t):
    print('Erro léxico, carácter desconhecido:', t.value[0], 'Linha:', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()
