#this scrapes the testcases and expected input

import requests as req
import bs4
import subprocess
import time
from threading import Thread

#needed stuff
TimeLimit = 2 #time limit of the problem in seconds
#should ask problem number and automatically crawel and then scrape

class RunCmd(Thread):
    def __init__(self, cmd, timeout):
        Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()
            self.join()
            return True

url = 'https://codeforces.com/problemset/submission/510/9680110'
res = req.get(url)
soup = bs4.BeautifulSoup(res.text, 'html.parser')

file = open('Files/TestCases.txt', 'w')
i = 1
for mydivs in soup.find_all("div", class_ = "file input-view"):
    divs = mydivs.find('div', class_ = "text").get_text()
    file.write("case #" + str(i) + ":" + "\n")
    if(divs[len(divs)-3] == '.'):
        file.write("Long input....\n")
    else:
        file.write(divs)
    i+=1

file = open('Files/Answers.txt', 'w')
i = 1
for mydivs in soup.find_all("div", class_ = "file answer-view"):
    divs = mydivs.find('div', class_ = "text").get_text()
    file.write("case #" + str(i) + ":" + "\n")
    if(divs[len(divs)-3] == '.'):
        file.write("Long input....\n")
    else:
        file.write(divs)
    i+=1
file.close()


#this runs your c++ code
# generates its output and compares the output with the expected one

testcases = open('Files/TestCases.txt', 'r')
input = open('Files/input.txt', 'w')
output = open('Files/output.txt', 'w')
output.close()
results = open('Files/Result.txt','w')
results.write("Grading in process....")
results.close()

#running and coolecting your c++ ouput
i = 0
LongInput = False
for line in testcases:
    if(line == '\n'):
        continue;
    elif(line.find("case") == -1):
        if("Long input...." in line):
            LongInput = True
        else:
            input.write(line)
    else:
        input.close()
        if(i > 0):
            output = open('Files/output.txt', 'a')
            if(LongInput):
                output.write("case #" + str(i) + ":" + "\n")
                output.write("Long input....\n")
                LongInput = False
            else:
                output.write("case #" + str(i) + ":" + "\n")
                output.close()
                subprocess.call(["g++", "test.cpp"])
                problem = RunCmd(["./a.exe"], TimeLimit).Run()
                output = open('Files/output.txt', 'a')
                if(problem):
                    output.write("TLE\n")
                else:
                    output.write("\n")
                output.close()
        input = open('Files/input.txt', 'w')
        i+=1

output = open('Files/output.txt', 'a')
output.write("case #" + str(i) + ":" + "\n")
output.close()
input.close()
subprocess.call(["g++", "test.cpp"])
problem = RunCmd(["./a.exe"], TimeLimit).Run()
output = open('Files/output.txt', 'a')
if(problem):
    output.write("TLE")
output.close()

#now we have to check if the two files are samne
output = open('Files/output.txt', 'r')
answer = open('Files/Answers.txt', 'r')
result = open('Files/Result.txt', 'w')

i = 0
TotalCases = 0
Passed = 0
TimeLimit = 0
Failed = 0
Unjudjed = 0
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
            Passed +=1
            TotalCases += 1
        else:
            result.write("case #" + str(i) + ": ---------Failed---------\n\n")
            Failed += 1
            TotalCases += 1
        i+=1
        ans = True
    elif("case" in o_line  or "case" in a_line):
        while(o_line.find("case") == -1):
            o_line = output.readline()
        while(a_line.find("case") == -1):
            a_line = answer.readline()
        ans = False
    elif(not(o_line.find("Long input....") == -1)):
        result.write("case #" + str(i) + ": >>>>Long input..Skipped\n\n")
        i+=1
        ans = True;
        while(o_line and o_line.find("case") == -1):
            o_line = output.readline()
        while(a_line and a_line.find("case") == -1):
            a_line = answer.readline()
        Unjudjed += 1
    elif(not(o_line.find("TLE") == -1)):
        result.write("case #" + str(i) + ":  ---------TLE---------\n\n")
        i+=1
        ans = True;
        while(o_line and o_line.find("case") == -1):
            o_line = output.readline()
        while(a_line and a_line.find("case") == -1):
            a_line = answer.readline()
        TimeLimit += 1
        TotalCases += 1
    else:
        if(o_line != a_line):
            ans = False

    o_line = output.readline()
    a_line = answer.readline()

output.close()
answer.close()
result.close()

line = "AC: "+str(Passed)+"\nWA: "+str(Failed)+"\nTLE: "+str(TimeLimit)+"\nTotalCases: "+str(TotalCases)+"\n\nUnjudged due to long input:"+str(Unjudjed)+"\n\n\n" + "-----------------------------------------------------DETAILS---------------------------------------------------------------------\n\n\n"
#to write this at the start of result.txt
with open('Files/Result.txt', 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(line + '\n' + content)


#check the results file to see how you performed
