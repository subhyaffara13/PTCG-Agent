
def test_dup_count_complex_roots_4():
    R, x = ring("x", ZZ)

    # (z-I)*(z+I)
    f = x**2 + 1
    assert R.dup_count_complex_roots(f, a, b) == 2
    assert R.dup_count_complex_roots(f, c, d) == 1

    # (z-I)*(z+I)*(z)
    f = x**3 + x
    assert R.dup_count_complex_roots(f, a, b) == 3
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I)*(z+I)*(-z)
    f = -x**3 - x
    assert R.dup_count_complex_roots(f, a, b) == 3
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I)*(z+I)*(z-1)
    f = x**3 - x**2 + x - 1
    assert R.dup_count_complex_roots(f, a, b) == 3
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I)*(z+I)*(z-1)*(z)
    f = x**4 - x**3 + x**2 - x
    assert R.dup_count_complex_roots(f, a, b) == 4
    assert R.dup_count_complex_roots(f, c, d) == 3

    # (z-I)*(z+I)*(z-1)*(-z)
    f = -x**4 + x**3 - x**2 + x
    assert R.dup_count_complex_roots(f, a, b) == 4
    assert R.dup_count_complex_roots(f, c, d) == 3

    # (z-I)*(z+I)*(z-1)*(z+1)
    f = x**4 - 1
    assert R.dup_count_complex_roots(f, a, b) == 4
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I)*(z+I)*(z-1)*(z+1)*(z)
    f = x**5 - x
    assert R.dup_count_complex_roots(f, a, b) == 5
    assert R.dup_count_complex_roots(f, c, d) == 3

    # (z-I)*(z+I)*(z-1)*(z+1)*(-z)
    f = -x**5 + x
    assert R.dup_count_complex_roots(f, a, b) == 5
    assert R.dup_count_complex_roots(f, c, d) == 3

