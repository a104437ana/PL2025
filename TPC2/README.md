# TPC1 : Análise de um dataset de obras musicais
## Data
- 16/02/2025
## Autor
- **Nome:** Ana Sá Oliveira
- **Número:** A104437
- **Fotografia:**
  
![Fotografia](../Fotografia.jpg)

## Resumo
### Objetivos
- Neste TPC, é proibido usar o módulo CSV do Python;
- Deverás ler o dataset, processá-lo e criar os seguintes resultados:
  1. Lista ordenada alfabeticamente dos compositores musicais;
  2. Distribuição das obras por período: quantas obras catalogadas em cada período;
  3. Dicionário em que a cada período está associada uma lista alfabética dos títulos das obras desse período.

### Resolução

Em primeiro lugar, percebi que o dataset **obras.csv** é um ficheiro **CSV** (**Comma-Separated Values**), ou seja, é um ficheiro de texto estruturado onde os dados são organizados em linhas, e os valores dentro de cada linha são separados por um delimitador, geralmente uma vírgula, mas podendo ser outro caractere, como ponto e vírgula ou tabulação.

Em segundo lugar, abri o CSV e percebi que cada obra musical irá ter os seguintes valores:
1. Nome
2. Descrição
3. Ano de Criação
4. Período
5. Compositor
6. Duração
7. Identificador
  
e todos eles separados por ponto e vírgula (**;**).

Em terceiro lugar, percebi que as obras musicais não estão uma em cada linha, como devia ser. Neste dataset, o que separa uma obra musical de outra é o new line, nova linha (**\n**) quando (**?=**) é seguido imediatamente de um caracter não branco (**\S**), ou seja, um caracter que não seja o espaço, nova linha ou tabulação. Podemos observar que quando se muda de linha e depois temos tabulação é porque continuamos na mesma obra musical. Se mudarmos de linha e imediatamente tivermos um caracter não branco, então ai é porque já mudamos de obra musical. Assim, queremos dividir o texto (**split**) com o delimitador de nova linha (**\n**) quando (**?=**) este está antes de um caracter não branco (**\S**), para assim obtermos a lista das obras musicais. Expressão regular para isto:
```
\n(?=\S)
```
O **?=** serve para não incluir o caracter não branco no delimitador. Afinal, o delimitador é apenas new line, apenas temos a restrição de o delimitador ser a new line quando esta está seguida de um caracter não branco. O caracter não branco não é para ser consumido, logo não faz parte do delimitador.

Depois cada obra musical será dividida (**split**) numa lista de valores e estes estão delimitados por ponto e vírgula (**;**). Expressão regular para isto:
```
;
```
Em quarto lugar, depois de já ter uma lista de listas de valores, percebi que algumas listas de valores tinham tamanho superior a 7, mais campos do que deviam. Depois de alguma análise percebi que na descrição das obras musicais, muitas vezes aparecia o caracter ponto e vírgula (**;**), o que o programa interpretava como final da descrição, mesmo não o sendo. Assim, mudei o programa para ter em atenção isto.

Por fim, com a lista de listas de valores já válida, procedi a criar os resultados pedidos, colocando-os na saída.

### Testes
Para testar o programa, podemos executar, no terminal, o seguinte comando, se quisermos que os resultados apareçam no terminal:
```
python3 programa.py
```
Se quisermos que os resultados apareçam num ficheiro, como o ficheiro **resultados.txt**, podemos executar o seguinte comando:
```
python3 programa.py > resultados.txt
```
## Resultados
### Ficheiros resultantes deste trabalho
- O dataset das obras musicais, um ficheiro CSV, fornecido pelo professor: [obras.csv](obras.csv)
- O programa em Python que le o dataset, processá-o e cria os resultados: [programa.py](programa.py)
- O ficheiro de saída resultado de um teste: [resultados.txt](resultados.txt)
- O manifesto que está a ler neste momento: [README.md](README.md)