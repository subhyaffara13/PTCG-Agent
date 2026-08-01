
def _all_partitions(nx, ny):
    """
    Partition a set of indices into two fixed-length sets in all possible ways

    Partition a set of indices 0 ... nx + ny - 1 into two sets of length nx and
    ny in all possible ways (ignoring order of elements).
    """
    z = np.arange(nx+ny)
    for c in combinations(z, nx):
        x = np.array(c)
        mask = np.ones(nx+ny, bool)
        mask[x] = False
        y = z[mask]
        yield x, y

