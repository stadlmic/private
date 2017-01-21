import random
import shutil
import os
import time

rawPath = "rawdata/"
shutil.rmtree("rawdata")
time.sleep(0.1)
if not os.path.exists("rawdata"):
    os.makedirs("rawdata/")
variablesCount = 250
clausesCount = 250
#variablesCount = random.randint(10,10)
#clausesCount = random.randint(10,10)
for cnt in range(0,100):
    f = open(""+rawPath + str(cnt) + ".cnf", 'w')
    f.write('c generated formula for SAT\n')
    f.write('c dummy comment\n')
    f.write('c dummy comment\n')
    f.write("cw ")
    for i in range(0,variablesCount):
        rand = random.randint(1,10)
        f.write(str(rand))
        f.write(" ")
    f.write("\n")


    f.write('p cnf ' + str(variablesCount) + ' ' + str(clausesCount) + '\n')

    for i in range(0,clausesCount):
         numbers = range(-variablesCount + 1, -1) + range(1, variablesCount - 1)
        f.write(str(random.choice(numbers)) + ' ' + str(random.choice(numbers)) + ' ' + str(random.choice(numbers)) + ' 0\n')