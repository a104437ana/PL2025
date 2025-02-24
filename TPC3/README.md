# TPC3 : Conversor de MarkDown para HTML
## Data
- 24/02/2025
## Autor
- **Nome:** Ana Sá Oliveira
- **Número:** A104437
- **Fotografia:**
  
![Fotografia](../Fotografia.jpg)

## Resumo
### Objetivos
Criar em Python um pequeno conversor de MarkDown para HTML para os elementos descritos na "Basic
Syntax" da Cheat Sheet:

### Cabeçalhos
Linhas iniciadas por "# texto", ou "## texto" ou "### texto":

In:
```md
# Exemplo
```
Out:
```html
<h1>Exemplo</h1>
```

### Bold
Pedaços de texto entre "**":

In: 
```md
Este é um **exemplo** ...
```
Out:
```html
Este é um <b>exemplo</b> ...
```

### Itálico
Pedaços de texto entre "*":

In: 
```md
Este é um *exemplo* ...
```
Out: 
```html
Este é um <i>exemplo</i> ...
```
### Lista numerada

In:
```md
1. Primeiro item
2. Segundo item
3. Terceiro item
```
Out:
```html
<ol>
<li>Primeiro item</li>
<li>Segundo item</li>
<li>Terceiro item</li>
</ol>
```
### Link 
[texto](endereço URL)

In: 
```md
Como pode ser consultado em [página da UC](http://www.uc.pt)
```
Out:
```html
Como pode ser consultado em <a href="http://www.uc.pt">página da UC</a>
```
### Imagem 
![texto alternativo](path para a imagem)

In:
```md
Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ...
```
Out:
```html
Como se vê na imagem seguinte: <img src="http://www.coellho.com" alt="imagem
dum coelho"/> ...
```

### Resolução

Para resolver este trabalho, utilizei expressões regulares em Python para identificar e substituir elementos de formatação do MarkDown por suas equivalentes em HTML, garantindo a correta conversão de cabeçalhos, bold, itálico, listas numeradas, links e imagens. Para isto fiz a função **md_to_html** que recebe um texto MarkDown e coloca na saída o seu equivalente em HTML.

Neste programa, a função recebe o texto dado no stdin, que deverá ser MarkDown, e coloca o seu equivalente HTML na saída, no stdout.

### Testes
Para testar o programa, primeiro fiz um ficheiro MarkDown para podermos ver a sua conversão para HTML. O ficheiro chama-se **input.md**.

Podemos executar, no terminal, o seguinte comando, se quisermos que os resultados HTML apareçam no terminal:
```
python3 md_to_html.py < input.md
```
Se quisermos que os resultados apareçam num ficheiro, como o ficheiro **output.html**, podemos executar o seguinte comando:
```
python3 md_to_html.py < input.md > output.html
```
## Resultados
### Ficheiros resultantes deste trabalho
- O programa em Python que converte MarkDown para HTML: [md_to_html.py](md_to_html.py)
- O ficheiro de entrada MarkDown para testar: [input.md](input.md)
- O ficheiro de saída HTML resultado desse teste: [output.html](output.html)
- O manifesto que está a ler neste momento: [README.md](README.md)