# TPC5 : Máquina de Vending
## Data
- 09/03/2025
## Autor
- **Nome:** Ana Sá Oliveira
- **Número:** A104437
- **Fotografia:**
  
![Fotografia](../Fotografia.jpg)

## Resumo
### Objetivos
Pediram-te para construir um programa que simule uma máquina de vending.

A máquina tem um stock de produtos: uma lista de triplos, nome do produto, quantidade e preço.
```
stock = [
{"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7},
...
]
```
Podes persistir essa lista num ficheiro em JSON que é carregado no arranque do programa e é atulizado
quando o programa termina.

A seguir apresenta-se um exemplo de uma interação com a máquina, assim que esta é ligada, para que
possas perceber o tipo de comandos que a máquina aceita (as linhas iniciadas marcadas com >>
representam o input do utilizador):
```
maq: 2024-03-08, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq:
cod | nome | quantidade | preço
---------------------------------
A23 água 0.5L 8 0.7
...
>> MOEDA 1e, 20c, 5c, 5c .
maq: Saldo = 1e30c
>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 60c
>> SELECIONAR A23
maq: Saldo insufuciente para satisfazer o seu pedido
maq: Saldo = 60c; Pedido = 70c
>> ...
...
maq: Saldo = 74c
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 20c e 2x 2c.
maq: Até à próxima
```
O stock encontra-se inicialmente armazenado num ficheiro JSON de nome "stock.json" que é carregado
em memória quando o programa arranca. Quando o programa termina, o stock é gravado no mesmo
ficheiro, mantendo assim o estado da aplicação entre interações.

Use a imaginação e criatividade e tente contemplar todos os cenários, por exemplo, produto inexistente ou
stock vazio.

Como extra pode adicionar um comando para adicionar alguns produtos ao stock existente (produtos
novos ou já existentes).
### Resolução

Em primeiro lugar, criei o ficheiro **stock.json** e adicionei produtos aleatórios ao stock.

Em segundo lugar, criei o ficheiro **maq.py** que é o programa em Python que simula uma máquina de vending.
Implementei todas as operações descritas no enunciado, incluindo a operação extra de adicionar alguns produtos
ao stock existente (produtos novos ou já existentes). Outro extra que fiz foi uma operação para ver o saldo atual. Tive em conta todos
os cenários possíveis, por exemplo, produto inexistente ou
stock vazio. Nesta máquina de vending considerei que os códigos deviam ser formados por uma letra seguida de dois digitos.

### Testes
Para simular a máquina de vending, executamos o programa **maq.py** com o seguinte comando:
```
python3 maq.py
```
Depois podemos simular várias operações, por exemplo:
- Listar os produtos do stock: ``LISTAR``
- Carregar uma moeda de 1 euro e outra de 20 centimos na máquina: ``MOEDA 1e, 20c .``
- Selecionar um produto de código A23: ``SELECIONAR A23``
- Sair da máquina e receber o troco se houver: ``SAIR``
- Adicionar um novo produto ao stock de código E23, nome KitKat, 2 quantidades e preço 1.9: ``NOVO E23 "KitKat" 2 1.9``
- Adicionar 2 quantidades do produto de código B12 à máquina: ``ADICIONAR B12 2``
- Ver o saldo atual: `SALDO`

Exemplo de interação com esta máquina:
```
maq: 2025-03-09, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq:
┌──────┬──────────────────────────┬────────────┬───────┐
│ cod  │ nome                     │ quantidade │ preço │
├──────┼──────────────────────────┼────────────┼───────┤
│ A23  │ água 0.5L                │ 8          │ 0.7   │
├──────┼──────────────────────────┼────────────┼───────┤
│ B12  │ refrigerante 350mL       │ 0          │ 1.2   │
├──────┼──────────────────────────┼────────────┼───────┤
│ C45  │ barrinha de cereais      │ 10         │ 1.0   │
├──────┼──────────────────────────┼────────────┼───────┤
│ D67  │ sumo de laranja 1L       │ 3          │ 1.5   │
└──────┴──────────────────────────┴────────────┴───────┘
>> MOEDA 1e, 20c, 5c, 5c .
maq: Saldo = 1e30c
>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 60c
>> SELECIONAR A23
maq: Saldo insuficiente para satisfazer o seu pedido
maq: Saldo = 60c; Pedido = 70c
>> SELECIONAR B12
maq: O produto refrigerante 350mL está esgotado
>> MOEDA 10c, 2c, 2c .
maq: Saldo = 74c
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 20c e 2x 2c.
maq: Até à próxima
```
Mais exemplos:
```
maq: 2025-03-09, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> MOEDA 3c .
maq: Pedido inválido
>> ADICIONAR B12 3
maq: Adicionadas 3 quantidades do produto B12.
>> LISTAR
maq:
┌──────┬──────────────────────────┬────────────┬───────┐
│ cod  │ nome                     │ quantidade │ preço │
├──────┼──────────────────────────┼────────────┼───────┤
│ A23  │ água 0.5L                │ 7          │ 0.7   │
├──────┼──────────────────────────┼────────────┼───────┤
│ B12  │ refrigerante 350mL       │ 3          │ 1.2   │
├──────┼──────────────────────────┼────────────┼───────┤
│ C45  │ barrinha de cereais      │ 10         │ 1.0   │
├──────┼──────────────────────────┼────────────┼───────┤
│ D67  │ sumo de laranja 1L       │ 3          │ 1.5   │
└──────┴──────────────────────────┴────────────┴───────┘
>> SAIR
maq: Até à próxima
```

```
maq: 2025-03-09, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> NOVO A23 "KitKat" 2 1.9
maq: Um produto com código A23 já existe
>> NOVO E23 "KitKat" 2 1.9
maq: Produto E23 adicionado
>> LISTAR
maq:
┌──────┬──────────────────────────┬────────────┬───────┐
│ cod  │ nome                     │ quantidade │ preço │
├──────┼──────────────────────────┼────────────┼───────┤
│ A23  │ água 0.5L                │ 7          │ 0.7   │
├──────┼──────────────────────────┼────────────┼───────┤
│ B12  │ refrigerante 350mL       │ 3          │ 1.2   │
├──────┼──────────────────────────┼────────────┼───────┤
│ C45  │ barrinha de cereais      │ 10         │ 1.0   │
├──────┼──────────────────────────┼────────────┼───────┤
│ D67  │ sumo de laranja 1L       │ 3          │ 1.5   │
├──────┼──────────────────────────┼────────────┼───────┤
│ E23  │ KitKat                   │ 2          │ 1.9   │
└──────┴──────────────────────────┴────────────┴───────┘
>> SELECIONAR W11
maq: O produto W11 não existe
>> SALDO
maq: Saldo = 0c
>> SAIR
maq: Até à próxima
```
## Resultados
### Ficheiros resultantes deste trabalho
- O ficheiro inicial JSON que contém a lista com os nomes, quantidades e preços dos produtos (stock dos produtos): [stock.json](stock.json)
- O programa em Python que simula uma máquina de vending: [maq.py](maq.py)
- O manifesto que está a ler neste momento: [README.md](README.md)