#!/usr/bin/env python
#Filename:sudoku.py

"""Sudoku solver- by Aditya Gopalakrishnan.You can either run it as a script to enter a valid sudoku puzzle and view the solution."""

TupleOfVals=('1','2','3','4','5','6','7','8','9','b')                    #for getInput()
TupleOfRowIds=('1st','2nd','3rd','4th','5th','6th','7th','8th','9th') 

def getInput():
    """Gets input for the grid and returns a list with blanks replaced by a

    list of all values which it can have"""
    b=1
    f=open('sudoku.puzzle','r')
    ListFromFile=delNewline(f.readlines())
    a=[]
    i=0
    while i<9:        
        string=ListFromFile[i]
        if (len(string)==9) and checkSim(string,TupleOfVals):
            a.extend(string)
            replaceListItem(a,'b')
            i+=1
        else:
            b=0
            print "Error in ",TupleOfRowIds[i],"row."
            break
    if b==0:
        return 0
    if checkGrid(a):
        return a
    else:
        print "The sudoku puzzle is not valid."
        return 0
    
    
def delNewline(List):
    """Deletes the trailing newline from each of the lines extracted from the file sudoku.puzzle""" 

    spare=List
    for i in range(len(spare)):
        List[i]=(spare[i])[:9]
    return List


def checkSim(string,List):
    """checks if string is made up of only elements in List"""
    
    flag="ON"
    for i in string:
        if (i=='b' or string.count(i)<2) and i in List:
            pass
        else:
            flag="OFF"
            break
    if flag=="ON":
        return True
    else:
        return False

def replaceListItem(List,par1):

    for i in List[:]:
        if i==par1:
            List[List.index(i)]=['1','2','3','4','5','6','7','8','9']
        else:
            pass


def removeString(Grid,index,string):
    """Removes all occurences of string from grid"""
    
    copy=Grid[:]
    ListOfIndices=idInGrid(index)
    for z in ListOfIndices:
        List=doSet(copy[:],z[1],z[0])
        ListOfLists=[]
        for i in range(len(List[:])):
            if type(List[i])==type([]):
                a=List[i]
                a.append(i)
                ListOfLists.append(a)
        for i in range(len(ListOfLists[:])):
            if string in ListOfLists[:][i]:
                (ListOfLists[i]).remove(string)
            x=ListOfLists[i].pop()
            List[x]=ListOfLists[i]
        updateGrid(copy,List,z[1],z[0])
    return copy
        
        
def removeValues(Grid,index,char):
    """Basically clears up the set denoted by index and char in grid"""
    
    List=doSet(Grid[:],index,char)
    copy=Grid[:]
    ListOfConfirmed=[]
    ListOfDoubtfuls=[]
    for i in range(len(List[:])):
        if type(List[i])==type(""):
            ListOfConfirmed.append(List[:][i])
        else:
            a=List[:][i]
            a.append(i)
            ListOfDoubtfuls.append(a)
    for i in range(len(ListOfDoubtfuls[:])):
        for any in ListOfConfirmed:        
            if any in ListOfDoubtfuls[:][i]:
                (ListOfDoubtfuls[i]).remove(any)
        x=ListOfDoubtfuls[i].pop()
        List[x]=ListOfDoubtfuls[i]
        updateGrid(copy,List,index,char)    
    return copy

def returnIndex(Grid,val,index,char):
    
    if char=='r':
        indexList=rowIndexes[index]
    elif char=='c':
        indexList=columnIndexes[index]
    elif char=='s':
        indexList=squareIndexes[index] 
    valList=[Grid[z] for z in indexList]
    b=valList.index(val)
    return indexList[b]
    

def changer(Grid,index,char):
    List=doSet(Grid[:],index,char)
    copy=Grid[:]
    updateVals=[]
    for i in range(len(List)):
        if type(List[i])==type([]) and len(List[i])==1:
            List[i]=(List[i][:])[0]
            updateVals.append(List[i])
    updateGrid(copy,List,index,char)
    for any in updateVals:
        absInd=returnIndex(copy[:],any,index,char)
        copy=removeString(copy,absInd,any)
    return copy


def checkForObvious(Grid,index,char,refList):         
    List=doSet(Grid[:],index,char)
    copy=Grid[:]
    updateVals=[]
    countList=[]
    for i in range(len(refList)):
        countList.append(['','',''])
        (countList[len(countList)-1])[:2]=[refList[i],0]
    for i in range(len(refList)):
        for j in range(len(List)):
            if refList[i] in List[j]:
                (countList[i])[1:]=[(countList[i])[1]+1,j]
    for i in range(len(countList)):
        if (countList[i])[1]==1:
            List[(countList[i])[2]]=(countList[i])[0]
            updateVals.append(List[(countList[i])[2]])
    updateGrid(copy,List,index,char)
    for any in updateVals:
        absInd=returnIndex(copy,any,index,char)
        copy=removeString(copy,absInd,any)
    return copy
    
