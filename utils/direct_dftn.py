
def direct_dftn(x):
    x = asarray(x)
    for axis in range(len(x.shape)):
        x = fft(x, axis=axis)
    return x


def direct_dftn(x):
    x = asarray(x)
    for axis in range(x.ndim):
        x = fft(x, axis=axis)
    return x

