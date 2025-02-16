import re

with open("obras.csv","r",encoding = "utf-8") as file:
    conteudo = file.read()

lista = []
i = 0
for line in re.split(r"\n(?=\S)",conteudo):
    obra = re.split(r";",line)
    if (len(obra) > 7):
        obra_corrigida = []
        obra_corrigida.append(obra[0])
        i = 2
        l = len(obra)
        while (l > 7):
            obra[1] = obra[1] + obra[i]
            i += 1
            l -= 1
        obra_corrigida.append(obra[1])
        while i < len(obra):
            obra_corrigida.append(obra[i])
            i += 1
        lista.append(obra_corrigida)
    else:
        lista.append(obra)

lista.pop(0)

set_compositores = set()

for obra in lista:
    compositor = obra[4]
    set_compositores.add(compositor)
    
list_compositores = list(set_compositores)
list_compositores.sort()

print("Lista ordenada alfabeticamente dos compositores musicais:")
print(list_compositores)

map_periodo_numero = {}
map_periodo_obras = {}
for obra in lista:
    titulo = obra[0]
    periodo = obra[3]
    if periodo in map_periodo_numero.keys():
        map_periodo_numero[periodo] += 1
        map_periodo_obras[periodo].append(titulo)
    else:
        map_periodo_numero[periodo] = 1
        map_periodo_obras[periodo] = []
        map_periodo_obras[periodo].append(titulo)
        
print("\nDistribuição das obras por período -> quantas obras catalogadas em cada período:")
print(map_periodo_numero)

for obras in map_periodo_obras.values():
    obras.sort()

print("\nDicionário em que a cada período está a associada uma lista alfabética dos títulos das obras desse período:")
print(map_periodo_obras)