level = 0

class Gramma:          
        def __init__(self, letter=None, parent=None):
                self.initGramma(0 if parent==None else -1,letter,parent if parent != None else self)

        def initGramma(self, level, letter, parent):
                self.letter = letter
                self.level = level
                self.nodes = []
                self.parent = parent
                self.parentLevel = parent.level
                self.isRecursion = False
                self.recursionRepeat = []

        def setLevel(self, level):
                self.level = level

        def addNode(self, node):
                self.nodes.append(node)

        def isEquals(self, letter):
                return self.letter == letter

        def getDefaultString(self):
                return 'A{0}->{1}'.format(self.parentLevel, self.letter)

        def getPrintedString(self):
                defaultString = self.getDefaultString()
                return '{0}, A{1}'.format(defaultString, self.level) if len(self.nodes)>0 else defaultString
        
        def printed(self):
                if self != self.parent:
                        print(self.getPrintedString())
                if not self.isRecursion:
                        [x.printed() for x in self.nodes]
                
        def __repr__(self):
                return self.getPrintedString()

        def isRules(self):
                return len(self.letter)>1 if self.letter != None else False

        def notUseInRecursion(self):
                return len(self.letter)>1 or len(self.nodes)==0

        def isLastLeaf(self):
                return len(self.letter)==1 and len(self.nodes) ==0

        def getRecursionObject(self, rule):
                if self.notUseInRecursion():
                        return False

                if self.letter == rule.letter[0]:
                        for y in [x for x in self.nodes if x.isLastLeaf()]:
                                if y.letter == rule.letter[1]:
                                        return True
                return False

        def copyObject(self, newNode):
                self.letter = newNode.letter
                self.level = newNode.parentLevel
                self.nodes = newNode.parent.nodes
        

        def updateParentRecursion(self,newNode):
                self.parent.nodes.remove(self)
                for child in self.parent.nodes:
                        for checkNode in newNode.parent.nodes:
                                if checkNode.isEquals(child.letter):
                                        break
                        else:
                                newNode.parent.nodes.append(child)
                                child.parent = newNode.parent
                                child.parentLevel = newNode.parentLevel

                self.parent.copyObject(newNode)
                self.parent.isRecursion = True
                newNode.recursionRepeat.append(self.parent)

        def equalChild(left,right):
                return (left.letter == right.letter) and ((left.level == right.level) or ( (left.level==left.parentLevel)and(right.level==right.parentLevel) ) or ( (left.level==right.parentLevel)and(right.level==left.parentLevel) ))

        def equalsGramma(left,right):
                if len(left.nodes)==0 or (len(left.nodes) != len(right.nodes)):
                        return False

                checkedRight = []
                for leftChild in left.nodes:
                        for rightChild in [rightChild for rightChild in right.nodes if (not rightChild in checkedRight)]:
                                if Gramma.equalChild(leftChild, rightChild):
                                        checkedRight.append(rightChild)
                                        break
                return True if len(checkedRight)==len(right.nodes) else False
                

        def findChildEqual(fixed, children):
                for node in children.nodes:
                        result = Gramma.findEqualGramma(fixed, node)
                        if result != False:
                                return result
                return False

        def findEqualGramma(left, right):
                if right.isRecursion or left.isRecursion:
                        return False
                if (left!=right) and (Gramma.equalsGramma(left, right)):
                        return [left, right]

                result = Gramma.findChildEqual(left,right)
                if result!=False:
                        return result
                if left==right:
                        return False
                result = Gramma.findChildEqual(right,left)
                return result

        def mergeGramma(self, merged):
                mergedNodes = merged.recursionRepeat[:]
                mergedNodes.append(merged)

                for copyNode in mergedNodes:
                        copyNode.nodes = self.nodes
                        copyNode.level = self.level

                merged.isRecursion = True
                merged.recursionRepeat = []
                self.recursionRepeat.extend(mergedNodes)
                
