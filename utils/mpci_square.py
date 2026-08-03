import re

def mpci_square(x, prec):
    a, b = x
    # (a+bi)^2 = (a^2-b^2) + 2abi
    re = mpi_sub(mpi_square(a), mpi_square(b), prec)
    im = mpi_mul(a, b, prec)
    im = mpi_shift(im, 1)
    return re, im

