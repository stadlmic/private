import copy
import time
import math
import random

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
    ratio = 0.0
    def f(self, weight, price ):
        self.weight = weight
        self.price = price
        self.ratio = float(price)/float(weight)

def nicePrint(data):
    print "---Print out---"
    for m in data:
        print ("total weight, price: ")
        print (m.totalWeight, m.totalPrice)
        print ("items dump: ")
        #print m.values.weight, m.values.price
        for l in m.values:
            print l.weight, l.price, l.ratio
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

    for i in resData:
        if(i.totalPrice > maxPrice):
            res = i
            maxPrice = i.totalPrice
    return res


def annealing_algorithm(n, M, dataList, init_temp=100, steps=50):
    start_sol = init_solution(dataList, M)
    best_price, solution = simulate(start_sol, dataList, M, init_temp, steps)
    best_combination = [0] * n
    for idx in solution:
        best_combination[idx] = 1
    return best_price, best_combination


def init_solution(dataList, max_weight):
    solution = []
    allowed_positions = range(len(dataList))
    while len(allowed_positions) > 0:
        idx = random.randint(0, len(allowed_positions) - 1)
        selected_position = allowed_positions.pop(idx)
        if fitness(solution + [selected_position], dataList).weight <= max_weight:
            solution.append(selected_position)
        else:
            break
    return solution


def fitness(solution, dataList):
    newItem = itemPair()
    price, weight = 0, 0
    for item in solution:
        weight += int(dataList[item].weight)
        price += int(dataList[item].price)
        newItem.f(weight, price)
    return newItem


def moveto(solution, dataList, max_weight):
    moves = []
    for i, _ in enumerate(dataList):
        if i not in solution:
            move = solution[:]
            move.append(i)
            if fitness(move, dataList).weight <= max_weight:
                moves.append(move)
    for i, _ in enumerate(solution):
        move = solution[:]
        del move[i]
        if move not in moves:
            moves.append(move)
    return moves


def simulate(solution, dataList, max_weight, init_temp, steps):
    temperature = init_temp

    best = solution
    best_price = fitness(solution, dataList).price

    current_sol = solution
    while True:
        current_price = fitness(best, dataList).price
        for i in range(0, steps):
            moves = moveto(current_sol, dataList, max_weight)
            idx = random.randint(0, len(moves) - 1)
            random_move = moves[idx]
            delta = fitness(random_move, dataList).price - best_price
            if delta > 0:
                best = random_move
                best_price = fitness(best, dataList).price
                current_sol = random_move
            else:
                if math.exp(delta / float(temperature)) > random.random():
                    current_sol = random_move

        temperature *= ALPHA
        if current_price >= best_price or temperature <= 0:
            break
    return best_price, best

for a in range(1,11,1):
    ALPHA = a / 10.0
    dataFILE = 40
    data = open("inst/knap_" + str(dataFILE) + ".inst.dat")
    f = open("sol/knap_" + str(dataFILE) + ".sol.dat")
    refResLines = f.readlines()
    print("-----")
    relErrors = []
    start = time.time()
    print "alpha is " + str(ALPHA)
    for i, line in enumerate(data):
        #print "--------"

        dataList = []
        resData = [] #pole permutations
        target = []
        dummy, idRes, nRes, PRes = loadLineRes(refResLines[i])
        dataList, id, n, M = loadLine(line)

        #combinations(M,target,dataList)
        #result = FindMaxPrice(resData)

        #resultHeuristics = Heuristics(M, dataList)
        resultSA = annealing_algorithm(n, M, dataList)
        #print(resultSA[0])
        #nicePrint([resultHeuristics])

        """
        if(PRes == resultHeuristics.totalPrice):
            print "result " + str(id) + " OK "
        else:
            print "result " + str(id) + " not optimal "
            #nicePrint([resultHeuristics])
            #nicePrint([result])
            relErrors.append(abs(resultHeuristics.totalPrice-PRes)/float(PRes))
        """
        """
        if(PRes == resultSA[0]):
            print "result " + str(id) + " OK "
        else:
            print "result " + str(id) + " not optimal "
            #nicePrint([resultHeuristics])
            #nicePrint([result])
            relErrors.append(abs(resultSA[0]-PRes)/float(PRes))
        """
        relErrors.append(abs(resultSA[0] - PRes) / float(PRes))
        #print "PRes " + str(PRes)
        #print "Best score"
        #nicePrint([result])
        #print  resultSA[0]

    print "max err " + str(max(relErrors))
    print "rel err " + str(sum(relErrors)/50)
    end = time.time()
    print "finished in time " + str(end - start)





