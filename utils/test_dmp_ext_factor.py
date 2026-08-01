
def test_dmp_ext_factor():
    K = QQ.algebraic_field(sqrt(2))
    R, x,y = ring("x,y", K)
    sqrt2 = K.unit

    def anp(x):
        return ANP(x, [QQ(1), QQ(0), QQ(-2)], QQ)

    assert R.dmp_ext_factor(0) == (anp([]), [])

    f = anp([QQ(1)])*x + anp([QQ(1)])

    assert R.dmp_ext_factor(f) == (anp([QQ(1)]), [(f, 1)])

    g = anp([QQ(2)])*x + anp([QQ(2)])

    assert R.dmp_ext_factor(g) == (anp([QQ(2)]), [(f, 1)])

    f = anp([QQ(1)])*x**2 + anp([QQ(-2)])*y**2

    assert R.dmp_ext_factor(f) == \
        (anp([QQ(1)]), [(anp([QQ(1)])*x + anp([QQ(-1), QQ(0)])*y, 1),
                        (anp([QQ(1)])*x + anp([QQ( 1), QQ(0)])*y, 1)])

    f = anp([QQ(2)])*x**2 + anp([QQ(-4)])*y**2

    assert R.dmp_ext_factor(f) == \
        (anp([QQ(2)]), [(anp([QQ(1)])*x + anp([QQ(-1), QQ(0)])*y, 1),
                        (anp([QQ(1)])*x + anp([QQ( 1), QQ(0)])*y, 1)])

    f1 = y + 1
    f2 = y + sqrt2
    f3 = x**2 + x + 2 + 3*sqrt2
    f = f1**2 * f2**2 * f3**2
    assert R.dmp_ext_factor(f) == (K.one, [(f1, 2), (f2, 2), (f3, 2)])

