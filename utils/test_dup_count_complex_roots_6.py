
def test_dup_count_complex_roots_6():
    R, x = ring("x", ZZ)

    # (z-I-1)*(z+I-1)
    f = x**2 - 2*x + 2
    assert R.dup_count_complex_roots(f, a, b) == 2
    assert R.dup_count_complex_roots(f, c, d) == 1

    # (z-I-1)*(z+I-1)*(z-1)
    f = x**3 - 3*x**2 + 4*x - 2
    assert R.dup_count_complex_roots(f, a, b) == 3
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I-1)*(z+I-1)*(z-1)*z
    f = x**4 - 3*x**3 + 4*x**2 - 2*x
    assert R.dup_count_complex_roots(f, a, b) == 4
    assert R.dup_count_complex_roots(f, c, d) == 3

    # (z-I-1)*(z+I-1)*(z+1)
    f = x**3 - x**2 + 2
    assert R.dup_count_complex_roots(f, a, b) == 3
    assert R.dup_count_complex_roots(f, c, d) == 1

    # (z-I-1)*(z+I-1)*(z+1)*z
    f = x**4 - x**3 + 2*x
    assert R.dup_count_complex_roots(f, a, b) == 4
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I-1)*(z+I-1)*(z-1)*(z+1)
    f = x**4 - 2*x**3 + x**2 + 2*x - 2
    assert R.dup_count_complex_roots(f, a, b) == 4
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I-1)*(z+I-1)*(z-1)*(z+1)*z
    f = x**5 - 2*x**4 + x**3 + 2*x**2 - 2*x
    assert R.dup_count_complex_roots(f, a, b) == 5
    assert R.dup_count_complex_roots(f, c, d) == 3

