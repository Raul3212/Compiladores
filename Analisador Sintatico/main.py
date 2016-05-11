import sys
from gramatica import *

def analisadorSintatico(glc, tokens):
    estados = glc.items()
    tabela = glc.analisysTable()
    
    estadoStack = [0]
    listaTokens = tokens.split()
    
    t = 0
    while t < len(listaTokens):
        
        acao = tabela[estadoStack[-1]][listaTokens[t]]
        partes = acao.split('_')
        if acao == "ok":
            print "Sucesso"
            break
        
        elif acao == "-1":
            print "Erro sintatico" 
            break

        elif partes[0] == 's':
            estadoStack.append(int(partes[1]))
            
        elif partes[0] == 'r':
            (X, prod) = glc.getRegra(int(partes[1]))
            for _ in prod.split():
                estadoStack.pop()
            aux = tabela[estadoStack[-1]][X]
            if aux != "-1":
                aux = aux.split('_')
                estadoStack.append(int(aux[1]))
                t -= 1
                
        elif partes[0] == 'g':
            estadoStack.append(int(partes[1]))
        
        t+=1

glc = GLC()

glc.setTerminais([";", "+", "id", ":=", "print", "(", ")", "num", ",", "$"])
glc.setNTerminais(["S", "E", "L"])

glc.addRegra(("S_", "S"))
glc.addRegra(("S", "S ; S"))
glc.addRegra(("S", "id := E"))
glc.addRegra(("S", "print ( L )"))
glc.addRegra(("E", "id"))
glc.addRegra(("E", "num"))
glc.addRegra(("E", "E + E"))
glc.addRegra(("E", "( S , E )"))
glc.addRegra(("L", "E"))
glc.addRegra(("L", "L , E"))

l = raw_input()
analisadorSintatico(glc, l+' $')
