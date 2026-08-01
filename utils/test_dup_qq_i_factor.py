
def test_dup_qq_i_factor():
    R, x = ring("x", QQ_I)
    i = QQ_I(0, 1)

    assert R.dup_qq_i_factor(x**2 - 2) == (QQ_I(1, 0), [(x**2 - 2, 1)])

    assert R.dup_qq_i_factor(x**2 - 1) == (QQ_I(1, 0), [(x - 1, 1), (x + 1, 1)])

    assert R.dup_qq_i_factor(x**2 + 1) == (QQ_I(1, 0), [(x - i, 1), (x + i, 1)])

    assert R.dup_qq_i_factor(x**2/4 + 1) == \
            (QQ_I(QQ(1, 4), 0), [(x - 2*i, 1), (x + 2*i, 1)])

    assert R.dup_qq_i_factor(x**2 + 4) == \
            (QQ_I(1, 0), [(x - 2*i, 1), (x + 2*i, 1)])

    assert R.dup_qq_i_factor(x**2 + 2*x + 1) == \
            (QQ_I(1, 0), [(x + 1, 2)])

    assert R.dup_qq_i_factor(x**2 + 2*i*x - 1) == \
            (QQ_I(1, 0), [(x + i, 2)])

    f = 8192*x**2 + x*(22656 + 175232*i) - 921416 + 242313*i

    assert R.dup_qq_i_factor(f) == \
            (QQ_I(8192, 0), [(x + QQ_I(QQ(177, 128), QQ(1369, 128)), 2)])

