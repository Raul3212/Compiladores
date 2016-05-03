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

    def addRegra(self, (nt, r)):
        self.__regras.append((nt, r))
        self.__nterminais.append(nt)

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

    def getFirst(self, simbolo):
        if simbolo in self.getTerminais():
            return set([simbolo])
        first = set([])
        for prod in self.getGeracoes(simbolo):
            Y = prod.split()
            if Y[0] in self.getTerminais():
                first.add(Y[0])
            elif Y[0] in self.getNTerminais() and not Y[0] == simbolo:
                first = first.union(self.getFirst(Y[0]))
        return first

    def getFollow(self, simbolo):
        follow = set([])
        for (_ , prod) in self.__regras:
            Y = prod.split()
            k = len(Y)
            for i in range(k):
                if Y[i] == simbolo:
                    if i < k-1:
                        # if Y[i+1] not in self.getNullables():
                        follow = follow.union(self.getFirst(Y[i+1]))
        return follow

glc = GLC([";", "id", ":=", "print", "(", ")", "num", "+", ","])
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
