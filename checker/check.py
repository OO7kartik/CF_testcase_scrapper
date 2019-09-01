#this scrapes the testcases and expected input

from tkinter import *
from tkinter import simpledialog
import requests as req
import bs4
import subprocess
import time
from threading import Thread
from time import sleep

extension = ".out"

def get_input():
    get_input.ProblemId = simpledialog.askstring("Problem Id", "Enter the Problem id: ")
    #get_input.TimeLimit = simpledialog.askinteger("Time Limit", "Enter time limit per test: ")
    get_input.file_to_test = simpledialog.askstring("file_to_test", "Submit file name:  ")
    Label(root, text="ProblemId: "+str(get_input.ProblemId)).pack()
    #Label(root, text="TimeLimit: "+str(get_input.TimeLimit)).pack()
    root.destroy()

root = Tk()

theLabel = Label(root, text="Problem Details").pack()
button = Button(root, text="Click Here To Enter", command = get_input, fg="red").pack()
positionRight = int(root.winfo_screenwidth()/2 - 100)
positionDown = int(root.winfo_screenheight()/2 - 100)
root.geometry("200x200+{}+{}".format(positionRight, positionDown))
root.mainloop()


ProblemId = get_input.ProblemId
    TimeLimit = 10
    file_to_test = get_input.file_to_test

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

root = Tk()
retData = Label(root, text="Retrieving data...").pack()
root.after(2000, root.destroy)
root.mainloop()

tempUrl = 'https://codeforces.com/problemset/status/' + str(ProblemId[:-1]) + '/problem/' + str(ProblemId[-1].upper())
tempRes = req.get(tempUrl)
tempSoup = bs4.BeautifulSoup(tempRes.text, 'html.parser')
for a in tempSoup.findAll('a', href=True):
    if '/problemset/submission/' in a['href']:
        url = 'https://codeforces.com/'+a["href"]
        break;
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
root = Tk()
retData = Label(root, text="Running your program on all testcases.... (around 10s-30s)").pack()
root.after(2000, root.destroy)
root.mainloop()

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
                subprocess.call(["g++", file_to_test])
                problem = RunCmd(["./a"+extension], TimeLimit).Run()
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
subprocess.call(["g++", file_to_test])
problem = RunCmd(["./a"+extension], TimeLimit).Run()
output = open('Files/output.txt', 'a')
if(problem):
    output.write("TLE")
output.close()

#now we have to check if the two files are samne
output = open('Files/output.txt', 'r')
answer = open('Files/Answers.txt', 'r')
result = open('Files/Result.txt', 'w')

root = Tk()
retData = Label(root, text="Generating your grade......").pack()
root.after(2000, root.destroy)
root.mainloop()

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

line = "AC: "+str(Passed)+"\nWA: "+str(Failed)+"\nTLE: "+str(TimeLimit)+"\nTotalCases: "+str(TotalCases)+"\n\nUnjudged due to long input:"+str(Unjudjed)+"\n\n\n" + "--------------------DETAILS--------------------\n\n"
#to write this at the start of result.txt
with open('Files/Result.txt', 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(line + '\n' + content)

root = Tk()
retData = Label(root, text="Results declared! Good luck!").pack()
root.after(1000, root.destroy)
root.mainloop()
# print("Results declared! Good luck!\n\n")
# print("AC: "+str(Passed)+"\nWA: "+str(Failed)+"\nTLE: "+str(TimeLimit)+"\nTotalCases: "+str(TotalCases)+"\n\nUnjudged due to long input:"+str(Unjudjed))

def quit():
    root.destroy()
    exit()

ShowDetails = False
def details():
    global ShowDetails
    ShowDetails = True
    root.destroy()

root = Tk()
resDisplay = Label(root, text="AC: "+str(Passed)+"\nWA: "+str(Failed)+"\nTLE: "+str(TimeLimit)+"\nTotalCases: "+str(TotalCases)+"\n\nUnjudged due to long input:"+str(Unjudjed)).pack()
button1 = Button(root, text="Get Details", command=details, bg="green").pack()
button2 = Button(root, text="Exit", command=quit, fg="green", bg="red").pack()
root.geometry("200x200")
root.mainloop()

if(not ShowDetails):
    exit()

root = Tk()

with open('Files/Result.txt', 'r') as file:
    data = file.read()

S = Scrollbar(root)
T = Text(root, height=30, width=50)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
T.config(yscrollcommand=S.set)
T.insert(END, data)
root.mainloop()
