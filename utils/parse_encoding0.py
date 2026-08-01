
def parseEncoding0(charset, file):
    """
    Format 0: simple list of codes.
    After reading the base table, optionally parse the supplement.
    """
    nCodes = readCard8(file)
    encoding = [".notdef"] * 256
    for glyphID in range(1, nCodes + 1):
        code = readCard8(file)
        if code != 0:
            encoding[code] = charset[glyphID]

    return encoding

