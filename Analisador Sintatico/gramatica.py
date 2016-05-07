from copy import copy

def areAllNullable(lista, nullables):
    for i in lista:
        if not nullables[i] == False:
            return False
    return True

def getStringFromList(list):
    result = ""
    for s in list:
        result += (" " + s)
    return result[1:]

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
        if nt not in self.__nterminais:
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

    def getSymbols(self):
        return self.getNTerminais() + self.getTerminais()
    
    def __getInitSymbol(self):
        return self.__nterminais[0]
    
    def getNullables(self):
        return self.__nullables
                
    def getFirst(self, regra):
        Y = regra.split()
        if Y[0] not in self.getNullables() or len(Y) == 1:
            return self.__getFirst(Y[0])
        else:
            return self.__getFirst(Y[0]).union(self.getFirst(Y[1]))

    def __getFirst(self, simbolo):
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

    def closure(self, I):
        while True:
            I2 = copy(I)
            for (A, prod, z) in I:
                S = prod.split()
                for s in range(len(S)-1):
                    if S[s] == '.' and S[s+1] in self.getNTerminais():
                        for y in self.getGeracoes(S[s+1]):
                            if s < len(S) - 2:
                                for w in self.getFirst(S[s+2]+" "+z):
                                    if w == '':
                                        w = '$'
                                    I = I.union(set([(S[s+1], ". " + y, w)]))
                            else:
                                I = I.union(set([(S[s+1], ". " + y, '$')]))
            if I2 == I:
                break
        return I

    def goTo(self, I, X):
        J = set([])
        for (A, prod, z) in I:
            S = prod.split()
            for s in range(len(S)-1):
                if S[s] == '.' and S[s+1] == X:
                    if z == '':
                        z = '$'
                    J.add((A, getStringFromList(S[0:s]) + " " + X + ' . ' + getStringFromList(S[s+2:]), z))
        return self.closure(J)

    def items(self):
        initSymbol = self.__getInitSymbol()
        T = []
        T.append(self.closure(set([('S_', '. '+initSymbol, '$')])))
        while True:
            T2 = copy(T)
            for I in T:
                for X in self.getSymbols():
                    aux = self.goTo(I, X)
                    if aux not in T and aux != set([]):
                        T.append(aux)
            if T2 == T:
                break
        return T
    
    def analisysTable(self):
        initSymbol = self.__getInitSymbol()
        table = []
        C = self.items()
        print C
        #inicializando a tabela
        for i in range(len(C)):
            table.append({})
            
        for I in C:
            i = C.index(I)
            if ('S_', ' S . ', '$') in I:
                table[i]['$'] = 'ok'
            
            for (A, prod, z) in I:
                Y = prod.split()
                y = 0
                while y < len(Y):
                    if y < len(Y)-1:
                        if Y[y] == '.' and Y[y+1] in self.getTerminais():
                            g = self.goTo(I, Y[y+1])
                            if g in C:
                                j = C.index(g)
                                table[i][Y[y+1]] = 's_'+str(j)
                    y+=1
                if Y[len(Y) - 1] == '.' and A != 'S_':
                    table[i][z] = 'r_'+A+'_'+Y[len(Y) - 2]
                
                g = self.goTo(I, A)
                if g in C:
                    j = C.index(g)
                    table[i][A] = j            
        return table                
                
"""glc = GLC([";", "id", ":=", "print", "(", ")", "num", "+", ",", "a"])
glc.addRegra(("S", "S ; S"))
glc.addRegra(("S", "id := E"))
glc.addRegra(("S", "print ( L )"))
glc.addRegra(("E", "id"))
glc.addRegra(("E", "num"))
glc.addRegra(("E", "E + E"))
glc.addRegra(("E", "( S , E )"))
glc.addRegra(("L", "E"))
glc.addRegra(("L", "L , E"))"""

"""glc = GLC(["+", "*", "(", ")", "id"])
glc.addRegra(("E", "E + T"))
glc.addRegra(("E", "T"))
glc.addRegra(("T", "T * F"))
glc.addRegra(("T", "F"))
glc.addRegra(("F", "( E )"))
glc.addRegra(("F", "id"))"""

glc = GLC(['c', 'd'])
glc.addRegra(('S', 'C C'))
glc.addRegra(('C', 'c C'))
glc.addRegra(('C', 'd'))

#Y = set([('S', 'E .', ''), ('E', 'E . + T', '')])
#print glc.goTo(Y, '+')
for c in glc.analisysTable():
    print str(c) + '\n'