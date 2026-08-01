
def flagFits(newFlag, oldFlag, mask):
    newBytes = _flagSignBytes[newFlag & mask]
    oldBytes = _flagSignBytes[oldFlag & mask]
    return newBytes == oldBytes or abs(newBytes) > abs(oldBytes)

