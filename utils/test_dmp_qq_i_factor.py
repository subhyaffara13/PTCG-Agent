
def test_dmp_qq_i_factor():
    R, x, y = ring("x, y", QQ_I)
    i = QQ_I(0, 1)

    assert R.dmp_qq_i_factor(x**2 + 2*y**2) == \
            (QQ_I(1, 0), [(x**2 + 2*y**2, 1)])

    assert R.dmp_qq_i_factor(x**2 + y**2) == \
            (QQ_I(1, 0), [(x - i*y, 1), (x + i*y, 1)])

    assert R.dmp_qq_i_factor(x**2 + y**2/4) == \
            (QQ_I(1, 0), [(x - i*y/2, 1), (x + i*y/2, 1)])

    assert R.dmp_qq_i_factor(4*x**2 + y**2) == \
            (QQ_I(4, 0), [(x - i*y/2, 1), (x + i*y/2, 1)])

