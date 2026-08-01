
def cexpm1(x, y):
    z = expm1(x + 1j*y)
    return z.real, z.imag

