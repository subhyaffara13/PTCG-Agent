
def test_issue_10681():
    from sympy.polys.domains.realfield import RR
    from sympy.abc import R, r
    f = integrate(r**2*(R**2-r**2)**0.5, r, meijerg=True)
    g = (1.0/3)*R**1.0*r**3*hyper((-0.5, Rational(3, 2)), (Rational(5, 2),),
                                  r**2*exp_polar(2*I*pi)/R**2)
    assert RR.almosteq((f/g).n(), 1.0, 1e-12)

