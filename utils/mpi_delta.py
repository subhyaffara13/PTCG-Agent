
def mpi_delta(s, prec):
    sa, sb = s
    return mpf_sub(sb, sa, prec, round_up)

