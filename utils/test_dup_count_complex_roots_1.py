
def test_dup_count_complex_roots_1():
    R, x = ring("x", ZZ)

    # z-1
    f = x - 1
    assert R.dup_count_complex_roots(f, a, b) == 1
    assert R.dup_count_complex_roots(f, c, d) == 1

    # z+1
    f = x + 1
    assert R.dup_count_complex_roots(f, a, b) == 1
    assert R.dup_count_complex_roots(f, c, d) == 0

