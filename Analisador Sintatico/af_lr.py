from automato import *

def af_lr():
    af = AF_LR1(22)

    af.addTransicao(0, "print", 1)
    af.addTransicao(0, "S", 2)
    af.addTransicao(0, "id", 4)

    af.addTransicao(1, "(", 3)

    af.addTransicao(2, ";", 5)

    af.addTransicao(3, "id", 6)
    af.addTransicao(3, "L", 10)
    af.addTransicao(3, "E", 11)
    af.addTransicao(3, "num", 12)
    af.addTransicao(3, "(", 15)

    af.addTransicao(4, ":=", 7)

    af.addTransicao(5, "print", 1)
    af.addTransicao(5, "S", 2)
    af.addTransicao(5, "id", 4)

    af.addTransicao(7, "id", 6)
    af.addTransicao(7, "E", 8)
    af.addTransicao(7, "num", 12)
    af.addTransicao(7, "(", 15)

    af.addTransicao(8, "+", 9)

    af.addTransicao(9, "num", 12)
    af.addTransicao(9, "(", 15)
    af.addTransicao(9, "E", 13)
    af.addTransicao(9, "id", 6)

    af.addTransicao(10, ",", 16)
    af.addTransicao(10, ")", 14)

    af.addTransicao(11, "+", 9)

    af.addTransicao(13, "+", 9)

    af.addTransicao(15, "print", 1)
    af.addTransicao(15, "S", 17)

    af.addTransicao(16, "id", 6)
    af.addTransicao(16, "num", 12)
    af.addTransicao(16, "(", 15)
    af.addTransicao(16, "E", 18)

    af.addTransicao(17, ";", 5)
    af.addTransicao(17, ",", 19)

    af.addTransicao(18, "+", 9)

    af.addTransicao(19, "E", 20)
    af.addTransicao(19, "(", 15)
    af.addTransicao(19, "num", 12)

    af.addTransicao(20, "+", 9)
    af.addTransicao(20, ")", 21)

    af.addItem(0, 'S2', ". S $", "")
    af.addItem(0, 'S', ". id := E $", "")
    af.addItem(0, 'S', ". S ; S $", "")
    af.addItem(0, 'S', ". print ( L ) $", "(")

    af.addItem(1, 'S', "print . ( L ) $", "")

    af.addItem(2, 'S2', "S . $", "")
    af.addItem(2, 'S', "S . ; S $", "")

    af.addItem(3, 'S', "print ( . L ) $", "")
    af.addItem(3, 'L', ". E $", "")
    af.addItem(3, 'L', ". L , E $", "")
    af.addItem(3, 'E', ". id $", "")
    af.addItem(3, 'E', ". num $", "")
    af.addItem(3, 'E', ". E + E $", "")
    af.addItem(3, 'E', ". ( S , E ) $", "")

    af.addItem(4, 'S', "id . := E $", "")

    af.addItem(5, 'S', "S ; . S $", "")
    af.addItem(5, 'S', ". id $", "")
    af.addItem(5, 'S', ". S ; S $", "")
    af.addItem(5, 'S', ". print ( L ) $", "(")

    af.addItem(6, 'E', "id . $", "")

    af.addItem(7, 'S', "id . := E $", "")
    af.addItem(7, 'E', ". id $", "")
    af.addItem(7, 'E', ". num $", "")
    af.addItem(7, 'E', ". E + E $", "")
    af.addItem(7, 'E', ". ( S , E ) $", "")

    af.addItem(8, 'S', "id := E . $", "")
    af.addItem(8, 'E', "E . + E $", "")

    af.addItem(9, 'E', "E + . E $", "")
    af.addItem(9, 'E', ". id $", "")
    af.addItem(9, 'E', ". num $", "")
    af.addItem(9, 'E', ". E + E $", "")
    af.addItem(9, 'E', ". ( S , E ) $", "")

    af.addItem(10, 'S', "print ( L . ) $", "")
    af.addItem(10, 'L', "L . , E $", "")

    af.addItem(11, 'L', "E . $", "")
    af.addItem(11, 'E', "E . + E $", "")

    af.addItem(12, 'E', "num . $", "")

    af.addItem(13, 'E', "E + E . $", "")
    af.addItem(13, 'E', "E . + E $", "")

    af.addItem(14, 'S', "print ( L ) . $", "")

    af.addItem(15, 'E', "( . S , E ) $", "")
    af.addItem(15, 'S', ". S ; S $", "")
    af.addItem(15, 'S', ". id := E $", "")
    af.addItem(15, 'S', ". print ( L ) $", "(")

    af.addItem(16, 'L', "L , . E $", "")
    af.addItem(16, 'E', ". id $", "")
    af.addItem(16, 'E', ". num $", "")
    af.addItem(16, 'E', ". E + E $", "")
    af.addItem(16, 'E', ". ( S , E ) $", "")

    af.addItem(17, 'E', "( S . , E ) $", "")
    af.addItem(17, 'S', "S . ; S $", "")

    af.addItem(18, 'L', "L , E . $", "")
    af.addItem(18, 'E', "E . + E $", "")

    af.addItem(19, 'E', "( S , . E ) $", "")
    af.addItem(19, 'E', ". id $", "")
    af.addItem(19, 'E', ". num $", "")
    af.addItem(19, 'E', ". E + E $", "")
    af.addItem(19, 'E', ". ( S , E ) $", "")

    af.addItem(20, 'E', "( S , E . ) $", "")
    af.addItem(20, 'E', "E . + E $", "")

    af.addItem(21, 'E', "( S , E ) . $", "")

    af.setAsFinal(6)
    af.setAsFinal(8)
    af.setAsFinal(11)
    af.setAsFinal(12)
    af.setAsFinal(13)
    af.setAsFinal(14)
    af.setAsFinal(21)

    return af
