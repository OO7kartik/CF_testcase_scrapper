#checks your output matches the expected output

output = open('output.txt', 'r')
answer = open('TestCases.txt', 'r')
result = open('Result.txt', 'w')

i = 0
ans = True

o_line = output.readline()
a_line = answer.readline()

#to complete this white, so that it check both files
while(o_line and a_line):
    while(o_line == '\n'):
        o_line = output.readline()
    while(a_line == '\n'):
        a_line = answer.readline()

    if("case" in o_line  and "case" in a_line):
        if(ans):
            result.write("case #" + str(i) + ": Passed\n\n")
        else:
            result.write("case #" + str(i) + ": --------------------Failed\n\n")
        i+=1
        ans = True
    elif("case" in o_line  or "case" in a_line):
        while(o_line.find("case") == -1):
            o_line = output.readline()
        while(a_line.find("case") == -1):
            a_line = answer.readline()
        ans = False
    else:
        if(o_line != a_line):
            ans = False

    o_line = output.readline()
    a_line = answer.readline()

output.close()
answer.close()
result.close()
