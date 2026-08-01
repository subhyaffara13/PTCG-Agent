
def clog1p(x, y):
    z = log1p(x + 1j*y)
    return z.real, z.imag

