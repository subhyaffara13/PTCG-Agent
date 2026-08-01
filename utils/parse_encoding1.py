
def parseEncoding1(charset, file):
    """
    Format 1: range-based encoding.
    After reading the base ranges, optionally parse the supplement.
    """
    nRanges = readCard8(file)
    encoding = [".notdef"] * 256
    glyphID = 1
    for _ in range(nRanges):
        code = readCard8(file)
        nLeft = readCard8(file)
        for _ in range(nLeft + 1):
            encoding[code] = charset[glyphID]
            code += 1
            glyphID += 1

    return encoding

