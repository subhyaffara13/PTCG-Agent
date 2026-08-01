
def mpci_abs(x, prec):
    a, b = x
    if a == mpi_zero:
        return mpi_abs(b)
    if b == mpi_zero:
        return mpi_abs(a)
    # Important: nonnegative
    a = mpi_square(a)
    b = mpi_square(b)
    t = mpi_add(a, b, prec+20)
    return mpi_sqrt(t, prec)

