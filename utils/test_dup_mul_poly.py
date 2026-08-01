
def test_dup_mul_poly():
    p = Poly(18786186952704.0*x**165 + 9.31746684052255e+31*x**82, x, domain='RR')
    px = Poly(18786186952704.0*x**166 + 9.31746684052255e+31*x**83, x, domain='RR')

    assert p * x == px
    assert p.set_domain(QQ) * x == px.set_domain(QQ)
    assert p.set_domain(CC) * x == px.set_domain(CC)

