
def mpi_lt(s, t):
    sa, sb = s
    ta, tb = t
    if mpf_lt(sb, ta): return True
    if mpf_ge(sa, tb): return False
    return None

