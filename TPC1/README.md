# TPC1 : Somador on/off 
## Data
- 13/02/2025
## Autor
- **Nome:** Ana Sá Oliveira
- **Número:** A104437
- **Fotografia:**
  
![Fotografia](../Fotografia.jpg)

## Resumo
### Objetivos
1. Neste trabalho pretende-se criar um programa em Python que some todas as sequências de dígitos que encontre num texto.

2. Sempre que encontrar a string "Off" em qualquer combinação de maiúsculas e minúsculas,
esse comportamento é desligado.

3. Sempre que encontrar a string "On" em qualquer combinação de maiúsculas e minúsculas,
esse comportamento é novamente ligado.

4. Sempre que encontrar o caráter "=", o resultado da soma é colocado na saída.

5. No fim, coloca o valor da soma na saída.

### Resolução

Em primeiro lugar, defini uma função **somador** que recebe um texto e executa o comportamento descrito em cima.

Em segundo lugar, defini que, neste programa, todo o conteúdo lido da entrada padrão (stdin) será passado para a função **somador**.

### Testes
Primeiro comando:
```
python3 somador.py < ficheiro1.txt > resultado1.txt
```
Conteúdo do ficheiro de entrada (ficheiro1.txt - ficheiro inspirado no exemplo dado na aula teórica):
```
Olá Mundo!.45HelloWorld?
hojeédia2025.02.07olá
=oiOLÁOFfadeus
?./789Çç43
oleon...2,,
*-5=
```
Conteúdo do ficheiro de saída (resultado1.txt):
```
2079
2086
2086

```
Segundo comando:
```
python3 somador.py < ficheiro2.txt > resultado2.txt
```
Conteúdo do ficheiro de entrada (ficheiro2.txt):
```
1.2
=
oFF1
1=On1=
```
Conteúdo do ficheiro de saída (resultado2.txt):
```
3
3
4
4

```
Terceiro comando:
```
python3 somador.py
```
Depois coloquei no terminal:
```
ola1,
m7=a3.oFf1=
on1=4aoN=

```
Depois, na última linha vazia, introduzi **EOF** (End of File) ao pressionar **Ctrl+D**, uma vez que o sistema operativo do meu computador é **Linux**. Fiz isto para informar o programa de que não há mais conteúdo para ler da entrada padrão (**stdin**), pois chegámos ao fim do ficheiro (**EOF**). Assim, o programa irá ler todo o conteúdo do stdin e esse conteúdo será depois processado pela função **somador**.

Depois obtive na saída, neste caso no terminal, o seguinte resultado:
```
8
11
12
16
16
```
Todos estes testes provam que o programa funciona corretamente.
## Resultados
### Ficheiros resultantes deste trabalho
- O programa em Python que soma todas as sequências de digítos que encontre num texto: [somador.py](somador.py)
- Os ficheiros de teste:
  - Os ficheiros de entrada: [ficheiro1.txt](ficheiro1.txt) e [ficheiro2.txt](ficheiro2.txt)
  - Os ficheiros de saída respetivos: [resultado1.txt](resultado1.txt) e [resultado2.txt](resultado2.txt)
- O manifesto que está a ler neste momento: [README.md](README.md)