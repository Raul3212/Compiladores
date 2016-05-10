import sys
from gramatica import *

def analisadorSintatico(glc, tokens):
    estados = glc.items()
    tabela = glc.analisysTable()
    pilha = []
    estadoAtual = 0
    listaTokens = tokens.split()
    for t in listaTokens:
        acao = tabela[estadoAtual][t]
        partes = acao.split('_')
        if acao == "-1":
            print "Erro sintatico -> " + t 
            break

        elif partes[0] == 's':
            pilha.append(t)
            estadoAtual = int(partes[1])
            
        elif partes[0] == 'r':
            (X, prod) = glc.getRegra(int(partes[1]))
            for p in str(prod):
                pilha.pop()
            pilha.append(X)
            estadoAtual = int(tabela[estadoAtual][X])
            
        elif partes[0] == 'g':
            estadoAtual = C.index(C[partes[1]])
            
        elif partes == "ok":
            print "Sucesso"    


glc = GLC()

glc.setTerminais([";", "+", "id", ":=", "print", "(", ")", "num", ",", "$"])
glc.setNTerminais(["S", "E", "L"])

glc.addRegra(("S_", "S $"))
glc.addRegra(("S", "S ; S"))
glc.addRegra(("S", "id := E"))
glc.addRegra(("S", "print ( L )"))
glc.addRegra(("E", "id"))
glc.addRegra(("E", "num"))
glc.addRegra(("E", "E + E"))
glc.addRegra(("E", "( S , E )"))
glc.addRegra(("L", "E"))
glc.addRegra(("L", "L , E"))

C = glc.analisysTable()
print len(C)

for l in sys.stdin:
    print analisadorSintatico(glc, l)
