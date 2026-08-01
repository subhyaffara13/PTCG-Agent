
def is_64bit():
    return struct.calcsize("P") == 8

