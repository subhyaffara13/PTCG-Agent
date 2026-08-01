
def encodeNumber(num):
    if isinstance(num, float):
        return psCharStrings.encodeFloat(num)
    else:
        return psCharStrings.encodeIntCFF(num)

