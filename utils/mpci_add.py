
def mpci_add(x, y, prec):
    a, b = x
    c, d = y
    return mpi_add(a, c, prec), mpi_add(b, d, prec)

