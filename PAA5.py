import copy
import time
import math
import random
import ast
from symbol import for_stmt

validFound = 0
#holds individual clauses
class clause:
    f = 0
    s = 0
    t = 0
    def __init__(self, f, s, t):
        self.f = f
        self.s = s
        self.t = t
    def f(self, f, s, t):
        self.f = f
        self.s = s
        self.t = t

#holds whole formula + formula related methods
class Formula:
    n = 0
    c = 0
    id = 0
    variablesCount = 0
    clausesCount = 0
    def __init__(self, id, clauses, weights):
        self.clauses = clauses #pole itemFormula #ekvivalent itemPair
        self.weights = weights
        self.id = id
        self.variablesCount = len(weights)
        self.clausesCount = len(clauses)
    def totalWeight(self):
        totalWeight = 0
        for i in self.weights:
            totalWeight += int(i)
        return totalWeight

    def computeSatisfiedClauses(self, solution):
        satisfiedClauses = 0
        for i in self.clauses:
            if ((int(i.f) in solution) and (int(i.f) > 0)) or ((-int(i.f) not in solution) and (int(i.f) < 0)):
                satisfiedClauses += 1
                continue
            if ((int(i.s) in solution) and (int(i.s) > 0)) or ((-int(i.s) not in solution) and (int(i.s) < 0)):
                satisfiedClauses += 1
                continue
            if ((int(i.t) in solution) and (int(i.t) > 0)) or ((-int(i.t) not in solution) and (int(i.t) < 0)):
                satisfiedClauses += 1
                continue
        return satisfiedClauses

    def computeWeightSolution(self, solution):
        weight = 0
        for i in solution:
            weight += int(self.weights[i-1])
        return weight

    def printFormula(self):
        print "clauses: "
        for i in self.clauses:
            print i.f, i.s, i.t
        print "weights: "
        print self.weights

    def validSoluton(self, solution):
        if(self.computeSatisfiedClauses(solution) == self.clausesCount):
            return 1
        return 0

#file loader
def loadMultine(f):
    variablesCount, clausesCount = 0,0
    l_weights = []
    l_dataList = []
    data = open(f)
    for i, line in enumerate(data):
        parts = line.split()
        if(line[0]=="c" and line[1]=="w"): #weights
            for j in xrange(1, len(parts), 1):
                 l_weights.append(parts[j])
        if(line[0]=="c"):
            continue #comment
        if(line[0]=="p"):
            variablesCount = int(parts[2])  # no of variables
            clausesCount = int(parts[3])  # no of clauses
            continue #comment
        newItem = clause(parts[0], parts[1], parts[2])
        l_dataList.append(newItem)

    if(variablesCount != len(l_weights) or clausesCount != len(l_dataList)):
        print "problem"
        exit -1
    return Formula(id, l_dataList, l_weights)

#AA main func
def annealing_algorithm(formula, init_temp=100, steps=100):
    start_sol, start_satisfiedClauses = init_solution(formula)
    best_price, solution = simulate(start_sol, formula, init_temp, steps)
    n = formula.variablesCount
    best_combination = [0] * n
    for idx in solution:
        best_combination[idx-1] = 1
        if(idx<0):
            print "!!!!!!!problem idx " + str(idx)
            exit -1
    return best_price, best_combination, solution

#starting random solution
def init_solution(formula):
    solution = []
    rand = random.randint(0, formula.variablesCount-1 ) #allowed_positions
    solution.append(rand)
    satisfiedClauses = formula.computeSatisfiedClauses(solution)
    return solution, satisfiedClauses

#calculate fitnes
def fitness(solution, formula):
    satisfiedClauses = formula.computeSatisfiedClauses( solution) + 0.0
    clausesCount = formula.clausesCount + 0.0
    fitness =  formula.computeWeightSolution(solution) * math.pow(satisfiedClauses / clausesCount,4 )
    valid = formula.validSoluton(solution)
    if(valid):
        #print "valid solution found"
        global validFound
        validFound = 1
        fitness *= 2
    return fitness

#generate possible moves
def moveto(solution, formula):
    moves = []
    for i, _ in enumerate(formula.weights):
        if i not in solution:
            move = solution[:]
            if(move < 0 and move >= Formula.variablesCount):
                print "001 nemelo by nastat"
                exit -1
            moves.append(move)
            move.append(i)
            #if fitness(move, dataList).weight <= max_weight:
    for i, _ in enumerate(solution):
        move = solution[:]
        del move[i]
        if move not in moves:
            if(move < 0 and move >= Formula.variablesCount):
                print "002 nemelo by nastat"
                exit -1
            moves.append(move)
    return moves

#start simulation
def simulate(solution, formula, init_temp, steps):
    temperature = init_temp
    best = solution
    best_price = fitness(solution, formula)
    current_sol = solution
    while True:
        current_price = fitness(best, formula)
        for i in range(0, steps):
            moves = moveto(current_sol, formula)
            idx = random.randint(0, len(moves) - 1)
            random_move = moves[idx]
            delta = fitness(random_move, formula) - best_price
            if delta > 0:
                best = random_move
                best_price = fitness(best, formula)
                current_sol = random_move
            else:
                if math.exp(delta / float(temperature)) > random.random():
                    current_sol = random_move
        temperature *= ALPHA
        if current_price >= best_price or temperature <= 0:
            break
    return best_price, best

#main
for a in range(0,30,1):
    #ALPHA = a / 10.0
    ALPHA = 0.2
    #print "ALPHA"
    #print  ALPHA
    result = []
    resultValid = []
    timeValid = []
    timeNotValid = []
    bestPrice = 0
    bestSolution = []
    bestCombination = []
    for n in range(0, 10):
        #start = time.time()

        #print("-----")
        #print "alpha is " + str(ALPHA)
        #print "round " + str(n)
        b = loadMultine("rawdata/"+str(a)+".cnf")

        #b.printFormula()

        price, best_combination, sol = annealing_algorithm(b)
        valid = b.validSoluton(sol)
        if(bestPrice < price):
            bestPrice = price
            bestSolution = sol
            bestCombination = best_combination

        #print "-------------------"
        #print "valid"
        #resultValid.append(valid)
        if(validFound != valid):
            "CAUTION valid solution found but fitness is not high enough"
        #print "price"
        #result.append(b.computeWeightSolution(sol))
        #print best_combination
        #print "max err " + str(max(relErrors))
        #print "rel err " + str(sum(relErrors)/50)
        #end = time.time()
        #if(valid):
        #    timeValid.append((end - start))
        #else:
        #    timeNotValid.append((end - start))
    print "file " + str(a) +".cnf"
    print "bestCombination:"
    print bestCombination
    print "computeWeightSolution: " + str(b.computeWeightSolution(bestSolution))
    print "is valid: " + str(b.validSoluton(sol))
    print "------"
    #print resultValid
    #print "timeValid.count()"
    #if(len(timeValid) ==0):
    #    timeValid.append(0)
    #if(len(timeNotValid) == 0):
    #    timeNotValid.append(0)
    #print sum(timeValid) / len(timeValid)
    #print "timeNotValid.count()"
    #print sum(timeNotValid) / len(timeNotValid)
    #print "finished in time " + str(end - start)





