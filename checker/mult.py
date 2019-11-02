def areFilesEqual(file1, file2):
    f1 = open(file1).read().splitlines()
    f2 = open(file2).read().splitlines()

    if(len(f1) != len(f2)):
        return False
    else:
        for (l1, l2) in zip(f1, f2):
            if(l1.rstrip() != l2.rstrip()):
                return False
    return True

print(areFilesEqual('a.txt', 'b.txt'))
