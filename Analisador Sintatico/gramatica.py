from copy import copy

def areAllNullable(lista, nullables):
    for i in lista:
        if not nullables[i] == False:
            return False
    return True

class GLC:
    def __init__(self, terminais):
        self.__terminais = terminais
        self.__nterminais = []
        self.__regras = {}

    def addRegra(self, gerador, gerado):
        if gerador not in self.__nterminais:
            self.__nterminais.append(gerador)
        try:
            self.__regras[gerador].append(gerado)
        except:
            self.__regras[gerador] = []
            self.__regras[gerador].append(gerado)

    def getGeracoes(self, gerador):
        try:
            return self.__regras[gerador]
        except:
            return None

    def getFiFoN(self):
        fi = {}
        fo = {}
        nullables = {}

        #Inicializacao
        for nt in self.__nterminais:
            fi[nt] = set([])
            fo[nt] = set([])
            nullables[nt] = False
        for t in self.__terminais:
            fi[t] = set([t])
            fo[t] = set([])
            nullables[t] = False

        while True:
            fi2 = copy(fi)
            fo2 = copy(fo)
            nullables2 = copy(nullables)
            for X in self.__regras:
                for g in self.__regras[X]:
                    Y = g.split()
                    k = len(Y)
                    if (Y in self.__nterminais and areAllNullable(Y, nullables)) or k == 0:
                        nullables[X] = True
                    for i in range(k):
                        j = i+1
                        while j < k:
                            if areAllNullable(Y[0:i], nullables):
                                fi[X] = fi[X].union(fi[Y[i]])
                            if areAllNullable(Y[i+1:k], nullables):
                                fo[Y[i]] = fo[Y[i]].union(fo[X])
                            if areAllNullable(Y[i+1:j], nullables):
                                fo[Y[i]] = fo[Y[i]].union(fi[Y[j]])
                            j += 1
            if (fo == fo2) and (fi == fi2) and (nullables == nullables2):
                break
        return (fi, fo, nullables)

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

# (fi, fo, null) = glc.getFiFoN()
# print fi["S"]
# print fi["E"]
# print fi["L"]
# print null
