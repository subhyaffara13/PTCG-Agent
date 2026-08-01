
def direct_idftn(x):
    x = asarray(x)
    for axis in range(len(x.shape)):
        x = ifft(x, axis=axis)
    return x


def direct_idftn(x):
    x = asarray(x)
    for axis in range(x.ndim):
        x = ifft(x, axis=axis)
    return x

