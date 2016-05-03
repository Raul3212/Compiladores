from copy import copy
from gramatica import *

class Automato(object):
    def __init__(self, qtdEstados):
        self._trans = []
        self._tokens = []
        for i in range(qtdEstados):
            self._trans.append({'\n':i})
            self._tokens.append("")

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

class AF_LR1(Automato):

    def __init__(self, qtdEstados, glc = None):
        super(AF_LR1, self).__init__(qtdEstados)
        self.__glc = glc
        self.__itens = []
        self.__finais = []
        for i in range(qtdEstados):
            self.__itens.append({})
            self.__finais.append(False)

    def addTransicao(self, estado, c, proximoEstado):
        self._trans[estado][c] = proximoEstado

    def addItem(self, estado, gerador, gerado, lkh):
        try:
            self.__itens[estado][gerador].append((gerado, lkh))
        except:
            self.__itens[estado][gerador] = []
            self.__itens[estado][gerador].append((gerado, lkh))

    def setAsFinal(self, estado):
        self.__finais[estado] = True

    def ehFinal(self, estado):
        return self.__finais[estado] == True

    def closure(self, I):
        while True:
            I2 = copy(I)
            for i in range(len(I)):
                for A in I[i]:
                    for (prod, lkh) in I[i][A]:
                        P = prod.split()
                        j = 0
                        while j < len(P):
                            if P[j] == '.' and P[j+1] in self.__glc.getNTerminais():
                                X = P[j+1]
                                for (prod2, lkh2) in I[i][X]:
                                    Y = prod2.split()
                                    for w in self.__glc.getSet(Y[1], "FIRST"):
                                        if '.' not in Y:
                                            try:
                                                I[i][X].append((". " + prod2, w))
                                            except:
                                                I[i][X] = []
                                                I[i][X].append((". " + prod2, w))
                            j+=1
            if I2 == I:
                break
        return I

    def goTo(self, I, X):
        J = []
        for i in range(len(I)):
            J.append({})
            for (prod, lkh) in I[i][X]:
                try:
                    J[i][X].append((prod, lkh))
                except:
                    J[i][X] = []
                    J[i][X].append((prod, lkh))
        return self.closure(J)

glc = GLC([";", "id", ":=", "print", "(", ")", "num", "+", ","])
glc.addRegra("S", "S ; S")
glc.addRegra("S", "id := E")
glc.addRegra("S", "print ( L )")
glc.addRegra("E", "id")
glc.addRegra("E", "num")
glc.addRegra("E", "E + E")
glc.addRegra("E", "( S , E )")
glc.addRegra("L", "E")
glc.addRegra("L", "L , E")

af = AF_LR1(100, glc)

print af.goTo([{'S':[('S ; S', '$'), ('id := E', '$')], 'E':[('num', '$'), ('id', '$')]}], 'E')
