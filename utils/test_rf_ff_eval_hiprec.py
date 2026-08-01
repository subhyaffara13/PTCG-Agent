
def test_rf_ff_eval_hiprec():
    maple = Float('6.9109401292234329956525265438452')
    us = ff(18, Rational(2, 3)).evalf(32)
    assert abs(us - maple)/us < 1e-31

    maple = Float('6.8261540131125511557924466355367')
    us = rf(18, Rational(2, 3)).evalf(32)
    assert abs(us - maple)/us < 1e-31

    maple = Float('34.007346127440197150854651814225')
    us = rf(Float('4.4', 32), Float('2.2', 32))
    assert abs(us - maple)/us < 1e-31

