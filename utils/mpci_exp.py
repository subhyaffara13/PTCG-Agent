
def mpci_exp(x, prec):
    a, b = x
    wp = prec+20
    r = mpi_exp(a, wp)
    c, s = mpi_cos_sin(b, wp)
    a = mpi_mul(r, c, prec)
    b = mpi_mul(r, s, prec)
    return a, b

