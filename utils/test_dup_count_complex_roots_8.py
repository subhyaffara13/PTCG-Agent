
def test_dup_count_complex_roots_8():
    R, x = ring("x", ZZ)

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z-1)*(z+1)*(z-I)*(z+I)*z
    f = x**9 + 3*x**5 - 4*x
    assert R.dup_count_complex_roots(f, a, b) == 9
    assert R.dup_count_complex_roots(f, c, d) == 4

    # (z-I-1)*(z+I-1)*(z-I+1)*(z+I+1)*(z-1)*(z+1)*(z-I)*(z+I)*(z**2-2)*z
    f = x**11 - 2*x**9 + 3*x**7 - 6*x**5 - 4*x**3 + 8*x
    assert R.dup_count_complex_roots(f, a, b) == 9
    assert R.dup_count_complex_roots(f, c, d) == 4

