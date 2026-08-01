
def test_dup_count_complex_roots_3():
    R, x = ring("x", ZZ)

    # (z-1)*(z+1)
    f = x**2 - 1
    assert R.dup_count_complex_roots(f, a, b) == 2
    assert R.dup_count_complex_roots(f, c, d) == 1

    # (z-1)*(z+1)*(z)
    f = x**3 - x
    assert R.dup_count_complex_roots(f, a, b) == 3
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-1)*(z+1)*(-z)
    f = -x**3 + x
    assert R.dup_count_complex_roots(f, a, b) == 3
    assert R.dup_count_complex_roots(f, c, d) == 2

