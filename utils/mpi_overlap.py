
def mpi_overlap(x, y):
    a, b = x
    c, d = y
    if mpf_lt(d, a): return False
    if mpf_gt(c, b): return False
    return True

