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

verificarUsoVariaveis(tokens, var) 
verificarUsoFuncoes(tokens, var, fun) 
verificarAtribuicoes(tokens, var, fun) 
verificarReturnsFuncoes(tokens, var, fun)