def idInGrid(index):
    belongList=[['r'],['c'],['s']]
    ListOfILists=[rowIndexes,columnIndexes,squareIndexes]
    for i in range(3):
        for j in range(9):
            if index in (ListOfILists[i])[j]:
                belongList[i].append(j)
                breaker=False
                break
        if breaker:
            continue
    belongList=[tuple(i) for i in belongList]
    return belongList

def updateGrid(a,List,index,char):
    indexList=[]
    if char=='r':
        indexList=rowIndexes[index]
    if char=='c':
        indexList=columnIndexes[index]
    if char=='s':
        indexList=squareIndexes[index]
    for i in range(len(indexList)):
        a[indexList[i]]=List[i]

def resolveList(Grid,index,char):
    return changer(checkForObvious(removeValues(Grid[:],index,char),index,char,('1','2','3','4','5','6','7','8','9')),index,char)

def doSet(Grid,index,char):
    b=[[]]
    i=0
    if char=='r':        
        while i<9:
            for x in range(9*i,9*i+9):
                b[i].append(Grid[x])
            i+=1
            b.append([])
    elif char=='c':
        while i<9:
            for x in range(i,81,9):
                b[i].append(Grid[x])
            i+=1
            b.append([])
    elif char=='s':
        j=k=0
        while i<9:
            j=0
            while j<3:
                k=0
                while k<3:
                    b[i].append(Grid[(i/3)*27+(i%3)*3+9*j+k])
                    k+=1
                j+=1
            i+=1
            b.append([])
    b.pop()
    return b[index]    

rowIndexes=[]
columnIndexes=[]
squareIndexes=[]

for i in range(9):
    rowIndexes.append([])
    columnIndexes.append([])
    squareIndexes.append([])
    rowIndexes[i]=doSet(range(81),i,'r')
    columnIndexes[i]=doSet(range(81),i,'c')
    squareIndexes[i]=doSet(range(81),i,'s')

rowIndexes=tuple(rowIndexes)
columnIndexes=tuple(columnIndexes)
squareIndexes=tuple(squareIndexes)

def findSmallestList(List):
    """Returns index of smallest Iterable."""
    
    freqs=[List.count(i) for i in List]
    min=freqs[0]
    for any in freqs:
        if any>1 and min>any:
            min=any
        else:
            pass
    return freqs.index(min)

def checkVal(Set):
    b=True
    ListOfChars=[]
    ListOfAll=[]
    for any in Set[:]:
        if type(any)==type(""):
            ListOfChars.append(any)
        elif type(any)==type([]):
            ListOfAll.extend(any)
    for i in TupleOfVals[:9]:
        if ListOfAll.count(i)>0 and (ListOfChars.count(i) in [1,0]):
            pass
        else:
            b=False
            break
    return b

def checkGrid(Grid):
    b=True
    for char in 'rcs':
        for i in range(9):
            if checkVal(doSet(Grid,i,char)):
                pass
            else:
                b=False
                break
        if b==False:
            break
    return b                               

def checkForList(Grid):
    b=True
    for i in Grid:
        if type(i)==type([]):
            b=False
            break
        else:
            pass            
    return b


def resolveGrid(Grid,index=None):
    q=Grid[:]
    breaker='y'
    if index is None:
        b=[]
        while q!=b:
            b=q[:]
            copy=q[:]
            for x in ['r','c','s']:
                for i in range(9):
                    copy=resolveList(copy[:],i,x)
                    if checkGrid(copy):
                        breaker='n'
                        break
                if breaker=='n':
                    break
            if breaker=='n':
                break
            q=copy
        if checkForList(Grid):
            return [q,breaker]
        else:
            return resolveGrid(q,findSmallestList(q))
    else:
        for i in range(len(q[index])):
            c=q[:]
            c[index]=(c[:][index])[i]
            blah=resolveGrid(c)
            if blah[1]=='y' and checkForList(blah[0]):
                break
        return blah

        
def main():
    a=getInput()
    if a==0:
        return 0
    a=resolveGrid(a)[0]
    for i in range(9):
        print ' '.join(a[9*i:9*i+9])
    print 'Solved'
        
main()












