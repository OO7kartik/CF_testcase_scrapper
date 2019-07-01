import time

testcases = open('TestCases.txt', 'r')
input = open('input.txt', 'w')

num_test = 5
i = 1

for line in testcases:
    if(line.find("case") == -1):
        if(line != '\n'):
            input.write(line)
    else:
        input.close()
        time.sleep(0.5)
        input = open('input.txt', 'w')
        input.write("case #:" + str(i) + '\n')
        i+=1
# for i in range(num_test):
