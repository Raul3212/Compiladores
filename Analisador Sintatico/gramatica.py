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
        self.__regras = []
        self.__nullables = set([])

    def __findNullables(self):
        for (S, P) in self.__regras:
            if P == "" or P in self.__nullables:
                self.__nullables.add(S)

    def addRegra(self, (nt, r)):
        self.__regras.append((nt, r))
        self.__nterminais.append(nt)
        self.__findNullables()

    def getGeracoes(self, nterminal):
        regras = []
        for (nt, r) in self.__regras:
            if nt == nterminal:
                regras.append(r)
        return regras

    def getTerminais(self):
        return self.__terminais

    def getNTerminais(self):
        return self.__nterminais

    def getNullables(self):
        return self.__nullables

    def getFirst(self, simbolo):
        if simbolo in self.getTerminais():
            return set([simbolo])
        first = set([])
        for prod in self.getGeracoes(simbolo):
            if prod != "":
                Y = prod.split()
                k = len(Y)
                if Y[0] in self.getTerminais():
                    first.add(Y[0])
                else:
                    if not Y[0] == simbolo:
                        first = first.union(self.getFirst(Y[0]))
                    if Y[0] in self.getNullables():
                        i = 1
                        while i < k:
                            first = first.union(self.getFirst(Y[i]))
                            if Y[i] not in self.getNullables():
                                break
                            i+=1

        return first

    def getFollow(self, simbolo):
        follow = set([])
        for (_ , prod) in self.__regras:
            Y = prod.split()
            k = len(Y)
            for i in range(k):
                if Y[i] == simbolo and i < k-1:
                    follow = follow.union(self.getFirst(Y[i+1]))
                    if Y[i+1] in self.getNullables():
                        j = i+2
                        while j < k:
                            follow = follow.union(self.getFirst(Y[j]))
                            if Y[j] not in self.getNullables():
                                break
                            j+=1
        return follow

glc = GLC([";", "id", ":=", "print", "(", ")", "num", "+", ",", "a"])
glc.addRegra(("S", "S ; S"))
glc.addRegra(("S", "id := E"))
glc.addRegra(("S", "print ( L )"))
glc.addRegra(("E", "id"))
glc.addRegra(("E", "num"))
glc.addRegra(("E", "E + E"))
glc.addRegra(("E", "( S , E )"))
glc.addRegra(("L", "E"))
glc.addRegra(("L", "L , E"))

print glc.getFollow('S')

# print fi['L']
