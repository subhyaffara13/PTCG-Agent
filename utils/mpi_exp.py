
def mpi_exp(s, prec):
    sa, sb = s
    # exp is monotonic
    a = mpf_exp(sa, prec, round_floor)
    b = mpf_exp(sb, prec, round_ceiling)
    return a, b

