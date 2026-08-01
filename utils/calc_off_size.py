
def calcOffSize(largestOffset):
    if largestOffset < 0x100:
        offSize = 1
    elif largestOffset < 0x10000:
        offSize = 2
    elif largestOffset < 0x1000000:
        offSize = 3
    else:
        offSize = 4
    return offSize

