
def mpi_pi(prec):
    a = mpf_pi(prec, round_floor)
    b = mpf_pi(prec, round_ceiling)
    return a, b

