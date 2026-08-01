
def bspline2(xy, t, c, k):
    """A naive 2D tensort product spline evaluation."""
    x, y = xy
    tx, ty = t
    nx = len(tx) - k - 1
    assert (nx >= k+1)
    ny = len(ty) - k - 1
    assert (ny >= k+1)
    res = sum(c[ix, iy] * B(x, k, ix, tx) * B(y, k, iy, ty)
              for ix in range(nx) for iy in range(ny))
    return np.asarray(res)

