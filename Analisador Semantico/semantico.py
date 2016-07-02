#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

tipos = ['STRING', 'INT']
valores = ['STR', 'NUM']

#Controi tabelas de variaveis e funcoes
#Detecta ambiguidade de nomes
def extrairIDs(tokens):
    variaveis = []
    funcoes = []
    escopo = "1"
    contEscopo = 0
    idEscopo = 0
    for i in range(len(tokens)):
        if tokens[i] == 'SEMI':
            idEscopo += 1
        if tokens[i] == 'LKEY':
            escopo += str(contEscopo)
        elif tokens[i] == 'RKEY':
            escopo = escopo[0:len(escopo)-1]
            contEscopo += 1
        
        #Caso de ser variável    
        if (tokens[i] in tipos) and tokens[i+1][:2] == 'ID' and tokens[i+2] != 'LPAREN' and tokens[i-1] != 'LPAREN' and tokens[i-1] != 'COMMA':
            if existeDefinicaoIDNoEscopo(variaveis, funcoes, tokens[i+1][3:-1], escopo, idEscopo):
                print "Variavel '"+ tokens[i+1][3:-1] +"' causa ambiguidade."
                return ([], [])
            variaveis.append((tokens[i], tokens[i+1][3:-1], escopo, idEscopo))  
        
        #Caso encontre uma função
        elif (tokens[i] in tipos) and tokens[i+1][:2] == 'ID' and tokens[i+2] == 'LPAREN':
            #Verifica existencia de parâmetro 1
            if tokens[i+3] in tipos:
                variaveis.append((tokens[i+3], tokens[i+4][3:-1], escopo+str(contEscopo), idEscopo))
                
                #Verifica existência de parâmetro 2
                if tokens[i+5] == 'COMMA':
                    variaveis.append((tokens[i+6], tokens[i+7][3:-1], escopo+str(contEscopo), idEscopo))
                    
                    if existeDefinicaoIDNoEscopo(variaveis, funcoes, tokens[i+1][3:-1], escopo, idEscopo):
                        print "Funcao '"+ tokens[i+1][3:-1] +"("+ tokens[i+3] +", "+ tokens[i+6] +")' causa ambiguidade."
                        return ([], [])
                    #Adiciona funcao com 2 parâmetros
                    funcoes.append((tokens[i], tokens[i+1][3:-1], tokens[i+3], tokens[i+6], escopo, idEscopo))
                else:
                    if existeDefinicaoIDNoEscopo(variaveis, funcoes, tokens[i+1][3:-1], escopo, idEscopo):
                        print "Funcao '"+ tokens[i+1][3:-1] +"("+ tokens[i+3] +")' causa ambiguidade."
                        return ([], [])
                    #Adiciona funcao com 1 parâmetro
                    funcoes.append((tokens[i], tokens[i+1][3:-1], tokens[i+3], None, escopo, idEscopo))
            else:
                if existeDefinicaoIDNoEscopo(variaveis, funcoes, tokens[i+1][3:-1], escopo, idEscopo):
                    print "Funcao '"+ tokens[i+1][3:-1] +"()' causa ambiguidade."
                    return ([], [])
                #Adiciona funcao sem parâmetros
                funcoes.append((tokens[i], tokens[i+1][3:-1], None, None, escopo, idEscopo))
                    
    return (variaveis, funcoes)            

def pegarVariaveisDisponiveis(variaveis, nome, escopo, idEscopo):
    vs = []
    for (t, v, s, ids) in variaveis:
        if ((len(s) < len(escopo) and s[0:len(s)] == escopo[0:len(s)]) or (len(s) == len(escopo) and int(s) == int(escopo) and ids < idEscopo)) and v == nome:
            vs.append((t, v))
    return vs    

def existeDefinicaoID(variaveis, funcoes, nome, escopo, idEscopo):
    for (t, n, s, ids) in variaveis:
        if (len(s) < len(escopo) or (int(s) == int(escopo) and ids <= idEscopo)) and n == nome:
            return True
            
    for (t, f, p1, p2, s, ids) in funcoes:
        if (len(s) < len(escopo) or (int(s) == int(escopo) and ids <= idEscopo)) and f == nome:
            return True
    
    return False

def existeDefinicaoIDNoEscopo(variaveis, funcoes, nome, escopo, idEscopo):
    for (t, n, s, ids) in variaveis:
        if (int(s) == int(escopo) and ids <= idEscopo) and n == nome:
            return True
            
    for (t, f, p1, p2, s, ids) in funcoes:
        if (int(s) == int(escopo) and ids <= idEscopo) and f == nome:
            return True
    
    return False        

def pegarFuncoesDisponiveis(funcoes, nome, tp1, tp2, escopo, idEscopo):
    fs = []
    for (t, f, p1, p2, s, ids) in funcoes:
        if (s < escopo or (s == escopo and ids < idEscopo)) and f == nome and p1 == tp1 and p2 == tp2:
            fs.append((t, f))
    return fs
    
