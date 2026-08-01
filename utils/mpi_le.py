
def mpi_le(s, t):
    sa, sb = s
    ta, tb = t
    if mpf_le(sb, ta): return True
    if mpf_gt(sa, tb): return False
    return None

