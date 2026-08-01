
def _quadratic(B, x):
    return x*(x*B[0] + B[1]) + B[2]


def _quadratic(x):
    xp = array_namespace(x)

    x = abs(np.asarray(x, dtype=float))
    b = BSpline.basis_element([-1.5, -0.5, 0.5, 1.5], extrapolate=False)
    out = b(x)
    out[(x < -1.5) | (x > 1.5)] = 0
    return xp.asarray(out)

