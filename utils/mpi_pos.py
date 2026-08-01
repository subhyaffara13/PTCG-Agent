
def mpi_pos(s, prec):
    sa, sb = s
    a = mpf_pos(sa, prec, round_floor)
    b = mpf_pos(sb, prec, round_ceiling)
    return a, b

