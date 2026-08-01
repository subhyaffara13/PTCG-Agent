
def mpci_sin(x, prec):
    a, b = x
    wp = prec+10
    c, s = mpi_cos_sin(a, wp)
    ch, sh = mpi_cosh_sinh(b, wp)
    re = mpi_mul(s, ch, prec)
    im = mpi_mul(c, sh, prec)
    return re, im

