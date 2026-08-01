
def parseCharset0(numGlyphs, file, strings, isCID):
    charset = [".notdef"]
    if isCID:
        for i in range(numGlyphs - 1):
            CID = readCard16(file)
            charset.append("cid" + str(CID).zfill(5))
    else:
        for i in range(numGlyphs - 1):
            SID = readCard16(file)
            charset.append(strings[SID])
    return charset

