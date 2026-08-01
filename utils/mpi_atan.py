
def mpi_atan(s, prec):
    sa, sb = s
    a = mpf_atan(sa, prec, round_floor)
    b = mpf_atan(sb, prec, round_ceiling)
    return a, b

