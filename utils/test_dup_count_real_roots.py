
def test_dup_count_real_roots():
    R, x = ring("x", ZZ)

    assert R.dup_count_real_roots(0) == 0
    assert R.dup_count_real_roots(7) == 0

    f = x - 1
    assert R.dup_count_real_roots(f) == 1
    assert R.dup_count_real_roots(f, inf=1) == 1
    assert R.dup_count_real_roots(f, sup=0) == 0
    assert R.dup_count_real_roots(f, sup=1) == 1
    assert R.dup_count_real_roots(f, inf=0, sup=1) == 1
    assert R.dup_count_real_roots(f, inf=0, sup=2) == 1
    assert R.dup_count_real_roots(f, inf=1, sup=2) == 1

    f = x**2 - 2
    assert R.dup_count_real_roots(f) == 2
    assert R.dup_count_real_roots(f, sup=0) == 1
    assert R.dup_count_real_roots(f, inf=-1, sup=1) == 0

