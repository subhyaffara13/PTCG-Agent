
def make_nonnative(arrs):
    return [a.astype(a.dtype.newbyteorder()) for a in arrs]

