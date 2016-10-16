"""

def combinations(target,data):
    for i in range(len(data)):
        new_target = copy.copy(target)

        new_target.append(data[i])
        new_data = data[i+1:]
        print new_target
        combinations(new_target,new_data)

target = []
data = ['a','b','c','d']
combinations(target,data)


"""
import copy
def combinations(cil, data):
    for i in range(len(data)):

        novycil = copy.copy(cil)
        novycil.append(data[i])
        novadata= data[i+1:]
        print novycil
        combinations(novycil,novadata)

"""
        cil = data[:i] + data[i+1:]

        if(not cil):
            continue
        print cil
        combinations(cil)

"""
target = []
data = ['a','b','c','d','e']
combinations(target, data)
-------------------------------------


import copy
import pprint


class permutation:
    totalPrice = 0
    #values = []
    def __init__(self):
        self.values = []
    def addValues(self, values, totalPrice):
        self.values = values
        self.totalPrice = totalPrice
    def addItemPair(self, itemPair):
        self.values .append( itemPair)
        self.totalPrice += int(itemPair.price)
    def addItemPairExt(self, itemPairs):
        cnt = 0
        for line in itemPairs:
            if(line in self.values):
                continue
            self.values.append(line)
            cnt += int(line.price)


        #self.values .extend( itemPair)

        self.totalPrice += cnt

class itemPair:
    weight = 0
    price = 0
    def f(self, weight, price ):
        self.weight = weight
        self.price = price

def nicePrint(data):
    print "---Print out---"
    for m in data:
        print ("total price: ")
        print (m.totalPrice)
        print ("values: ")
        #print m.values.weight, m.values.price
        for l in m.values:
            print l.weight, l.price
            #print l

    print "----------------------------------------------------------"
def loadLine():
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
    return dataList

"""
def combinations(target, data):
    for a,k in enumerate(data): #itemPair type

        newRes = permutation()
        newRes.addItemPair(k)

        resData.append(newRes)
        lastRes .append(newRes.values[0])

        for b,l in enumerate(data):
            #if(a == b):
            #    continue
            newRes = permutation()
            newRes.addItemPair(l)
            newRes.addItemPairExt(lastRes)
            resData.append(newRes)

"""
def combinations(cil, data):
    for i in range(len(data)):

        novycil = copy.copy(cil)
        novycil.append(data[i])
        novadata= data[i+1:]
        #print novycil
        newRes = permutation()
        #newRes.addItemPair(novycil[0])

        newRes.addItemPairExt(novycil)
        resData.append(newRes)
        combinations(novycil,novadata)








data = open("inst/knap_4.inst.dat")
print("bruteforce starting...")
for line in data:
    dataList = []
    resData = [] #pole permutations
    lastRes = []
    target = []
    loadLine()

    combinations(target,dataList)



    nicePrint(resData)
    break



