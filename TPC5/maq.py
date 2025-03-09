import json
from datetime import datetime
import re

def calctroco(saldo):
    valores = [2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    troco = {}
    saldo = round(saldo,2)
    for valor in valores:
        troco[valor] = int(saldo // valor)
        saldo = round(saldo % valor,2)
    return troco

with open('stock.json', 'r', encoding="utf-8") as f:
    conteudo_json = json.load(f)

stock = conteudo_json["stock"]

print("maq: " + datetime.now().strftime("%Y-%m-%d") + ", Stock carregado, Estado atualizado.")
print("maq: Bom dia. Estou disponível para atender o seu pedido.")
saldo = 0
while True:
    resposta = input(">> ")
    if resposta == "SAIR":
        if saldo != 0:
            print("maq: Pode retirar o troco: ", end="")
            troco = calctroco(saldo)
            l = []
            for key in troco.keys():
                if troco[key] > 0:
                    if key == 1 or key == 2:
                        t = str(key) + "e"
                    else:
                        t = str(int(key * 100)) + "c"
                    l.append(str(troco[key]) + "x " + t)
            for i in range(0,len(l)):
                if i == len(l)-2:
                    print(l[i] + " e ",end="")
                elif i == len(l)-1:
                    print(l[i]+".")
                else:
                    print(l[i] + ", ",end="")
        print("maq: Até à próxima")
        l = {}
        l['stock'] = stock
        with open('stock.json', 'w', encoding="utf-8") as f:
            json.dump(l,f,ensure_ascii=False,indent=4)
        break
    elif resposta == "SALDO":
        saldo_parte = "{:.2f}".format(float(saldo)).split(".")
        euros = saldo_parte[0]+"e" if saldo_parte[0]!="0" else ""
        centimos = (saldo_parte[1][1] if saldo_parte[1][0] == "0" else saldo_parte[1])+"c" if saldo_parte[1]!="00" else ""
        if (euros == "" and centimos == ""):
            centimos = "0c"
        print("maq: Saldo = " + euros + centimos)
    elif resposta == "LISTAR":
        if stock:
            print("maq:")
            print("┌──────┬──────────────────────────┬────────────┬───────┐")
            print("│ cod  │ nome                     │ quantidade │ preço │")
            for produto in stock:
                print("├──────┼──────────────────────────┼────────────┼───────┤")
                print(f"│ {produto['cod']:<4} │ {produto['nome']:<24} │ {produto['quant']:<10} │ {produto['preco']:<5} │")
            print("└──────┴──────────────────────────┴────────────┴───────┘")
        else:
            print("maq: Stock vazio")
    elif (produto := re.fullmatch(r"SELECIONAR ([^\W_\d](?:\d){2})",resposta)):
        existe = False
        cod = produto.group(1)
        for produto in stock:
            if produto['cod'] == cod:
                existe = True
                if produto['quant'] == 0:
                    print(f"maq: O produto {produto['nome']} está esgotado")
                else:
                    if saldo >= produto['preco']:
                        print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
                        saldo -= produto['preco']
                        produto['quant']-=1
                        saldo_parte = "{:.2f}".format(float(saldo)).split(".")
                        euros = saldo_parte[0]+"e" if saldo_parte[0]!="0" else ""
                        centimos = (saldo_parte[1][1] if saldo_parte[1][0] == "0" else saldo_parte[1])+"c" if saldo_parte[1]!="00" else ""
                        if (euros == "" and centimos == ""):
                            centimos = "0c"
                        print("maq: Saldo = " + euros + centimos)
                    else:
                        print("maq: Saldo insuficiente para satisfazer o seu pedido")
                        saldo_parte = "{:.2f}".format(float(saldo)).split(".")
                        euros = saldo_parte[0]+"e" if saldo_parte[0]!="0" else ""
                        centimos = (saldo_parte[1][1] if saldo_parte[1][0] == "0" else saldo_parte[1])+"c" if saldo_parte[1]!="00" else ""
                        if (euros == "" and centimos == ""):
                            centimos = "0c"
                        pedido_parte = "{:.2f}".format(float(produto['preco'])).split(".")
                        peuros = pedido_parte[0]+"e" if pedido_parte[0]!="0" else ""
                        pcentimos = (pedido_parte[1][1] if pedido_parte[1][0] == "0" else pedido_parte[1])+"c" if pedido_parte[1]!="00" else ""
                        if (peuros == "" and pcentimos == ""):
                            pcentimos = "0c"
                        print("maq: Saldo = " + euros + centimos + "; Pedido = " + peuros + pcentimos)
                break
        if not existe:
            print(f"maq: O produto {cod} não existe")
    elif (moedas := re.fullmatch(r"MOEDA ((?:(?:1c|2c|5c|10c|20c|50c|1e|2e), )*(?:1c|2c|5c|10c|20c|50c|1e|2e)) .",resposta)):
        moedas = moedas.group(1).split(", ")
        for moeda in moedas:
            if (valor := re.fullmatch(r"(\d)e",moeda)):
                valor = int(valor.group(1))
                saldo += valor
            elif (valor := re.fullmatch(r"(\d+)c",moeda)):
                valor = int(valor.group(1))/100
                saldo += valor
        saldo_parte = "{:.2f}".format(float(saldo)).split(".")
        euros = saldo_parte[0]+"e" if saldo_parte[0]!="0" else ""
        centimos = (saldo_parte[1][1] if saldo_parte[1][0] == "0" else saldo_parte[1])+"c" if saldo_parte[1]!="00" else ""
        if (euros == "" and centimos == ""):
            centimos = "0c"
        print("maq: Saldo = " + euros + centimos)
    elif (add := re.fullmatch(r"NOVO ([^\W_\d](?:\d){2}) \"(.+)\" (\d+) (\d+(?:\.\d{1,2})?)",resposta)):
        existe = False
        cod = add.group(1)
        for produto in stock:
            if produto['cod'] == cod:
                existe = True
                print(f"maq: Um produto com código {cod} já existe")
                break
        if not existe:
            p = {}
            p['cod'] = cod
            p['nome'] = add.group(2)
            p['quant'] = add.group(3)
            p['preco'] = add.group(4)
            stock.append(p)
            print(f'maq: Produto {cod} adicionado')
    elif (add := re.fullmatch(r"ADICIONAR ([^\W_\d](?:\d){2}) (\d+)",resposta)):
        existe = False
        cod = add.group(1)
        for produto in stock:
            if produto['cod'] == cod:
                existe = True
                produto['quant'] += int(add.group(2))
                print(f"maq: Adicionadas {int(add.group(2))} quantidades do produto {cod}.")
                break
        if not existe:
            print(f"maq: O produto {cod} não existe")
    else:
        print("maq: Pedido inválido")