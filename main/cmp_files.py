import filecmp

if(filecmp.cmp('file1.txt', 'file2.txt')):
    print("they are the same")
