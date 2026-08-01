
def mpci_sub(x, y, prec):
    a, b = x
    c, d = y
    return mpi_sub(a, c, prec), mpi_sub(b, d, prec)

