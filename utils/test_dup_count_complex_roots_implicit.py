
def test_dup_count_complex_roots_implicit():
    R, x = ring("x", ZZ)

    # z*(z-1)*(z+1)*(z-I)*(z+I)
    f = x**5 - x

    assert R.dup_count_complex_roots(f) == 5

    assert R.dup_count_complex_roots(f, sup=(0, 0)) == 3
    assert R.dup_count_complex_roots(f, inf=(0, 0)) == 3

