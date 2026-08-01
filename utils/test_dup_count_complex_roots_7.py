
def test_dup_count_complex_roots_7():
    R, x = ring("x", ZZ)

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)
    f = x**4 + 4
    assert R.dup_count_complex_roots(f, a, b) == 4
    assert R.dup_count_complex_roots(f, c, d) == 1

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z-2)
    f = x**5 - 2*x**4 + 4*x - 8
    assert R.dup_count_complex_roots(f, a, b) == 4
    assert R.dup_count_complex_roots(f, c, d) == 1

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z**2-2)
    f = x**6 - 2*x**4 + 4*x**2 - 8
    assert R.dup_count_complex_roots(f, a, b) == 4
    assert R.dup_count_complex_roots(f, c, d) == 1

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z-1)
    f = x**5 - x**4 + 4*x - 4
    assert R.dup_count_complex_roots(f, a, b) == 5
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z-1)*z
    f = x**6 - x**5 + 4*x**2 - 4*x
    assert R.dup_count_complex_roots(f, a, b) == 6
    assert R.dup_count_complex_roots(f, c, d) == 3

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z+1)
    f = x**5 + x**4 + 4*x + 4
    assert R.dup_count_complex_roots(f, a, b) == 5
    assert R.dup_count_complex_roots(f, c, d) == 1

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z+1)*z
    f = x**6 + x**5 + 4*x**2 + 4*x
    assert R.dup_count_complex_roots(f, a, b) == 6
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z-1)*(z+1)
    f = x**6 - x**4 + 4*x**2 - 4
    assert R.dup_count_complex_roots(f, a, b) == 6
    assert R.dup_count_complex_roots(f, c, d) == 2

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z-1)*(z+1)*z
    f = x**7 - x**5 + 4*x**3 - 4*x
    assert R.dup_count_complex_roots(f, a, b) == 7
    assert R.dup_count_complex_roots(f, c, d) == 3

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z-1)*(z+1)*(z-I)*(z+I)
    f = x**8 + 3*x**4 - 4
    assert R.dup_count_complex_roots(f, a, b) == 8
    assert R.dup_count_complex_roots(f, c, d) == 3

