from tree import *
from copy import copy

BINOP = ['+', '-', '*', '/']
exprs = []
contReg = 1
  
def getParam(expr):
    if expr == '' or expr is None:
        return (None, None)
    
    i = 0
    escopo = 0
    while i < len(expr):
        if expr[i] == '(':
            escopo += 1
        elif expr[i] == ')':
            escopo -= 1
        if expr[i] == ',' and escopo == 0:
            param1 = expr[0:i]            
            param2 = expr[i+1:]
            return (param1, param2)
        i += 1
                
    if expr[0:3] == 'MEM':
        return (expr[4:-1], None)          
  
def makeTree(expr):
    expr = expr.strip()
    #Casos base
    if expr == '' or expr is None:
        return None    
    if expr[0:5] == 'CONST' or expr.isdigit():
        return Tree(expr, None, None)
    if expr[0:4] == 'TEMP':
        return Tree(expr, None, None)    
    #Percorrendo expressao    
    i = 0
    while i < len(expr):
        if expr[i] in BINOP:
            (param1, param2) = getParam(expr[i+2:-1])
            return Tree(expr[i], makeTree(param1), makeTree(param2))        
        if expr[i:i+4] == 'MOVE':
            (param1, param2) = getParam(expr[i+5:-1])
            return Tree(expr[i:i+4], makeTree(param1), makeTree(param2))
        if expr[i:i+3] == 'MEM':
            return Tree(expr[i:i+3], makeTree(expr[i+4:-1]), None)                
        i += 1

def calculateCosts(tree):
    
    if tree == None:
        return 0
    for t in getPosOrderList(tree):
        if t.value[0:4] == 'TEMP':
            t.cost = 0
        elif t.value[0:5] == 'CONST':
            t.cost = 1
        
        if t.value == 'MEM':
            if t.right.value[0:5] != 'CONST' and t.right.value != '+':
                t.cost = 1 + calculateCosts(t.right)
            else:
                t.right.groupId = t.groupId
                t.cost = calculateCosts(t.right)
            
        elif t.value == '+':
            if t.right.value[0:5] != 'CONST' and t.left.value[0:5] == 'CONST':
                t.left.groupId = t.groupId
                t.cost = calculateCosts(t.right)
            elif t.right.value[0:5] == 'CONST' and t.left.value[0:5] != 'CONST':
                t.right.groupId = t.groupId
                t.cost = calculateCosts(t.left)
            elif t.right.value[0:5] == 'CONST' and t.left.value[0:5] == 'CONST':
                t.right.groupId = t.groupId
                t.cost = calculateCosts(t.left)    
            elif t.right.value[0:5] != 'CONST' and t.left.value[0:5] != 'CONST':
                t.cost = 1 + calculateCosts(t.right) + calculateCosts(t.left)
        
        elif t.value == '-':
            if t.left.value[0:5] == 'CONST':
                t.left.groupId = t.groupId
                t.cost = calculateCosts(t.right)
            elif t.right.value[0:5] != 'CONST' and t.left.value[0:5] != 'CONST':
                t.cost = 1 + calculateCosts(t.right) + calculateCosts(t.left)
        
        elif t.value in BINOP:
            t.cost = 1 + calculateCosts(t.right) + calculateCosts(t.left)        
        
        elif t.value == 'MOVE':
            if t.right.value == 'MEM' and t.left.value == 'MEM':
                t.cost = calculateCosts(t.right) + calculateCosts(t.left)
                t.right.groupId = t.groupId
                t.left.groupId = t.groupId
            elif t.left.value != 'MEM':
                t.right.groupId = t.groupId
                t.cost = calculateCosts(t.right) + 1 + calculateCosts(t.left) 
            
    return t.cost

def makeGroups(tree):
    groups = []
    posOrderList = getPosOrderList(tree)
    i = 0
    while i < len(posOrderList):
        group = []
        currentId = posOrderList[i].groupId
        for t in posOrderList:
            if t.groupId == currentId:
                group.append(t)
        if group not in groups:
            groups.append(group)
        i += 1                  
   
    return groups

def valueToExpr(value):
    if value[0:5] == 'CONST':
        return value[6:]
    elif value[0:4] == 'TEMP':
        return value[5:]
    elif value == 'FP':
        return 'fp'
    elif value.isdigit():
        return str(value)

def generateExpr(tree):
    global contReg
    global exprs
    if tree == None:
        return ''
    
    if tree.expred != False:
        return tree.expred
    
    expr = ''        
    for g in makeGroups(tree):
        if len(g) == 1:
            if g[0].value == '+':
                expr = 'ADD   r' + str(contReg) + ' <- ' + generateExpr(g[0].right) + ' + ' + generateExpr(g[0].left)
            elif g[0].value == '-':
                expr = 'SUB   r' + str(contReg) + ' <- ' + generateExpr(g[0].right) + ' - ' + generateExpr(g[0].left)
            elif g[0].value == '*':        
                expr = 'MUL   r' + str(contReg) + ' <- ' + generateExpr(g[0].right) + ' * ' + generateExpr(g[0].left)
            elif g[0].value == '/':
                expr = 'DIV   r' + str(contReg) + ' <- ' + generateExpr(g[0].right) + ' / ' + generateExpr(g[0].left)
            elif g[0].value == 'MEM':
                expr = 'LOAD  r' + str(contReg) + ' <- M[' + generateExpr(g[0].right) + ']'
            elif g[0].value[0:5] == 'CONST':
                expr = 'ADDI  r' + str(contReg) + ' <- r0 + ' + g[0].value[6:]
            elif g[0].value[0:4] == 'TEMP':
                return 'r' + g[0].value[5:]             
            elif g[0].value.isdigit():
                expr = 'ADDI  r' + str(contReg) + ' <- r0 + ' + g[0].value
            
        else:
            if g[-1].value == '+':
                if g[-1].right in g:
                    expr = 'ADD r' + str(contReg) + ' <- ' + valueToExpr(g[-1].right.value) + ' + ' + generateExpr(g[-1].left)
                elif g[-1].left in g:
                    expr = 'ADD r' + str(contReg) + ' <- ' + generateExpr(g[-1].right) + ' + ' + valueToExpr(g[-1].left.value)                 
            elif g[-1].value == '-':
                if g[-1].left in g:
                    expr = 'SUB r' + str(contReg) + ' <- ' + generateExpr(g[-1].right) + ' - ' + valueToExpr(g[-1].left.value)
            elif g[-1].value == 'MEM':
                if g[-1].right in g:
                    expr = 'LOAD r' + str(contReg) + ' <- M[' + generateExpr(g[-1].right) + ']'
            elif g[-1].value == 'MOVE':
                if g[-1].left.value != 'MEM':
                    expr = 'STORE M[' + generateExpr(g[-1].right) + ' + ' + generateExpr(g[-1].left) + '] <- r' + str(contReg)
                    break
                elif g[-1].left.value == 'MEM' and g[-1].left in g:    
                    expr = 'MOVEM' + ' M[' + generateExpr(g[-1].right.right) + '] <- M[' + generateExpr(g[-1].left.right) + ']'
                    break
                    
    tree.expred = 'r'+str(contReg)        
    exprs.append(expr)        
    contReg += 1
    return tree.expred
            
expr = raw_input()
tree = makeTree(expr)

#Inicializacao de grupos
i = 1
for t in getPosOrderList(tree):
    t.groupId = i
    i += 1

calculateCosts(tree)
printIndented(tree)
print "\n"
generateExpr(tree)
for expr in exprs:
    print expr