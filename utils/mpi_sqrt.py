
def mpi_sqrt(s, prec):
    sa, sb = s
    # sqrt is monotonic
    a = mpf_sqrt(sa, prec, round_floor)
    b = mpf_sqrt(sb, prec, round_ceiling)
    return a, b

