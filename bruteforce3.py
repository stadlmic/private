import copy
import pprint

class permutation:
    totalPrice = 0
    totalWeight = 0
    #values = []
    def __init__(self):
        self.values = []
    def addItemPairExt(self, itemPairs):
        cntP = 0
        cntW = 0
        for line in itemPairs:
            if(line in self.values):
                continue
            self.values.append(line)
            cntP += int(line.price)
            cntW += int(line.weight)
        self.totalPrice += cntP
        self.totalWeight += cntW

class itemPair:
    weight = 0
    price = 0
    def f(self, weight, price ):
        self.weight = weight
        self.price = price

def nicePrint(data):
    print "---Print out---"
    for m in data:
        print ("total weight, price: ")
        print (m.totalWeight, m.totalPrice)
        print ("items dump: ")
        #print m.values.weight, m.values.price
        for l in m.values:
            print l.weight, l.price
            #print l

    print "----------------------------------------------------------"
def loadLine(line):
    parts = line.split()
    id = int(parts[0])
    n = int(parts[1]) #no of items
    M = int(parts[2]) #knapsack capacity

    for i in xrange(3, n*2 + 2,2):
        newItem = itemPair()
        newItem.f(parts[i], parts[i+1])
        dataList.append(newItem)
    print id, n, M
    for j in dataList:
        print j.weight, j.price
    print "-----EOF------"
    return dataList, id, n, M

def combinations(M,cil, data):

    for i in range(len(data)):
        novycil = copy.copy(cil)
        novycil.append(data[i])
        novadata= data[i+1:]
        newRes = permutation()
        newRes.addItemPairExt(novycil)
        if(newRes.totalWeight <= M):
            resData.append(newRes)
        combinations(M,novycil,novadata)

def FindMaxPrice(resData):
    maxPrice = -1

    for i in resData:
        if(i.totalPrice > maxPrice):
            res = i
            maxPrice = i.totalPrice
    return res


data = open("inst/knap_4.inst.dat")
print("bruteforce starting...")
for line in data:
    dataList = []
    resData = [] #pole permutations
    target = []
    dataList, id, n, M = loadLine(line)

    combinations(M,target,dataList)

    result = FindMaxPrice(resData)


    print "Best score"
    nicePrint([result])
    #print  result

    break



