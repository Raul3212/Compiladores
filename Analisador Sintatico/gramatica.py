from copy import copy

def getStringFromList(list):
    result = ""
    for s in list:
        result += (" " + s.strip())
    return result[1:]

class GLC:
    def __init__(self):
        self.__terminais = []
        self.__nterminais = []
        self.__regras = []
        self.__nullables = set([])

    def setTerminais(self, terminais):
        self.__terminais = terminais

    def setNTerminais(self, nterminais):
        self.__nterminais = nterminais

    def setNullables(self, nullables):
        self.__nullables = set(nullables)
    
    def getTerminais(self):
        return self.__terminais

    def getNTerminais(self):
        return self.__nterminais

    def getSymbols(self):
        return self.getNTerminais() + self.getTerminais()
    
    def getRegra(self, id):
        return self.__regras[id]
        
    def addRegra(self, (nt, r)):
        self.__regras.append((nt, r))

    def getGeracoes(self, nterminal):
        regras = []
        for (nt, r) in self.__regras:
            if nt == nterminal:
                regras.append(r)
        return regras

    def getNullables(self):
        return self.__nullables
                
    def getFirst(self, regra):
        Y = regra.split()
        first = set([])
        for y in Y:
            first = first.union(self.__getFirst(y))
            if y not in self.getNullables():
                break
        return first
             
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
                partes = prod.split('.')
                X = partes[1].strip().split()
                if X != []:
                    if X[0] in self.getNTerminais():
                        for y in self.getGeracoes(X[0]):
                            for w in self.getFirst(getStringFromList(X[1:]).strip()+' '+z):
                                if w == '':
                                    w = '$'
                                I = I.union(set([(X[0], '.'+y.strip(), w)])) 
            if I2 == I:
                break
        return I

    def goTo(self, I, C):
        J = set([])
        for (A, prod, z) in I:
            partes = prod.split('.')
            X = partes[1].strip().split()
            if X != []:
                if X[0] == C:
                    J.add((A, partes[0].strip() +' '+ X[0].strip() + '.' + getStringFromList(X[1:]).strip(), z))
        return self.closure(J)

    def items(self):
        T = []
        (S_, prod) = self.__regras[0]
        T.append(self.closure(set([(S_, '.'+prod.strip(), '$')])))
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
        table = []
        C = self.items()
        
        #inicializando a tabela
        for i in range(len(C)):
            table.append({})
            for x in self.getSymbols():
                table[i][x] = '-1'
            
        for I in C:
            i = C.index(I)
            for (A, prod, z) in I:
                Y = prod.split('.')
                B = Y[1].strip().split()
                if B != []:
                    if B[0] in self.getTerminais() and self.goTo(I, B[0]) in C:
                        j = C.index(self.goTo(I, B[0]))
                        table[i][B[0]] = 's_'+str(j)
                  
                elif B == [] and A != 'S_':
                    indexRegra = self.__regras.index((A, Y[0].strip()))
                    table[i][z] = 'r_'+str(indexRegra)
                
                elif B == [] and A == 'S_':
                    table[i]['$'] = 'ok'
                
                g = self.goTo(I, A)
                if g in C:
                    j = C.index(g)
                    table[i][A] = 'g_'+str(j)            
            
        return table    