#this scrapes the testcases and expected input

import requests as req
import bs4

url = 'https://codeforces.com/problemset/submission/4/2785411'
res = req.get(url)
soup = bs4.BeautifulSoup(res.text, 'html.parser')

file = open('Files/TestCases.txt', 'w')
i = 1
for mydivs in soup.find_all("div", class_ = "file input-view"):
    divs = mydivs.find('div', class_ = "text")
    file.write("case #" + str(i) + ":" + "\n")
    file.write(divs.get_text())
    i+=1
file.close()

file = open('Files/Answers.txt', 'w')
i = 1
for mydivs in soup.find_all("div", class_ = "file answer-view"):
    divs = mydivs.find('div', class_ = "text")
    file.write("case #" + str(i) + ":" + "\n")
    file.write(divs.get_text())
    i+=1
file.close()


#this runs your c++ code
# generates its output and compares the output with the expected one

import subprocess
import time

testcases = open('Files/TestCases.txt', 'r')
input = open('Files/input.txt', 'w')
output = open('Files/output.txt', 'w')
output.close()

#running and coolecting your c++ ouput
i = 0
for line in testcases:
    if(line.find("case") == -1):
        if(line != '\n'):
            input.write(line)
    else:
        input.close()
        if(i > 0):
            output = open('Files/output.txt', 'a')
            output.write("case #" + str(i) + ":" + "\n")
            output.close()
            subprocess.call(["g++", "test.cpp"])
            subprocess.call("./a.exe")
            output = open('Files/output.txt', 'a')
            output.write("\n")
            output.close()
        input = open('Files/input.txt', 'w')
        i+=1

output = open('Files/output.txt', 'a')
output.write("case #" + str(i) + ":" + "\n")
output.close()
input.close()
subprocess.call(["g++", "test.cpp"])
subprocess.call("./a.exe")

#now we have to check if the two files are samne
output = open('Files/output.txt', 'r')
answer = open('Files/Answers.txt', 'r')
result = open('Files/Result.txt', 'w')

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

#check the results file to see how you performed
