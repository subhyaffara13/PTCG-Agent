
def test_dmp_zz_i_factor():
    R, x, y = ring("x, y", ZZ_I)
    i = ZZ_I(0, 1)

    assert R.dmp_zz_i_factor(x**2 + 2*y**2) == \
            (ZZ_I(1, 0), [(x**2 + 2*y**2, 1)])

    assert R.dmp_zz_i_factor(x**2 + y**2) == \
            (ZZ_I(1, 0), [(x - i*y, 1), (x + i*y, 1)])

    assert R.dmp_zz_i_factor(4*x**2 + y**2) == \
            (ZZ_I(1, 0), [(2*x - i*y, 1), (2*x + i*y, 1)])

