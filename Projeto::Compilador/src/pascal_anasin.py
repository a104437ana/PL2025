import sys
import os
import ply.yacc as yacc
from ply.yacc import YaccProduction
from pascal_analex import tokens, literals
from pascal_exemplos import *
from pascal_ast import *

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
)

def p_program(p: YaccProduction):
    """program : PROGRAM ID ';' declarations code_block '.'
               | declarations code_block '.'"""
    if len(p) == 7:
        p[0] = Program(p[2], p[4], p[5])
    elif len(p) == 4:
        p[0] = Program(None, p[1], p[2])

def p_declarations(p: YaccProduction):
    """declarations : declarations declaration
                    |"""
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 1:
        p[0] = []

def p_declaration(p: YaccProduction):
    """declaration : variables_declaration
                   | function
                   | procedure"""
    p[0] = p[1]

def p_variables_declaration(p: YaccProduction):
    """variables_declaration : VAR variables_list"""
    p[0] = p[2]

def p_variables_list(p: YaccProduction):
    """variables_list : variables_list same_type_variables
                      | same_type_variables"""
    if len(p) == 3:
        p[0] = p[1]
        p[0].add(p[2])
    elif len(p) == 2:
        p[0] = Variables()
        p[0].add(p[1])

def p_same_type_variables(p: YaccProduction):
    """same_type_variables : id_list ':' DATATYPE ';'
                           | id_list ':' ARRAY '[' INT RANGE INT ']' OF DATATYPE ';' """
    vars = Variables()
    if len(p) == 5:
        for id in p[1]:
            vars.add(Variable(id, str(p[3]).lower()))
    elif len(p) == 12:
        for id in p[1]:
            vars.add(Variable(id, str(p[3]).lower(), True, int(p[7]) - int(p[5]) + 1, int(p[5]), p[10]))
    p[0] = vars

def p_id_list(p: YaccProduction):
    """id_list : id_list ',' ID
               | ID"""
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]

def p_var_or_not(p: YaccProduction):
    """var_or_not : variables_declaration
                  |"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 1:
        p[0] = Variables()

def p_function(p: YaccProduction):
    """function : FUNCTION ID '(' parameters ')' ':' DATATYPE ';' var_or_not code_block ';'"""
    p[0] = Function(p[2], p[4], p[7], p[9], p[10])

def p_procedure(p: YaccProduction):
    """procedure : PROCEDURE ID '(' parameters ')' ';' var_or_not code_block ';'"""
    p[0] = Procedure(p[2], p[4], p[7], p[8])

def p_parameters(p: YaccProduction):
    """parameters : parameter_list
                  |"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 1:
        p[0] = Variables()

def p_parameter_list(p: YaccProduction):
    """parameter_list : parameter_list ';' parameter
                      | parameter"""
    if len(p) == 4:
        p[0] = p[1]
        p[0].add(p[3])
    elif len(p) == 2:
        p[0] = Variables()
        p[0].add(p[1])

def p_parameter(p: YaccProduction):
    """
    parameter : VAR_opt id_list ':' DATATYPE
    """
    vars = Variables()
    if len(p) == 5:
        for id in p[2]:
            vars.add(Variable(id, str(p[4]).lower()))
    p[0] = vars

def p_VAR_opt(p: YaccProduction):
    """
    VAR_opt : VAR
            |
    """

def p_code_block(p: YaccProduction):
    """code_block : BEGIN algorithm END"""
    p[0] = CodeBlock(p[2])

def p_algorithm(p: YaccProduction):
    """algorithm : algorithm ';' statement
                 | statement"""
    if len(p) == 4:
        p[0] = p[1]
        p[0].add(p[3])
    elif len(p) == 2:
        p[0] = Algorithm()
        p[0].add(p[1])

