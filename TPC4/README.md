# TPC4 : Analisador Léxico
## Data
- 06/03/2025
## Autor
- **Nome:** Ana Sá Oliveira
- **Número:** A104437
- **Fotografia:**
  
![Fotografia](../Fotografia.jpg)

## Resumo
### Objetivos
Construir um analisador léxico para uma liguagem de query com a qual se podem escrever frases do
género:
```
# DBPedia: obras de Chuck Berry

select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
```

### Resolução

Em primeiro lugar, para resolver este trabalho, tentei identificar qual era a linguagem de
query utilizada. Após uma pesquisa na internet, percebi rapidamente que se tratava de SPARQL,
uma linguagem específica para consultar dados armazenados no formato RDF, amplamente
utilizada em bases de dados como o DBpedia.

Nesta linguagem temos:
1. Comentários (COM): `"#.*"`;
2. Palavras reservadas:
    1. Select (SEL): `"select"`;
    2. Where (WHE): `"where"`;
    3. Limit (LIM): `"limit"`;
3. Pontuação (PON) que inclui o ponto (`.`) e as chavetas (`{`,`}`): `"[{\\.}]"`;
4. Variáveis (VAR): `"\\?\\w+"`;
5. Strings (STR): `"\".*\"`;
6. Linguagem dessa string (LAN): `"@\\w+"`;
7. Números (NUM): `"\\d+"`;
8. Predicados (PRE): `"a|\\w+:\\w+"`;

Nesta linguagem também temos caracteres que devem ser ignorados (SKIP) `"[ \\t]"` (espaços e tabs) e nova linha (NEWLINE) `"\\n"`.
Qualquer coisa diferente disto é erro na linguagem (ERRO) `"."`.

Tendo em conta isto, listei os tokens e as expressões regulares que os descrevem no ficheiro JSON, chamado **tokens_listas.json**.

Depois, peguei no gerador de analisadores léxicos do professor, **gen_tokenizer.py**, e fiz algumas alterações. Depois executei-o e obtive o analisador léxico, **analex.py**.

### Testes
Primeiro executamos o programa **gen_tokenizer.py**, que usa o ficheiro **tokens_listas.json**, para gerar o programa **analex.py**:
```
python3 gen_tokenizer.py > analex.py
```
Para testar o programa gerado, primeiro fiz um ficheiro .txt que tem como conteúdo a frase dada como exemplo, para podermos ver a sua analise léxica. O ficheiro chama-se **input.txt**.

Podemos executar, no terminal, o seguinte comando, se quisermos que os resultados apareçam no terminal:
```
python3 analex.py < input.txt
```
Se quisermos que os resultados apareçam num ficheiro, como o ficheiro **output.txt**, podemos executar o seguinte comando:
```
python3 analex.py < input.txt > output.txt
```
## Resultados
### Ficheiros resultantes deste trabalho
- O ficheiro JSON com os tipos de tokens e as expressões regulares que os descrevem: [tokens_listas.json](tokens_listas.json)
- O programa em Python que gera o analisador léxico apartir do JSON: [gen_tokenizer.py](gen_tokenizer.py)
- O programa em Python que é o analisador léxico: [analex.py](analex.py)
- O ficheiro de entrada .txt para testar: [input.txt](input.txt)
- O ficheiro de saída .txt resultado desse teste: [output.txt](output.txt)
- O manifesto que está a ler neste momento: [README.md](README.md)