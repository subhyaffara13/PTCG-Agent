
def mpi_cot(x, prec):
    cos, sin = mpi_cos_sin(x, prec+20)
    return mpi_div(cos, sin, prec)

