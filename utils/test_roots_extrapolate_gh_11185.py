
def test_roots_extrapolate_gh_11185():
    x = np.array([0.001, 0.002])
    y = np.array([1.66066935e-06, 1.10410807e-06])
    dy = np.array([-1.60061854, -1.600619])
    p = CubicHermiteSpline(x, y, dy)

    # roots(extrapolate=True) for a polynomial with a single interval
    # should return all three real roots
    r = p.roots(extrapolate=True)
    assert p.c.shape[1] == 1
    assert r.size == 3

