
def mpi_sub(s, t, prec=0):
    sa, sb = s
    ta, tb = t
    a = mpf_sub(sa, tb, prec, round_floor)
    b = mpf_sub(sb, ta, prec, round_ceiling)
    if a == fnan: a = fninf
    if b == fnan: b = finf
    return a, b

