
def test_meijerg_with_Floats():
    # see issue #10681
    from sympy.polys.domains.realfield import RR
    f = meijerg(((3.0, 1), ()), ((Rational(3, 2),), (0,)), z)
    a = -2.3632718012073
    g = a*z**Rational(3, 2)*hyper((-0.5, Rational(3, 2)), (Rational(5, 2),), z*exp_polar(I*pi))
    assert RR.almosteq((hyperexpand(f)/g).n(), 1.0, 1e-12)

