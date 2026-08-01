
def packFDSelect3(fdSelectArray):
    fmt = 3
    fdRanges = []
    lenArray = len(fdSelectArray)
    lastFDIndex = -1
    for i in range(lenArray):
        fdIndex = fdSelectArray[i]
        if lastFDIndex != fdIndex:
            fdRanges.append([i, fdIndex])
            lastFDIndex = fdIndex
    sentinelGID = i + 1

    data = [packCard8(fmt)]
    data.append(packCard16(len(fdRanges)))
    for fdRange in fdRanges:
        data.append(packCard16(fdRange[0]))
        data.append(packCard8(fdRange[1]))
    data.append(packCard16(sentinelGID))
    return bytesjoin(data)

