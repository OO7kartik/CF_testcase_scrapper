#this scrapes the testcases and expected input

from tkinter import *
from tkinter import simpledialog
import requests as req
import bs4
import subprocess
import time
from threading import Thread
from time import sleep
import os
import filecmp
from shutil import rmtree as rmt
import errno
import stat

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
      func(path)
  else:
      raise

def areFilesEqual(file1, file2):
    f1 = open(file1).read().splitlines()
    f2 = open(file2).read().splitlines()

    print(f1)
    print(f2)

    if(len(f1) != len(f2)):
        return False
    else:
        for (l1, l2) in zip(f1, f2):
            if(l1.rstrip() != l2.rstrip()):
                return False
    return True

if(os.path.exists('Files/Info/answers')):
    rmt('Files/Info/answers', ignore_errors=False, onerror=handleRemoveReadonly)
if(os.path.exists('Files/Info/FailOp')):
    rmt('Files/Info/FailOp', ignore_errors=False, onerror=handleRemoveReadonly)

if(os.path.exists('Files/Info')):
    rmt('Files/Info', ignore_errors=False, onerror=handleRemoveReadonly)
os.mkdir('Files/Info')
os.mkdir('Files/Info/answers')
os.mkdir('Files/Info/FailOp')

def get_input():
    get_input.ProblemId = simpledialog.askstring("Problem Id", "Enter the Problem id: ")
    get_input.TimeLimit = simpledialog.askinteger("Time Limit", "Enter time limit per test: ")
    Label(root, text="ProblemId: "+str(get_input.ProblemId)).pack()
    Label(root, text="TimeLimit: "+str(get_input.TimeLimit)).pack()
    root.destroy()

root = Tk()

theLabel = Label(root, text="Problem Details").pack()
button = Button(root, text="Click Here To Enter", command = get_input, fg="red").pack()
positionRight = int(root.winfo_screenwidth()/2 - 100)
positionDown = int(root.winfo_screenheight()/2 - 100)
root.geometry("200x200+{}+{}".format(positionRight, positionDown))
root.mainloop()


ProblemId = get_input.ProblemId
TimeLimit = get_input.TimeLimit

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

        #for TlE, have to fix this
        # if self.is_alive():
        #     self.p.terminate()
        #     self.join()
        #     return True

# root = Tk()
# retData = Label(root, text="Retrieving data...").pack()
# root.after(2000, root.destroy)
# root.mainloop()

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
file.write("case #" + "over"+ ":" + "\n")

file = open('Files/Answers.txt', 'w')
i = 1
for mydivs in soup.find_all("div", class_ = "file answer-view"):
    divs = mydivs.find('div', class_ = "text").get_text()
    file.write("case #" + str(i) + ":" + "\n")
    if(divs[len(divs)-3] == '.'):
        file.write("Long input....\n")
    else:
        f = open('Files/Info/answers/ans{}.txt'.format(i), 'w')
        f.write(divs)
        f.close()
        file.write(divs)
    i+=1
file.close()


#this runs your c++ code
# generates its output and compares the output with the expected one
# root = Tk()
# retData = Label(root, text="Running your program on all testcases.... (around 10s-30s)").pack()
# root.after(2000, root.destroy)
# root.mainloop()

testcases = open('Files/TestCases.txt', 'r')
results = open('Files/Result.txt', 'w')
results.close()

i = 1
TotalCases = 0
Passed = 0
TimeLimit = 0
Failed = 0
Unjudjed = 0
ans = True
t_line = testcases.readline()
t_line = testcases.readline()


#the problem is the second time we call subprocess, it fails.
#lets do this lets find this out.....
while(t_line):
    while(t_line == '\n'):
        t_line = testcases.readline()
    if(t_line.find("case") != -1): #means we find case
        st = time.time()
        subprocess.call(["g++", "../test.cpp"])
        problem = RunCmd(["./a.exe"], TimeLimit).Run()
        tt = (time.time() - st) / 1000
        #we need to store the expected output.....
        results = open("Files/Result.txt", "a")
        if(problem):
            result.write("case #" + str(i) + ":  ---------TLE---------\n\n")
            i+=1
        else:
            if(areFilesEqual('Files/output.txt', 'Files/Info/answers/ans{}.txt'.format(i))):
                results.write("case #" + str(i) + ": Passed in: " + "%.2f" % tt + " ms\n\n")
                Passed +=1
                TotalCases += 1
            else:
                print(areFilesEqual('Files/output.txt', 'Files/Info/answers/ans{}.txt'.format(i)))
                results.write("case #" + str(i) + ": -->Failed<-- in " + "%.2f" % tt + "ms\n\n")
                Failed += 1
                TotalCases += 1
                #need to add a button here
        i+=1
        t_line = testcases.readline()
        results.close()

    elif("Long input...." in t_line):
        result.write("case #" + str(i) + ": >>>>Long input..Skipped\n\n")
        t_line = readline()
        t_line = readline()
        i+=1
    else:
        input = open('Files/input.txt', 'w')
        while(t_line.find("case") == -1): #we dont find
            input.write(t_line)
            t_line = testcases.readline()
            while(t_line == '\n'):
                t_line = testcases.readline()
        input.close()

results.close()

line = "AC: "+str(Passed)+"\nWA: "+str(Failed)+"\nTLE: "+str(TimeLimit)+"\nTotalCases: "+str(TotalCases)+"\n\nUnjudged due to long input:"+str(Unjudjed)+"\n\n\n" + "--------------------DETAILS--------------------\n\n"
#to write this at the start of result.txt
with open('Files/Result.txt', 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(line + '\n' + content)

# root = Tk()
# retData = Label(root, text="Results declared! Good luck!").pack()
# root.after(1000, root.destroy)
# root.mainloop()
# print("Results declared! Good luck!\n\n")
# print("AC: "+str(Passed)+"\nWA: "+str(Failed)+"\nTLE: "+str(TimeLimit)+"\nTotalCases: "+str(TotalCases)+"\n\nUnjudged due to long input:"+str(Unjudjed))

def quit():
    root.destroy()
    os.rmdir('Files/Info')
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
