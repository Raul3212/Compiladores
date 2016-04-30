#!/usr/bin/env python
# -*- coding: utf-8 -*-

def lista2conjunto(lista):
    lr = []
    for e in lista:
        if not (e in lr):
            lr.append(e)
    return lr

def uniao(list1, list2):
    for e in list2:
        if not (e in list1):
            list1.append(e)
    return list1
