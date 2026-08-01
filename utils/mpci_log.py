
def mpci_log(z, prec):
    x, y = z
    re = mpi_log(mpci_abs(z, prec+20), prec)
    im = mpci_arg(z, prec)
    return re, im

