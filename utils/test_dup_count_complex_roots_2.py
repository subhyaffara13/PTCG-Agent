
def test_dup_count_complex_roots_2():
    R, x = ring("x", ZZ)

    # (z-1)*(z)
    f = x**2 - x
    assert R.dup_count_complex_roots(f, a, b) == 2
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-1)*(-z)
    f = -x**2 + x
    assert R.dup_count_complex_roots(f, a, b) == 2
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z+1)*(z)
    f = x**2 + x
    assert R.dup_count_complex_roots(f, a, b) == 2
    assert R.dup_count_complex_roots(f, c, d) == 1

    # (z+1)*(-z)
    f = -x**2 - x
    assert R.dup_count_complex_roots(f, a, b) == 2
    assert R.dup_count_complex_roots(f, c, d) == 1

