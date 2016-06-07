from operacoes import *
from definicoes import *

class Automato(object):
    def __init__(self, qtdEstados, alfabeto = alfabeto()):
        self._trans = []
        self._tokens = []
        self._alfabeto = alfabeto
        for i in range(qtdEstados):
            self._tokens.append("")
            self._trans.append({'\n':i})

    def addTransicao(self, estado, caractere, proximoEstado):
        pass

    def setTokenEstado(self, estado, token):
        self._tokens[estado] = token

    def getTokenEstado(self, estado):
        return self._tokens[estado]

    def getAlfabeto(self):
        return self._alfabeto

    def getQtdEstados(self):
        return len(self._trans)

    def proximoEstado(self, estado, caractere):
        try:
            return self._trans[estado][caractere]
        except:
            return None 

class AFD(Automato):

    def __init__(self, qtdEstados, alfabeto = alfabeto()):
        super(AFD, self).__init__(qtdEstados, alfabeto)

    def addTransicao(self, estado, caracteres, proximoEstado):
        for c in caracteres:
            self._trans[estado][c] = proximoEstado

class AFN(Automato):

    def __init__(self, qtdEstados, alfabeto = alfabeto()):
        super(AFN, self).__init__(qtdEstados, alfabeto)

    def addTransicao(self, estado, caracteres, proximoEstado):
        try:
            for c in caracteres:
                self._trans[estado][c].append(proximoEstado)
        except:
            for c in caracteres:
                self._trans[estado][c] = []
                self._trans[estado][c].append(proximoEstado)

    def edge(self, estado, caractere):
        try:
            return self._trans[estado][caractere]
        except:
            return []

    def closure(self, estados):
        T = estados
        while True:
            T2 = T
            u = []
            for s in T2:
                u = uniao(u, self.edge(s, '?'))

            T = uniao(T2, u)
            if T == T2:
                break
        return u

    def DFAedge(self, estados, caractere):
        u = []
        for s in estados:
            u = uniao(u, self.edge(s, caractere))
            print u
        return self.closure(u)

    def toAFD(self):
        afd = AFD(self.getQtdEstados()*(self.getQtdEstados()-1))
        estados = []
        estados.append([])
        estados.append(self.closure([0]))
        p = 1
        j = 0
        while j <= p:
            for c in self.getAlfabeto():
                e = self.DFAedge(estados[j], c)
                i = 0
                while i <= p:
                    if e == estados[i]:
                        afd.addTransicao(j, [c], i)
                        afd.setTokenEstado(j, str(estados[i]))
                    else:
                        p += 1
                        estados[p] = e
                        afd.addTransicao(j, [c], p)
                    i += 1
            j += 1
        return afd

#Faz a analise lexica de uma linha de codigo (tirei da classe AFD, reduzi as gambiarras!)
def analisadorLexico(afd, linha):
    tokens = []
    estadoAtual = 0
    palavra = ""
    tokenAtual = None
    c = 0
    while c < len(linha):
        tokenAtual = afd.getTokenEstado(estadoAtual)
        if linha[c] == " " and afd.proximoEstado(estadoAtual, linha[c]) == None:
            if tokenAtual == "ID":
                tokenAtual += "("+palavra+")"
            elif tokenAtual == "BINOP":
                tokenAtual += "("+palavra+")"    
            if tokenAtual != '':
                tokens.append(tokenAtual)
            estadoAtual = 0
            palavra = ""

        elif afd.proximoEstado(estadoAtual, linha[c]) == None:
            if tokenAtual == "ID":
                tokenAtual += "("+palavra+")"
            elif tokenAtual == "BINOP":
                tokenAtual += "("+palavra+")"
            if tokenAtual != '':    
                tokens.append(tokenAtual)
            estadoAtual = 0
            palavra = ""
            c -= 1

        elif afd.getTokenEstado(afd.proximoEstado(estadoAtual, linha[c])) == "ERRO":
            palavra += linha[c]
            raise Exception("ERRO: '" + palavra + "'")

        else:
            palavra += linha[c]
            estadoAtual = afd.proximoEstado(estadoAtual, linha[c])
            tokenAtual = afd.getTokenEstado(estadoAtual)
            if c == (len(linha) - 1):
                if tokenAtual == "ID":
                    tokenAtual += "("+palavra+")"
                elif tokenAtual == "BINOP":
                    tokenAtual += "("+palavra+")"
                if tokenAtual != '':
                    tokens.append(tokenAtual)

        c += 1
    return tokens
