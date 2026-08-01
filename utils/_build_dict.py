
def _buildDict():
    d = {}
    for mask, name, isDevice, signed in valueRecordFormat:
        d[name] = mask, isDevice, signed
    return d

