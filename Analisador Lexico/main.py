#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from automato_jav import *

afd = automatoJav()

codigo = ""

for l in sys.stdin:
    codigo += l + " \n "

try:
    tokens = analisadorLexico(afd, codigo.strip())
    for t in tokens:
        print t,
except Exception, e:
    print e
