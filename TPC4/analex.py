import sys
import re

def tokenize(input_string):
    reconhecidos = []
    linha = 1
    mo = re.finditer(r'(?P<COM>#.*)|(?P<SEL>select)|(?P<WHE>where)|(?P<LIM>limit)|(?P<PON>[{\.}])|(?P<VAR>\?\w+)|(?P<STR>".*")|(?P<LAN>@\w+)|(?P<NUM>\d+)|(?P<PRE>a|\w+:\w+)|(?P<SKIP>[ \t])|(?P<NEWLINE>\n)|(?P<ERRO>.)', input_string, re.IGNORECASE)
    for m in mo:
        dic = m.groupdict()
        if dic['COM']:
            t = ("COM", dic['COM'], linha, m.span())

        elif dic['SEL']:
            t = ("SEL", dic['SEL'], linha, m.span())
    
        elif dic['WHE']:
            t = ("WHE", dic['WHE'], linha, m.span())
    
        elif dic['LIM']:
            t = ("LIM", dic['LIM'], linha, m.span())
    
        elif dic['PON']:
            t = ("PON", dic['PON'], linha, m.span())
    
        elif dic['VAR']:
            t = ("VAR", dic['VAR'], linha, m.span())
    
        elif dic['STR']:
            t = ("STR", dic['STR'], linha, m.span())
    
        elif dic['LAN']:
            t = ("LAN", dic['LAN'], linha, m.span())
    
        elif dic['NUM']:
            t = ("NUM", dic['NUM'], linha, m.span())
    
        elif dic['PRE']:
            t = ("PRE", dic['PRE'], linha, m.span())
    
        elif dic['SKIP']:
            t = ("SKIP", dic['SKIP'], linha, m.span())
    
        elif dic['NEWLINE']:
            t = ("NEWLINE", dic['NEWLINE'], linha, m.span())
            linha+=1
        elif dic['ERRO']:
            t = ("ERRO", dic['ERRO'], linha, m.span())
    
        if not dic['SKIP']: reconhecidos.append(t)
    return reconhecidos

if sys.stdin.isatty():
    for linha in sys.stdin:
        for tok in tokenize(linha):
            print(tok)
else:
    for tok in tokenize(sys.stdin.read()):
        print(tok)
