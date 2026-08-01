
def mpi_cosh_sinh(x, prec):
    # TODO: accuracy for small x
    wp = prec+20
    e1 = mpi_exp(x, wp)
    e2 = mpi_div(mpi_one, e1, wp)
    c = mpi_add(e1, e2, prec)
    s = mpi_sub(e1, e2, prec)
    c = mpi_shift(c, -1)
    s = mpi_shift(s, -1)
    return c, s

