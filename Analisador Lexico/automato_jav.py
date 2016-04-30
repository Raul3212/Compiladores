#!/usr/bin/env python
# -*- coding: utf-8 -*-

from definicoes import *
from automato import *

def automatoJav():

    afd = AFD(84)

    #Definindo Rotulos e estados finais
    afd.setTokenEstado(1, "ID")
    afd.setTokenEstado(2, "IF")
    afd.setTokenEstado(3, "ID")
    afd.setTokenEstado(4, "ID")
    afd.setTokenEstado(5, "INT")
    afd.setTokenEstado(6, "ID")
    afd.setTokenEstado(7, "ID")
    afd.setTokenEstado(8, "ID")
    afd.setTokenEstado(9, "ID")
    afd.setTokenEstado(10, "ID")
    afd.setTokenEstado(11, "STRING")
    afd.setTokenEstado(12, "NUM")
    afd.setTokenEstado(14, "STR")
    afd.setTokenEstado(15, "ID")
    afd.setTokenEstado(16, "ID")
    afd.setTokenEstado(17, "ID")
    afd.setTokenEstado(18, "ELSE")
    afd.setTokenEstado(19, "LPAREN")
    afd.setTokenEstado(20, "RPAREN")
    afd.setTokenEstado(21, "LKEY")
    afd.setTokenEstado(22, "RKEY")
    afd.setTokenEstado(23, "LBRAC")
    afd.setTokenEstado(24, "RBRAC")
    afd.setTokenEstado(25, "PNT")
    afd.setTokenEstado(26, "COMMA")
    afd.setTokenEstado(27, "SEMI")
    afd.setTokenEstado(28, "BINOP")
    afd.setTokenEstado(29, "BINOP")
    afd.setTokenEstado(30, "BINOP")
    afd.setTokenEstado(31, "BINOP")
    afd.setTokenEstado(32, "BINOP")
    afd.setTokenEstado(33, "BINOP")
    afd.setTokenEstado(34, "BINOP")
    afd.setTokenEstado(35, "BINOP")
    afd.setTokenEstado(36, "BINOP")
    afd.setTokenEstado(37, "NOT")
    afd.setTokenEstado(38, "BINOP")
    afd.setTokenEstado(44, "RETURN")
    afd.setTokenEstado(45, "BINOP")
    afd.setTokenEstado(46, "ID")
    afd.setTokenEstado(47, "ID")
    afd.setTokenEstado(48, "ID")
    afd.setTokenEstado(49, "ID")
    afd.setTokenEstado(50, "CLASS")
    afd.setTokenEstado(51, "ID")
    afd.setTokenEstado(52, "ID")
    afd.setTokenEstado(53, "ID")
    afd.setTokenEstado(54, "ID")
    afd.setTokenEstado(55, "ID")
    afd.setTokenEstado(56, "PUBLIC")
    afd.setTokenEstado(57, "ID")
    afd.setTokenEstado(58, "ID")
    afd.setTokenEstado(59, "ID")
    afd.setTokenEstado(60, "ID")
    afd.setTokenEstado(61, "ID")
    afd.setTokenEstado(62, "PRIVATE")
    afd.setTokenEstado(63, "ID")
    afd.setTokenEstado(64, "ID")
    afd.setTokenEstado(65, "ID")
    afd.setTokenEstado(66, "ID")
    afd.setTokenEstado(67, "ID")
    afd.setTokenEstado(68, "ID")
    afd.setTokenEstado(69, "PROTECTED")
    afd.setTokenEstado(70, "ID")
    afd.setTokenEstado(71, "ID")
    afd.setTokenEstado(72, "ID")
    afd.setTokenEstado(73, "NULL")
    afd.setTokenEstado(74, "UNOP")
    afd.setTokenEstado(75, "BINOP")
    afd.setTokenEstado(76, "UNOP")
    afd.setTokenEstado(77, "UNOP")
    afd.setTokenEstado(78, "BINOP")
    afd.setTokenEstado(79, "ERRO")
    afd.setTokenEstado(80, "BINOP")

    for i in range(84):
        token_i = afd.getTokenEstado(i)
        if token_i == "ID":
            afd.addTransicao(i, simbolosEspeciais(), 79)
        elif token_i == "NUM":
            afd.addTransicao(i, letras() + simbolosEspeciais() + ['(', '{', '}', '['], 79)
        elif token_i == "STR":
            afd.addTransicao(i, letras() + digitos(), 79)
        elif token_i == "NOT":
            b = operadoresAritmeticos()
            b.remove('=')
            afd.addTransicao(i, caracteresEspeciais() + simbolosEspeciais() + digitos() + b, 79)
        elif token_i == "UNOP":
            a = caracteresEspeciais()
            a.remove(';')
            a.remove(',')
            afd.addTransicao(i, a + simbolosEspeciais() + digitos() + operadoresAritmeticos(), 79)
        elif token_i == "BINOP":
            a = caracteresEspeciais()
            a.remove('(')
            b = operadoresAritmeticos()
            b.remove('=')
            c = simbolosEspeciais()
            c.remove('"')
            afd.addTransicao(i, a + b + c, 79)
        elif token_i == "STRING":
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + caracteresEspeciais(), 79)
        elif token_i == "INT":
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + caracteresEspeciais(), 79)
        elif token_i == "NULL":
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + caracteresEspeciais(), 79)
        elif token_i == "PUBLIC":
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + caracteresEspeciais(), 79)
        elif token_i == "PRIVATE":
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + caracteresEspeciais(), 79)
        elif token_i == "PROTECTED":
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + caracteresEspeciais(), 79)
        elif token_i == "IF":
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + [')', '{', '}'], 79)
        elif token_i == "ELSE":
            a = caracteresEspeciais()
            a.remove('{')
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + a, 79)
        elif token_i == "LPAREN":
            a = caracteresEspeciais()
            a.remove('(')
            a.remove(')')
            b = simbolosEspeciais()
            b.remove('"')
            c = operadoresAritmeticos()
            c.remove('+')
            c.remove('-')
            afd.addTransicao(i, a + b + c, 79)
        elif token_i == "RPAREN":
            afd.addTransicao(i, simbolosEspeciais() + letras() + ['(', '['], 79)
        elif token_i == "LKEY":
            a = caracteresEspeciais()
            a.remove('(')
            b = simbolosEspeciais()
            b.remove('"')
            afd.addTransicao(i, operadoresAritmeticos() + a + b, 79)
        elif token_i == "RKEY":
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + letras() + [')', '{', ';'], 79)
        elif token_i == "LBRAC":
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + [')', '{', '}'], 79)
        elif token_i == "RBRAC":
            afd.addTransicao(i, letras() + operadoresAritmeticos() + simbolosEspeciais() + ['(', ')', '{', '}'], 79)
        elif token_i == "PNT":
            afd.addTransicao(i, alfabeto(), 79)
        elif token_i == "SEMI":
            a = caracteresEspeciais()
            a.remove('(')
            b = operadoresAritmeticos()
            b.remove('+')
            b.remove('-')
            b.remove('/')
            afd.addTransicao(i, b + simbolosEspeciais() + a, 79)
        elif token_i == "COMMA":
            a = caracteresEspeciais()
            a.remove('(')
            b = operadoresAritmeticos()
            b.remove('+')
            b.remove('-')
            c = simbolosEspeciais()
            c.remove('"')
            afd.addTransicao(i, a + b + c, 79)
        elif token_i == "RETURN":
            a = caracteresEspeciais()
            a.remove('(')
            afd.addTransicao(i, operadoresAritmeticos() + simbolosEspeciais() + a, 79)

    #Algumas transicoes precisaram ser movidas para depois do processamento de erros

    #TRANSICOES do estado 0
    a = letras()
    a.remove('i')
    a.remove('S')
    a.remove('r')
    a.remove('c')
    a.remove('p')
    a.remove('n')

    afd.addTransicao(0, ['i'], 1)
    afd.addTransicao(0, a, 3) #todo o letras exceto i, s e r
    afd.addTransicao(0, ['S'], 6)
    afd.addTransicao(0, digitos(), 12)
    afd.addTransicao(0, ['"'], 13)
    afd.addTransicao(0, ['e'], 15)
    afd.addTransicao(0, ['('], 19)
    afd.addTransicao(0, [')'], 20)
    afd.addTransicao(0, ['{'], 21)
    afd.addTransicao(0, ['}'], 22)
    afd.addTransicao(0, ['['], 23)
    afd.addTransicao(0, [']'], 24)
    afd.addTransicao(0, ['.'], 25)
    afd.addTransicao(0, [','], 26)
    afd.addTransicao(0, [';'], 27)
    afd.addTransicao(0, ['='], 28)
    afd.addTransicao(0, ['+'], 30)
    afd.addTransicao(0, ['&'], 31)
    afd.addTransicao(0, ['|'], 33)
    afd.addTransicao(0, ['<','>'], 35)
    afd.addTransicao(0, ['!'], 37)
    afd.addTransicao(0, ['r'], 39)
    afd.addTransicao(0, ['c'], 46)
    afd.addTransicao(0, ['p'], 51)
    afd.addTransicao(0, ['n'], 70)
    afd.addTransicao(0, ['-'], 75)
    afd.addTransicao(0, ['*'], 78)
    afd.addTransicao(0, ['/'], 80)
    #TRANSICOES do estado 1
    a = letras()
    a.remove('f')
    a.remove('n')
    afd.addTransicao(1, ['n'], 4)
    afd.addTransicao(1, ['f'], 2)
    afd.addTransicao(1, a + digitos(), 3)
    #todos os digitos e letras exceto f e n

    #TRANSICOES do estado 2
    afd.addTransicao(2, letras() + digitos(), 3)

    #TRANSICOES do estado 3
    afd.addTransicao(3, letras() + digitos(), 3)

    #TRANSICOES do estado 4
    a = letras()
    a.remove('t')
    afd.addTransicao(4, ['t'], 5)
    afd.addTransicao(4, a + digitos(), 3)

    #TRANSICOES do estado 5
    afd.addTransicao(5, letras() + digitos(), 3)

    #TRANSICOES do estado 6
    a = letras()
    a.remove('t')
    afd.addTransicao(6, ['t'], 7)
    afd.addTransicao(6, a + digitos(), 3)

    #TRANSICOES do estado 7
    a = letras()
    a.remove('r')
    afd.addTransicao(7, ['r'], 8)
    afd.addTransicao(7, a + digitos(), 3)

    #TRANSICOES do estado 8
    a = letras()
    a.remove('i')
    afd.addTransicao(8, ['i'], 9)
    afd.addTransicao(8, a + digitos(), 3)

    #TRANSICOES do estado 9
    a = letras()
    a.remove('n')
    afd.addTransicao(9, ['n'], 10)
    afd.addTransicao(9, a + digitos(), 3)

	#TRANSICOES do estado 10
    a = letras()
    a.remove('g')
    afd.addTransicao(10, ['g'], 11)
    afd.addTransicao(10, a + digitos(), 3)

    #TRANSICOES do estado 11
    afd.addTransicao(11, letras() + digitos() , 3)

    #TRANSICOES do estado 12
    afd.addTransicao(12, digitos(), 12)

    #TRANSICOES do estado 13
    a = alfabeto()
    a.remove('"')
    afd.addTransicao(13, ['"'], 14)
    afd.addTransicao(13, a + [' '], 13)

    #TRANSICOES do estado 15
    a = letras()
    a.remove('l')
    afd.addTransicao(15, ['l'], 16)
    afd.addTransicao(15, a + digitos() , 3)

    #TRANSICOES do estado 16
    a = letras()
    a.remove('s')
    afd.addTransicao(16, ['s'], 17)
    afd.addTransicao(16, a + digitos() , 3)

    #TRANSICOES do estado 17
    a = letras()
    a.remove('e')
    afd.addTransicao(17, ['e'], 18)
    afd.addTransicao(17, a + digitos() , 3)

    #TRANSICOES do estado 18
    afd.addTransicao(18, letras() + digitos() , 3)

    #TRANSICOES do estado 31
    afd.addTransicao(31, ['&'], 32)

    #TRANSICOES do estado 33
    afd.addTransicao(33, ['|'], 34)

    #TRANSICOES do estado 35
    afd.addTransicao(35, ['='], 36)

    #TRANSICOES do estado 37
    afd.addTransicao(37, ['='], 38)

    #TRANSICOES do estado 39
    a = letras()
    a.remove('e')
    afd.addTransicao(39, ['e'], 40)
    afd.addTransicao(39, a + digitos() , 3)

    #TRANSICOES do estado 40
    a = letras()
    a.remove('t')
    afd.addTransicao(40, ['t'], 41)
    afd.addTransicao(40, a + digitos() , 3)

    #TRANSICOES do estado 41
    a = letras()
    a.remove('u')
    afd.addTransicao(41, ['u'], 42)
    afd.addTransicao(41, a + digitos() , 3)

    #TRANSICOES do estado 42
    a = letras()
    a.remove('r')
    afd.addTransicao(42, ['r'], 43)
    afd.addTransicao(42, a + digitos() , 3)

    #TRANSICOES do estado 43
    a = letras()
    a.remove('n')
    afd.addTransicao(43, ['n'], 44)
    afd.addTransicao(43, a + digitos() , 3)

    #TRANSICOES do estado 44
    afd.addTransicao(44, letras() + digitos() , 3)

    #TRANSICOES do estado 46
    a = letras()
    a.remove('l')
    afd.addTransicao(46, ['l'], 47)
    afd.addTransicao(46, a + digitos() , 3)

    #TRANSICOES do estado 47
    a = letras()
    a.remove('a')
    afd.addTransicao(47, ['a'], 48)
    afd.addTransicao(47, a + digitos() , 3)

    #TRANSICOES do estado 48
    a = letras()
    a.remove('s')
    afd.addTransicao(48, ['s'], 49)
    afd.addTransicao(48, a + digitos() , 3)

    #TRANSICOES do estado 49
    a = letras()
    a.remove('s')
    afd.addTransicao(49, ['s'], 50)
    afd.addTransicao(49, a + digitos() , 3)

    #TRANSICOES do estado 50
    afd.addTransicao(50, letras() + digitos() , 3)

    #TRANSICOES do estado 51
    a = letras()
    a.remove('u')
    a.remove('r')
    afd.addTransicao(51, ['u'], 52)
    afd.addTransicao(51, ['r'], 57)
    afd.addTransicao(51, a + digitos() , 3)

    #TRANSICOES do estado 52
    a = letras()
    a.remove('b')
    afd.addTransicao(52, ['b'], 53)
    afd.addTransicao(52, a + digitos() , 3)

    #TRANSICOES do estado 53
    a = letras()
    a.remove('l')
    afd.addTransicao(53, ['l'], 54)
    afd.addTransicao(53, a + digitos() , 3)

    #TRANSICOES do estado 54
    a = letras()
    a.remove('i')
    afd.addTransicao(54, ['i'], 55)
    afd.addTransicao(54, a + digitos() , 3)

    #TRANSICOES do estado 55
    a = letras()
    a.remove('c')
    afd.addTransicao(55, ['c'], 56)
    afd.addTransicao(55, a + digitos() , 3)

    #TRANSICOES do estado 56
    afd.addTransicao(56, letras() + digitos() , 3)

    #TRANSICOES do estado 57
    a = letras()
    a.remove('i')
    a.remove('o')
    afd.addTransicao(57, ['i'], 58)
    afd.addTransicao(57, ['o'], 62)
    afd.addTransicao(57, a + digitos() , 3)

    #TRANSICOES do estado 58
    a = letras()
    a.remove('v')
    afd.addTransicao(58, ['v'], 59)
    afd.addTransicao(58, a + digitos() , 3)

    #TRANSICOES do estado 59
    a = letras()
    a.remove('a')
    afd.addTransicao(59, ['a'], 60)
    afd.addTransicao(59, a + digitos() , 3)

    #TRANSICOES do estado 60
    a = letras()
    a.remove('t')
    afd.addTransicao(60, ['t'], 61)
    afd.addTransicao(60, a + digitos() , 3)

    #TRANSICOES do estado 61
    a = letras()
    a.remove('e')
    afd.addTransicao(61, ['e'], 62)
    afd.addTransicao(61, a + digitos() , 3)

    #TRANSICOES do estado 62
    afd.addTransicao(62, letras() + digitos() , 3)

    #TRANSICOES do estado 63
    a = letras()
    a.remove('t')
    afd.addTransicao(63, ['t'], 64)
    afd.addTransicao(63, a + digitos() , 3)

    #TRANSICOES do estado 64
    a = letras()
    a.remove('e')
    afd.addTransicao(64, ['e'], 65)
    afd.addTransicao(64, a + digitos() , 3)

    #TRANSICOES do estado 65
    a = letras()
    a.remove('c')
    afd.addTransicao(65, ['c'], 66)
    afd.addTransicao(65, a + digitos() , 3)

    #TRANSICOES do estado 66
    a = letras()
    a.remove('t')
    afd.addTransicao(66, ['t'], 67)
    afd.addTransicao(66, a + digitos() , 3)

    #TRANSICOES do estado 67
    a = letras()
    a.remove('e')
    afd.addTransicao(67, ['e'], 68)
    afd.addTransicao(67, a + digitos() , 3)

    #TRANSICOES do estado 68
    a = letras()
    a.remove('d')
    afd.addTransicao(68, ['d'], 69)
    afd.addTransicao(68, a + digitos() , 3)

    #TRANSICOES do estado 69
    afd.addTransicao(69, letras() + digitos() , 3)

    #TRANSICOES do estado 70
    a = letras()
    a.remove('u')
    afd.addTransicao(70, ['u'], 71)
    afd.addTransicao(70, a + digitos() , 3)

    #TRANSICOES do estado 71
    a = letras()
    a.remove('l')
    afd.addTransicao(71, ['l'], 72)
    afd.addTransicao(71, a + digitos() , 3)

    #TRANSICOES do estado 72
    a = letras()
    a.remove('l')
    afd.addTransicao(72, ['l'], 73)
    afd.addTransicao(72, a + digitos() , 3)

    #TRANSICOES do estado 73
    afd.addTransicao(73, letras() + digitos() , 3)

    #TRANSICOES do estado 81
    afd.addTransicao(81, alfabeto() + [' '], 81)
    afd.addTransicao(81, ['\n'], 0)

    #TRANSICOES do estado 82
    afd.addTransicao(82, alfabeto() + [' '], 82)
    afd.addTransicao(82, ['*'], 83)

    #TRANSICOES do estado 83
    a = alfabeto()
    a.remove('/')
    afd.addTransicao(83, ['/'], 0)
    afd.addTransicao(83, a + [' '], 82)

    #TRANSICOES do estado 28
    afd.addTransicao(28, ['='], 29)

    #TRANSICOES do estado 30
    afd.addTransicao(30, ['='], 45)
    afd.addTransicao(30, ['+'], 74)

    #TRANSICOES do estado 75
    afd.addTransicao(75, ['='], 45)
    afd.addTransicao(75, ['-'], 76)

    #TRANSICOES do estado 78
    afd.addTransicao(78, ['='], 45)

    #TRANSICOES do estado 80
    afd.addTransicao(80, ['/'], 81)
    afd.addTransicao(80, ['*'], 82)

    return afd
