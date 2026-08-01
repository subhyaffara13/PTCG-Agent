
def _binary2data(binary):
    byteList = []
    for bitLoc in range(0, len(binary), 8):
        byteString = binary[bitLoc : bitLoc + 8]
        curByte = 0
        for curBit in reversed(byteString):
            curByte = curByte << 1
            if curBit == "1":
                curByte |= 1
        byteList.append(bytechr(curByte))
    return bytesjoin(byteList)

