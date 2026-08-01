
def test_dup_zz_hensel_lift():
    R, x = ring("x", ZZ)

    f = x**4 - 1
    F = [x - 1, x - 2, x + 2, x + 1]

    assert R.dup_zz_hensel_lift(ZZ(5), f, F, 4) == \
        [x - 1, x - 182, x + 182, x + 1]

