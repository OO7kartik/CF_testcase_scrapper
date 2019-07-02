import subprocess
import time

testcases = open('TestCases.txt', 'r')
input = open('input.txt', 'w')

i = 0
for line in testcases:
    if(line.find("case") == -1):
        if(line != '\n'):
            input.write(line)
    else:
        input.close()
        if(i > 0):
            output = open('output.txt', 'a')
            output.write("case #" + str(i) + ":" + "\n")
            output.close()
            subprocess.call(["g++", "test.cpp"])
            print(subprocess.call("./a.exe"))
        input = open('input.txt', 'w')
        # input.write("case #" + str(i) + ":" + "\n")
        i+=1

output = open('output.txt', 'a')
output.write("case #" + str(i) + ":" + "\n")
output.close()
input.close()
subprocess.call(["g++", "test.cpp"])
print(subprocess.call("./a.exe"))

# for i in range(num_test):
#     #we have to the the first test case
#     #put it in input
#
#     subprocess.call(["g++", "test.cpp"])
#     print(subprocess.call("./a.exe"))