def p_statement(p: YaccProduction):
    """statement : assignment
                 | func_call
                 | loop
                 | code_block
                 | if
                 | else
                 |"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 1:
        p[0] = None

def p_if(p: YaccProduction):
    """if : IF cond THEN statement %prec IFX"""
    p[0] = If(p[2], p[4])

def p_else(p: YaccProduction):
    """else : IF cond THEN statement ELSE statement"""
    p[0] = If(p[2], p[4], p[6])

def p_assignment(p: YaccProduction):
    """assignment : ID ASSIGNMENT cond
                  | ID '[' INT ']' ASSIGNMENT cond
                  | ID '[' ID ']' ASSIGNMENT cond"""
    if len(p) == 4:
        p[0] = Assignment(p[1], p[3])
    elif len(p) == 7:
        p[0] = Assignment(p[1], p[6], p[3], str(p.slice[3].type).lower())

def p_loop(p: YaccProduction):
    """loop : for
            | while"""
    p[0] = p[1]

def p_for(p: YaccProduction):
    """for : FOR for_cond DO statement"""
    p[0] = Loop("for", p[2][2], p[4], p[2][0], p[2][1])

def p_for_cond(p: YaccProduction):
    """for_cond : assignment TO cond
                | assignment DOWNTO cond"""
    p[0] = (p[1], str(p[2]).lower(), p[3])

def p_while(p: YaccProduction):
    """while : WHILE cond DO statement"""
    p[0] = Loop("while", p[2], p[4])

def p_cond(p: YaccProduction):
    """cond : expr
            | expr op_rel expr"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = BinaryOp(p[1], p[2], p[3])

def p_op_rel(p: YaccProduction):
    """op_rel : '='
              | NOT_EQUAL
              | '<'
              | LESS_EQUAL
              | '>'
              | GREATER_EQUAL"""
    p[0] = p[1]

def p_expr(p: YaccProduction):
    """expr : termo
            | expr op_ad termo"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = BinaryOp(p[1], p[2], p[3])

def p_termo(p: YaccProduction):
    """termo : fator
             | termo op_mul fator """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = BinaryOp(p[1], p[2], p[3])

def p_op_ad(p: YaccProduction):
    """op_ad : '+'
             | '-'
             | OR"""
    if p.slice[1].type == "OR":
        p[0] = str(p[1]).upper()
    else:
        p[0] = p[1]

def p_op_mul(p: YaccProduction):
    """op_mul : '*'
             | '/'
             | AND
             | MOD
             | DIV"""
    if p.slice[1].type in ["AND", "MOD", "DIV"]:
        p[0] = str(p[1]).upper()
    else:
        p[0] = p[1]

def p_fator(p: YaccProduction):
    """fator : value
             | '(' cond ')'
             | NOT fator"""
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 4:
        p[0] = p[2]
    if len(p) == 3:
        p[0] = UnaryOp("NOT", p[2])

def p_value(p: YaccProduction):
    """value : ID
             | INT
             | REAL
             | STRING
             | BOOL
             | ID '[' INT ']' 
             | ID '[' ID ']'
             | func_call
             | CHAR"""
    if p.slice[1].type == "ID":
        if len(p) == 2:
            p[0] = Value(str(p[1]), "id")
        elif len(p) == 5:
            p[0] = Value(str(p[1]), "array", p[3], str(p.slice[3].type).lower())
    elif p.slice[1].type == "INT":
        p[0] = Value(int(p[1]), "int")
    elif p.slice[1].type == "REAL":
        p[0] = Value(float(p[1]), "real")
    elif p.slice[1].type == "STRING":
        p[0] = Value(str(p[1]), "string")
    elif p.slice[1].type == "BOOL":
        b = str(p[1]).lower()
        if b == "true":
            p[0] = Value(int(1), "bool")
        elif b == "false":
            p[0] = Value(int(0), "bool")
    elif p.slice[1].type == "func_call":
        p[0] = p[1]
    elif p.slice[1].type == "CHAR":
        p[0] = Value(str(p[1]),"string")

def p_func_call(p: YaccProduction):
    """func_call : ID '(' args ')'"""
    p[0] = FunctionCall(p[1], p[3])

def p_args(p: YaccProduction):
    """args : elems
            |"""
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 1:
        p[0] = []

def p_elems(p: YaccProduction):
    """elems : elems ',' cond
             | cond"""
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    if len(p) == 2:
        p[0] = [p[1]]

def p_error(p: YaccProduction):
    if p:
        print(f"\033[1;31mSyntax error {p}\033[0m")
    else:
        print(f"\033[1;31mSyntax error at EOF\033[0m")
    parser.has_errors = True

parser = yacc.yacc(debug=True, write_tables=True, outputdir='.')
parser.has_errors = False

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
        print("\033[1;93mSyntax analysis:\033[0m")
        r = parser.parse(texto,debug=True)
        if parser.has_errors:
            print("\033[1;31mSyntax errors were found ❌\033[0m")
        else:
            print("\033[1;92mSyntax analysis completed without errors ✅\033[0m")