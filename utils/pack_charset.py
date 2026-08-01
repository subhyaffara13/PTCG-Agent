
def packCharset(charset, isCID, strings):
    fmt = 1
    ranges = []
    first = None
    end = 0
    if isCID:
        getNameID = getCIDfromName
    else:
        getNameID = getSIDfromName

    for name in charset[1:]:
        SID = getNameID(name, strings)
        if first is None:
            first = SID
        elif end + 1 != SID:
            nLeft = end - first
            if nLeft > 255:
                fmt = 2
            ranges.append((first, nLeft))
            first = SID
        end = SID
    if end:
        nLeft = end - first
        if nLeft > 255:
            fmt = 2
        ranges.append((first, nLeft))

    data = [packCard8(fmt)]
    if fmt == 1:
        nLeftFunc = packCard8
    else:
        nLeftFunc = packCard16
    for first, nLeft in ranges:
        data.append(packCard16(first) + nLeftFunc(nLeft))
    return bytesjoin(data)

