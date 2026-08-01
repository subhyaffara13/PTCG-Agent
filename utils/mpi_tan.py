
def mpi_tan(x, prec):
    cos, sin = mpi_cos_sin(x, prec+20)
    return mpi_div(sin, cos, prec)

