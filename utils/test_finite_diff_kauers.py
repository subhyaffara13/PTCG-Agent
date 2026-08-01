
def test_finite_diff_kauers():
    assert finite_diff_kauers(Sum(x**2, (x, 1, n))) == (n + 1)**2
    assert finite_diff_kauers(Sum(y, (y, 1, m))) == (m + 1)
    assert finite_diff_kauers(Sum((x*y), (x, 1, m), (y, 1, n))) == (m + 1)*(n + 1)
    assert finite_diff_kauers(Sum((x*y**2), (x, 1, m), (y, 1, n))) == (n + 1)**2*(m + 1)

