
def parseCharset(numGlyphs, file, strings, isCID, fmt):
    charset = [".notdef"]
    count = 1
    if fmt == 1:
        nLeftFunc = readCard8
    else:
        nLeftFunc = readCard16
    while count < numGlyphs:
        first = readCard16(file)
        nLeft = nLeftFunc(file)
        if isCID:
            for CID in range(first, first + nLeft + 1):
                charset.append("cid" + str(CID).zfill(5))
        else:
            for SID in range(first, first + nLeft + 1):
                charset.append(strings[SID])
        count = count + nLeft + 1
    return charset

