#!/usr/bin/env python
# -*- coding: utf-8 -*-

def letras():
	return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
 		'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
 		'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
 		'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_']

def digitos():
	numeros = []
	for i in range(10):
		numeros.append(str(i))
	return numeros

def operadoresAritmeticos():
	return ['+', '-', '*', '/', '%', '=']

def caracteresEspeciais():
	return ['!', '<', '>', '&', '|',
	',', ';', '[', ']', '(', ')', '{', '}']

def simbolosEspeciais():
	return ['?', "'", ':', '@', '\\', '.', '"']

def alfabeto():
	return letras() + digitos() + operadoresAritmeticos() + caracteresEspeciais() + simbolosEspeciais()
