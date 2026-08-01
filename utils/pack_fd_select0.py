
def packFDSelect0(fdSelectArray):
    fmt = 0
    data = [packCard8(fmt)]
    for index in fdSelectArray:
        data.append(packCard8(index))
    return bytesjoin(data)

