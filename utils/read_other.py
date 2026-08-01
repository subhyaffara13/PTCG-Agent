
def readOther(path):
    """reads any (font) file, returns raw data"""
    with open(path, "rb") as f:
        data = f.read()
    assertType1(data)
    chunks = findEncryptedChunks(data)
    data = []
    for isEncrypted, chunk in chunks:
        if isEncrypted and isHex(chunk[:4]):
            data.append(deHexString(chunk))
        else:
            data.append(chunk)
    return bytesjoin(data)

