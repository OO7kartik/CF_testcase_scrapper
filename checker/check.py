import subprocess
import time

num_test = 5 #somehow we need to get this

output = open('output.txt', 'a')
testcases = open('TestCases.txt', 'r')
input = open('input.txt', 'w')

i = 1
for line in testcases:
    if(line.find("case") == -1):
        if(line != '\n'):
            input.write(line)
    else:
        input.close()
        if(i > 1):
            subprocess.call(["g++", "test.cpp"])
            print(subprocess.call("./a.exe"))
        input = open('input.txt', 'w')
        input.write(str(i) + '\n')
        # input.write("case #:" + str(i) + '\n')
        i+=1

input.close()
subprocess.call(["g++", "test.cpp"])
print(subprocess.call("./a.exe"))

# for i in range(num_test):
#     #we have to the the first test case
#     #put it in input
#
#     subprocess.call(["g++", "test.cpp"])
#     print(subprocess.call("./a.exe"))
