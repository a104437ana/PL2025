# TPC5 : Analisador Léxico, Sintático e Avaliador de Expressões Aritméticas Simples
## Data
- 20/03/2025
## Autor
- **Nome:** Ana Sá Oliveira
- **Número:** A104437
- **Fotografia:**
  
![Fotografia](../Fotografia.jpg)

## Resumo
### Objetivos
O objetivo deste trabalho é desenvolver um analisador léxico e sintático, utilizando a técnica de análise recursiva descendente, para interpretar expressões aritméticas simples, como:
```
5 + 3 * 2
2 * 7 - 5 * 3
```
Além da análise, o programa deve ser capaz de calcular corretamente o valor da expressão fornecida como entrada.

Este programa lida apenas com expressões aritméticas simples, ou seja, lida apenas com números inteiros não negativos e com as operações de adição, subtração e multiplicação. Este programa não lida com parênteses.
### Resolução

Em primeiro lugar, defini que:

```
T =  {'+', '-', '*', number}

S = Expr

N = {Expr, Op}

P = {

    (P1) Expr -> number Op

    (P2) Op -> + number Op
    (P3)     | - number Op
    (P4)     | * number Op
    (P5)     | ε

}
```
Para chegar aquelas regras P, parti deste conhecimento:
```
Expr -> number + Expr
      | number - Expr
      | number * Expr
      | number
```
Para transformar isto nas regras P, pus o "number" em evidência.

Com base em **T**, **S**, **N** e **P**, desenvolvi o analisador léxico (**analex.py**) e o analisador sintático (**anasin.py**).

Neste programa os erros léxicos são ignorados (mas somos avisados que ocorreram) e os erros sintáticos terminam o programa. O analisador sintático, se não encontrar erros, gera uma árvore de análise sintática.

Percorrendo esta árvore, podemos avaliar o valor da expressão aritmética simples. Fazemos isto no programa **program.py**, o programa principal.

### Testes
Para testar, executamos o programa **program.py** com o seguinte comando:
```
python3 program.py
```
Depois podemos dar uma expressão que queiramos avaliar, por exemplo:
```
Introduza uma expressão aritmética simples: 5 + 3 * 2
```
Output:
```
Derivando por P1: Expr -> NUMBER Op
Derivando por P2: Op -> PLUS NUMBER Op
Derivando por P4: Op -> TIMES NUMBER Op
Derivando por P5: Op -> ε
Reconheci P5: Op -> ε
Reconheci P4: Op -> TIMES NUMBER Op
Reconheci P2: Op -> PLUS NUMBER OP
Reconheci P1: Expr -> NUMBER Op
('5', ('+', ('3', ('*', ('2', None)))))
-------------------------
Expressão: 5 + 3 * 2
O valor correto da expressão é 11
```
Outro exemplo:
```
Introduza uma expressão aritmética simples: 2 * 7 - 5 * 3
```
Output:
```
Derivando por P1: Expr -> NUMBER Op
Derivando por P4: Op -> TIMES NUMBER Op
Derivando por P3: Op -> MINUS NUMBER OP
Derivando por P4: Op -> TIMES NUMBER Op
Derivando por P5: Op -> ε
Reconheci P5: Op -> ε
Reconheci P4: Op -> TIMES NUMBER Op
Reconheci P3: Op -> MINUS NUMBER Op
Reconheci P4: Op -> TIMES NUMBER Op
Reconheci P1: Expr -> NUMBER Op
('2', ('*', ('7', ('-', ('5', ('*', ('3', None)))))))
-------------------------
Expressão: 2 * 7 - 5 * 3
O valor correto da expressão é -1
```
## Resultados
### Ficheiros resultantes deste trabalho
- O analisador léxico: [analex.py](analex.py)
- O analisador sintático: [anasin.py](anasin.py)
- O avaliador de expressões aritméticas e o programa principal: [program.py](program.py)
- O manifesto que está a ler neste momento: [README.md](README.md)