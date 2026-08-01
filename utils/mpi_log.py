
def mpi_log(s, prec):
    sa, sb = s
    # log is monotonic
    a = mpf_log(sa, prec, round_floor)
    b = mpf_log(sb, prec, round_ceiling)
    return a, b

