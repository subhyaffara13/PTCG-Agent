
def _dual_poly(j, k, t, y):
    """
    Dual polynomial of the B-spline B_{j,k,t} -
    polynomial which is associated with B_{j,k,t}:
    $p_{j,k}(y) = (y - t_{j+1})(y - t_{j+2})...(y - t_{j+k})$
    """
    if k == 0:
        return 1
    return np.prod([(y - t[j + i]) for i in range(1, k + 1)])

