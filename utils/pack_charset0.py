
def packCharset0(charset, isCID, strings):
    fmt = 0
    data = [packCard8(fmt)]
    if isCID:
        getNameID = getCIDfromName
    else:
        getNameID = getSIDfromName

    for name in charset[1:]:
        data.append(packCard16(getNameID(name, strings)))
    return bytesjoin(data)