#Retorna o tipo de uma variável            
def pegarTipoVariavel(variaveis, nome, escopo, idEscopo):
    aux = copy(variaveis)
    aux.reverse()
    for (t, v, s, ids) in aux:
        if (len(s) < len(escopo) or (int(s) == int(escopo) and ids <= idEscopo)) and v == nome: 
            return t
    return None
    
def pegarTipoFuncao(funcoes, nome, escopo, idEscopo):
    aux = copy(funcoes)
    aux.reverse()
    for (t, f, p1, p2, s, ids) in aux:
        if (len(s) < len(escopo) or (int(s) == int(escopo) and ids <= idEscopo)) and f == nome:
            return t
    return None

def removerParametros(tokens):
    escopo = 0
    i = 0
    while True:
        
        if tokens[i] == 'LPAREN':
            escopo += 1
        elif tokens[i] == 'RPAREN':
            escopo -= 1
            if escopo == 0:
                break

        del tokens[i]      
 
    return tokens

#Dada uma expressão (tokens) que vai até o tokenParada, retorna o tipo dessa expressão
#Se o tipo for inválido retorna a string 'NULL' 
def pegarTipoExpressao(tokens, variaveis, funcoes, escopo, idEscopo, tokenParada = 'SEMI'):
    tipo = "NULL"
    t = 0
    while t < (len(tokens)):
        if tokens[t] == 'STR':
            if tipo == "INT":
                return "NULL"
            tipo = "STRING"
        
        elif tokens[t] == 'NUM':
            if tipo == "STRING":
                return "NULL"
            tipo = "INT"
        
        elif tokens[t][:2] == 'ID':
            tipoAux = pegarTipoVariavel(variaveis, tokens[t][3:-1], escopo, idEscopo)
            if tipoAux == None:
                tipoAux = pegarTipoFuncao(funcoes, tokens[t][3:-1], escopo, idEscopo)
                if tipoAux == None:
                    return "NULL"
                else:
                    tokens = removerParametros(tokens[t:]) #remove os tokens que sao parametros da chamada a funcao
                    t = 0
                    tipo = tipoAux
            else:
                tipo = tipoAux
        elif tokens[t][:5] == "BINOP" and tokens[t][6] != '+' and tipo == "STRING":
            return "NULL"       
                
        elif tokens[t] == tokenParada:
            break
        t += 1       
    
    return tipo

#Analisa o uso de variaveis
def verificarUsoVariaveis(tokens, variaveis):
    escopo = "1"
    contEscopo = 0
    idEscopo = 0
    for i in range(len(tokens)):
        if tokens[i] == 'SEMI':
            idEscopo += 1
        if tokens[i] == 'LKEY':
            escopo += str(contEscopo)
        elif tokens[i] == 'RKEY':
            escopo = escopo[0:len(escopo)-1]
            contEscopo += 1
            
        if tokens[i][:2] == 'ID' and tokens[i-1] not in tipos and tokens[i+1] != 'LPAREN':
            if not existeDefinicaoID(variaveis, [], tokens[i][3:-1], escopo, idEscopo):
                print "Variavel '" + tokens[i][3:-1] + "' nao esta definida neste local."
                return False
    return True        

