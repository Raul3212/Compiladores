#!/usr/bin/env python
# -*- coding: utf-8 -*-

from automato_jav import *
from semantico import *
import sys

afd = automatoJav()
codigo = ""
for l in sys.stdin:
    codigo += l + " \n "
try:
    tokens = analisadorLexico(afd, codigo.strip())
except Exception, e:
    print e

(var, fun) = extrairIDs(tokens)
if (var, fun) != ([], []):
    if verificarUsoVariaveis(tokens, var) and verificarUsoFuncoes(tokens, var, fun): 
        if verificarAtribuicoes(tokens, var, fun) and verificarReturnsFuncoes(tokens, var, fun):
            print "Sucesso!"
