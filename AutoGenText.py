from Grammatic import *
import random

grammatic = Gramma()
level += 1

def readGrammar(fileName):
    inputFile =  open(fileName,'r')

    lines = [s.rstrip() for s in inputFile.readlines()]
    print('Start lines %s' % lines)
    inputFile.close()
 
    return lines

def sortLines(lines):
    '''not important
    lines.sort()'''
    lines.sort(key = len, reverse = True)
    print('Sorted lines %s' % lines)

def getNewGramma(gramma, letter):
    global grammatic
    global level
    if grammatic !=gramma and len(gramma.nodes)==0:
        gramma.setLevel(level)
        level += 1
    return Gramma(letter,gramma)

def updateGrammaLevel(gramma, letter):
    for node in gramma.nodes:
        if node.isEquals(letter):
            gramma = node
            break
    else:
        newNode = getNewGramma(gramma, letter)
        gramma.addNode(newNode)
        gramma = newNode
    return gramma
    
def printUsedLine(line):
    print('Used line "{0}"'.format(line))


def printGrammatic():
    global grammatic
    print("Current gramma:")
    grammatic.printed()
    print('-'*80)

LEN_RULES = (2)
def updateMaxLenLines(maxLen,lines):
    global grammatic
    maxLenLines = [x for x in lines if len(x)==maxLen]
    for currentLine in maxLenLines:
        printUsedLine(currentLine)
        grammaLevel = grammatic
        for letter in currentLine[:-LEN_RULES]:
            grammaLevel = updateGrammaLevel(grammaLevel, letter)
        updateGrammaLevel(grammaLevel, currentLine[-LEN_RULES:])
        printGrammatic()
    return len(maxLenLines)

def updateOtherLines(usedLinesCount,lines):
    global grammatic
    otherLines = lines[usedLinesCount:]
    for currentLine in otherLines:
        printUsedLine(currentLine)
        grammaLevel = grammatic
        for letter in currentLine:
            grammaLevel = updateGrammaLevel(grammaLevel, letter)
        printGrammatic()
    
def firstStep(lines):
    print('First step')
    sortLines(lines)
    countElement = len(lines)
    maxLen = len(lines[0])
    usedLinesCount = updateMaxLenLines(maxLen,lines)
    updateOtherLines(usedLinesCount,lines)
    print('-'*80)

def findRules(rules,gramma):
    for node in gramma.nodes:
        if node.isRules():
            rules.append(node)
        findRules(rules,node)

def changeRecursion(rule, node):
    rule.updateParentRecursion(node)
    
def updateRecursion(rules,gramma):
    for node in gramma.nodes:
        if len(rules)==0:
            break

        removedRules = []
        for rule in rules:
            if node.getRecursionObject(rule)!= None:
                print('Found recursion "{0}" at "{1}"'.format(node,rule))
                removedRules.append(rule)

        if len(removedRules)>0:
            for rule in removedRules:
                changeRecursion(rule,node)
                rules.remove(rule)
            
        updateRecursion(rules,gramma)
        

def secondStep():
    print('Second step')
    global grammatic
    rules = []
    for node in grammatic.nodes:
        findRules(rules,node)
    print('Rules {0}'.format(rules))
    for node in grammatic.nodes:
        updateRecursion(rules, node)
    printGrammatic()
    print('-'*80)

def injectGrammaBlock(left,right):
    if right.parent==left:
        left.mergeGramma(right)
    else:
        right.mergeGramma(left)
    

def findSingleEqualGramma():
    global grammatic
    result = Gramma.findEqualGramma(grammatic,grammatic)
    findResult = (result!=False)
    if findResult:
        print('*'*80)
        for grammaBlock in result:
            print('Node block')
            for node in grammaBlock.nodes:
                print(node)
            print('*'*80)

        injectGrammaBlock(result[0],result[1])
        printGrammatic()
       
    return findResult

def thirdStep():
    print('Third step')
    while (findSingleEqualGramma()):
        pass
    print('_'*80)


def printResult():
    print('^'*80)
    print("Result set")
    printGrammatic()
    print('^'*80)

def printExample():
    print('Grammatic Example')
    global grammatic
    count = 21
    maxDepth = 12
    for i in range(count):
        grammaLine = ''
        grammaPos = grammatic
        for j in range(random.randint(1,maxDepth)):
            countNodes = len(grammaPos.nodes)
            if countNodes==0:
                break
            grammaPos = grammaPos.nodes[random.randint(0,countNodes-1)]
            grammaLine+=grammaPos.letter
        print(grammaLine)

    print('^'*80)

lines = readGrammar('input.txt')
if len(lines)>1:
    firstStep(lines)
    secondStep()
    thirdStep()
    printResult()
    printExample()
else:
    print("Len lines <1")
