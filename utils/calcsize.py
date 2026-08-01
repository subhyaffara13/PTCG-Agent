
def calcsize(fmt):
    formatstring, names, fixes = getformat(fmt)
    return struct.calcsize(formatstring)

