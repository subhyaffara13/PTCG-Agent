
def convertCFFToCFF2(font):
    cff = font["CFF "].cff
    del font["CFF "]
    _convertCFFToCFF2(cff, font)
    table = font["CFF2"] = newTable("CFF2")
    table.cff = cff