#Analisa o uso de funções
def verificarUsoFuncoes(tokens, var, fun):
    escopo = "1"
    contEscopo = 0
    idEscopo = 0
    for i in range(len(tokens)):
        if tokens[i] == 'SEMI':
            idEscopo += 1
        if tokens[i] == 'LKEY':
            escopo += str(contEscopo)
        elif tokens[i] == 'RKEY':
            escopo = escopo[0:len(escopo)-1]
            contEscopo += 1
             
        if tokens[i][:2] == 'ID' and tokens[i-1] not in tipos and tokens[i+1] == 'LPAREN': #funcao sendo usada
             
            #funcao (num) ou funcao (str)
            if tokens[i+2] in valores and tokens[i+3] != 'COMMA':
                tipo1 = ''
                if tokens[i+2] == 'NUM':
                    tipo1 = 'INT'
                else:
                    tipo1 = 'STRING'
                funcoes = pegarFuncoesDisponiveis(fun, tokens[i][3:-1], tipo1, None, escopo, idEscopo)
                if funcoes == []:
                    print "Funcao '" + tokens[i][3:-1] + "("+ tipo1 +")' nao esta definida neste local."
                    return False
             
            #funcoes com dois parâmetro de valores        
            elif tokens[i+2] in valores and tokens[i+3] == 'COMMA' and tokens[i+4] in valores:
                tipo1 = ''
                if tokens[i+2] == 'NUM':
                    tipo1 = 'INT'
                else:
                    tipo1 = 'STRING'
                tipo2 = ''
                if tokens[i+4] == 'NUM':
                    tipo2 = 'INT'
                else:
                    tipo2 = 'STRING'
                funcoes = pegarFuncoesDisponiveis(fun, tokens[i][3:-1], tipo1, tipo2, escopo, idEscopo)
                if funcoes == []:
                    print "Funcao '" + tokens[i][3:-1] + "("+ tipo1 +", "+ tipo2 +")' nao esta definida neste local."
                    return False
             
            #funcoes com um parametro ID        
            elif tokens[i+2][:2] == 'ID' and tokens[i+3] != 'COMMA':
                tipo1 = pegarTipoVariavel(var, tokens[i+2][3:-1], escopo, idEscopo)
                funcoes = pegarFuncoesDisponiveis(fun, tokens[i][3:-1], tipo1, None, escopo, idEscopo)
                if funcoes == []:
                    print "Funcao '" + tokens[i][3:-1] + "("+ tipo1 +")' nao esta definida neste local."
                    return False
             
            #funcoes comparametros ID e valor
            elif tokens[i+2][:2] == 'ID' and tokens[i+3] == 'COMMA' and tokens[i+4] in valores:
                tipo1 = pegarTipoVariavel(var, tokens[i+2][3:-1], escopo, idEscopo)
                tipo2 = ''
                if tokens[i+4] == 'NUM':
                    tipo2 = 'INT'
                else:
                    tipo2 = 'STRING'
                funcoes = pegarFuncoesDisponiveis(fun, tokens[i][3:-1], tipo1, tipo2, escopo, idEscopo)
                if funcoes == []:
                    print "Funcao '" + tokens[i][3:-1] + "("+ tipo1 +", "+ tipo2 +")' nao esta definida neste local."
                    return False
             
            #funcoes comparametros valor e ID
            elif tokens[i+2] in valores and tokens[i+3] == 'COMMA' and tokens[i+4][:2] == 'ID':
                tipo1 = ''
                if tokens[i+2] == 'NUM':
                    tipo1 = 'INT'
                else:
                    tipo1 = 'STRING'
                tipo2 = pegarTipoVariavel(var, tokens[i+4][3:-1], escopo, idEscopo)
                funcoes = pegarFuncoesDisponiveis(fun, tokens[i][3:-1], tipo1, tipo2, escopo, idEscopo)
                if funcoes == []:
                    print "Funcao '" + tokens[i][3:-1] + "("+ tipo1 +", "+ tipo2 +")' nao esta definida neste local."
                    return False
             
            #funcoes com dois parametros IDs
            elif tokens[i+2][:2] == 'ID' and tokens[i+3] == 'COMMA' and tokens[i+4][:2] == 'ID':
                tipo1 = pegarTipoVariavel(var, tokens[i+2][3:-1], escopo, idEscopo)
                tipo2 = pegarTipoVariavel(var, tokens[i+4][3:-1], escopo, idEscopo)
                funcoes = pegarFuncoesDisponiveis(fun, tokens[i][3:-1], tipo1, tipo2, escopo, idEscopo)
                if funcoes == []:
                    print "Funcao '" + tokens[i][3:-1] + "("+ tipo1 +", "+ tipo2 +")' nao esta definida neste local."
                    return False
    return True


#Analisa tipos de valores em atribuições        
def verificarAtribuicoes(tokens, variaveis, funcoes):
    escopo = "1"
    contEscopo = 0
    idEscopo = 0
    for i in range(len(tokens)):
        if tokens[i] == 'SEMI':
            idEscopo += 1
        if tokens[i] == 'LKEY':
            escopo += str(contEscopo)
        elif tokens[i] == 'RKEY':
            escopo = escopo[0:len(escopo)-1]
            contEscopo += 1
    
        if tokens[i][:2] == 'ID' and tokens[i+1] == 'BINOP(=)':
            tipo = pegarTipoVariavel(variaveis, tokens[i][3:-1], escopo, idEscopo)
            
            if pegarTipoExpressao(tokens[i+2:], variaveis, funcoes, escopo, idEscopo) != tipo:
                print "Valor invalido para a variavel '"+ tokens[i][3:-1] +"'."
                return False

    return True
    
def verificarReturnsFuncoes(tokens, variaveis, funcoes):
    escopo = "1"
    contEscopo = 0
    idEscopo = 0
    for i in range(len(tokens)):
        if tokens[i] == 'SEMI':
            idEscopo += 1
        if tokens[i] == 'LKEY':
            escopo += str(contEscopo)
        elif tokens[i] == 'RKEY':
            escopo = escopo[0:len(escopo)-1]
            contEscopo += 1
    
        if tokens[i] in tipos and tokens[i+1][:2] == 'ID' and tokens[i+2] == 'LPAREN':
            tipoFuncao = tokens[i]
            escopoFuncao = 0    
            j = i+3
            while True:

                if tokens[i] == 'SEMI':
                    idEscopo += 1    
                if tokens[j] == 'LKEY':
                    escopo += str(contEscopo)
                    escopoFuncao += 1
                elif tokens[j] == 'RKEY':
                    escopo = escopo[0:len(escopo)-1]
                    contEscopo += 1
                    escopoFuncao -= 1
                    if escopoFuncao == 0:
                        break

                if tokens[j] == 'RETURN' and escopoFuncao >= 1:
                    if tipoFuncao != pegarTipoExpressao(tokens[j+1:], variaveis, funcoes, escopo, idEscopo):
                        print "Tipo de retorno invalido."
                        return False
                
                j += 1
    return True