from af_lr import *
import sys


def analisadorSintatico(af, linha):
    estadoAtual = 0
    palavraAtual = ""
    for p in linha.split(' '):
        palavraAtual += " " + p
        if af.proximoEstado(estadoAtual, p) == None:
            return "Erro sintatico -> '" + palavraAtual + "'"
        else:
            estadoAtual = af.proximoEstado(estadoAtual, p)
    if af.ehFinal(estadoAtual):
        return "SUCESSO!"
    return "ERRO"

af = af_lr()

for l in sys.stdin:
    print analisadorSintatico(af, l[0:len(l)-1])
