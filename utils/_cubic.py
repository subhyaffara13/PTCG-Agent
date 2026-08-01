
def _cubic(x):
    xp = array_namespace(x)

    x = np.asarray(x, dtype=float)
    b = BSpline.basis_element([-2, -1, 0, 1, 2], extrapolate=False)
    out = b(x)
    out[(x < -2) | (x > 2)] = 0
    return xp.asarray(out)

