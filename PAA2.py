import copy
import time
import math
from ctypes.macholib.dylib import DYLIB_RE


class permutation:
    totalPrice = 0
    totalWeight = 0
    #values = []
    def __init__(self):
        self.values = []
        self.usedValues = []
    def addItemPairExt(self, itemPairs):
        cntP = 0
        cntW = 0
        for i, line in enumerate(itemPairs):
            self.values.append(line)
            self.usedValues.append(line.placement)
            cntP += int(line.price)
            cntW += int(line.weight)
        self.totalPrice += cntP
        self.totalWeight += cntW

class itemPair:
    weight = 0
    price = 0
    ratio = 0.0
    placement = -1
    def f(self, weight, price, placement ):
        self.weight = weight
        self.price = price
        self.ratio = float(price)/float(weight)
        self.placement = placement

def nicePrint(data):
    print "---Print out---"
    for m in data:
        print ("total weight, price: ")
        print (m.totalWeight, m.totalPrice)
        print m.usedValues
        print ("items dump: (weight, price, ration, placement)")
        #print m.values.weight, m.values.price
        for l in m.values:
            print l.weight, l.price, l.ratio, l.placement
            #print l

    print "----------------------------------------------------------"
def loadLine(line):
    parts = line.split()
    id = int(parts[0])
    n = int(parts[1]) #no of items
    M = int(parts[2]) #knapsack capacity

    for i in xrange(3, n*2 + 2,2):
        newItem = itemPair()
        newItem.f(parts[i], parts[i+1], (i-3)/2)
        dataList.append(newItem)
    #print id, n, M
    #for j in dataList:
    #    print j.weight, j.price
    #print "-----EOF------"
    return dataList, id, n, M

def loadLineRes(line):
    parts = line.split()
    id = int(parts[0])
    n = int(parts[1]) #no of items
    P = int(parts[2]) #price
    return dataList, id, n, P


def combinationsBnB(M,cil, data):
    global maxPrice
    for i in range(len(data)):
        novycil = copy.copy(cil)
        novycil.append(data[i])
        novadata= data[i+1:]
        newRes = permutation()
        newRes.addItemPairExt(novycil)
        if(newRes.totalWeight <= M and newRes.totalPrice  + sum(int(c.price) for c in novadata) > maxPrice):
            resData.append(newRes)
            if(newRes.totalPrice > maxPrice):
                maxPrice =  newRes.totalPrice
            combinationsBnB(M,novycil,novadata)


def Heuristics(M, data):
    newRes = permutation()
    newlist = sorted(data, key=lambda data: data.ratio, reverse=True)
    for a in newlist:
        if(newRes.totalWeight + int(a.weight)<= M):
            newRes.addItemPairExt([a])
        else:
            continue
    return newRes

def FindMaxPrice(resData):
    maxPrice = -1
    res = -1

    for i in resData:
        #print i.totalPrice
        if(i.totalPrice > maxPrice):
            res = i
            maxPrice = i.totalPrice
    return res

def printMatrix(matrix):
    for i in matrix:
        print i

def DynamicProgramming(dataList, n, M):
    matrix = [[0 for x in range(M+1)] for y in range(n+1)]
    for i in range(n + 1):
        for w in range(M + 1):
            if (i == 0 or w == 0):
                matrix[i][w] = 0
            elif (int(dataList[i - 1].weight) <= w):
                matrix[i][w] = max(int(dataList[i - 1].price) + matrix[i - 1][w - int(dataList[i - 1].weight)], matrix[i - 1][w])
            else:
                matrix[i][w] = matrix[i - 1][w]

    return matrix[n][M]

def FPTAS(dataList, n, M, scaling_factor=4):
    new_M = int(float(M) / scaling_factor)

    newDataList = []  # pode itemPair
    for b in dataList:
        newItem = itemPair()
        newItem.f(round(float(b.weight) / scaling_factor) + 1, b.price, 0)
        newDataList.append(newItem)

    return DynamicProgramming( newDataList, n, new_M)

#dataFILE = 40
dataFILEarr = {4,10,15,20,22,25,30,32,35,37,40}
for a in dataFILEarr:
    data = open("inst/knap_"+str(a)+".inst.dat")
    f = open("sol/knap_"+str(a)+".sol.dat")
    refResLines=f.readlines()
    #print("bruteforce starting...")
    relErrors = []
    start = time.time()
    maxPrice = 0
    for i in range(0, 1):
        for i, line in enumerate(data):
            dataList = [] #pode itemPair
            resData = [] #pole permutations
            target = []
            dummy, idRes, nRes, PRes = loadLineRes(refResLines[i])
            dataList, id, n, M = loadLine(line)

            #resultHeuristics = Heuristics(M, dataList)

            #combinationsBnB(M,target,dataList)
            #result = FindMaxPrice(resData)

            #resultDynamic = DynamicProgramming(dataList, n, M)

            resultFPTAS = FPTAS(dataList, n, M)
            #nicePrint([result])



            #if(resultFPTAS == PRes):
            #    print "result " + str(id) + " OK "
            #else:
            #    print "result " + str(id) + " not optimal "

                #nicePrint([resultHeuristics])
                #nicePrint([result])
            relErrors.append(abs(resultFPTAS-PRes)/float(PRes))

            #print refResLines[i]
            #print "Best score"
            #nicePrint([result])
            #print  result
            maxPrice = 0


    print "Data file N = " + str(a)
    #print "finished"
    end = time.time()
    print "Time: " + str(end - start)
    print "Rel error: " + str(sum(relErrors)/50)
    print "Max Rel error: " + str(max(relErrors))
    print "-------------"
    relErrors = []