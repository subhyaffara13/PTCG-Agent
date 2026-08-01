
def test_collect_3():
    """Collect with respect to a product"""
    a, b, c = symbols('a,b,c')
    f = Function('f')
    x, y, z, n = symbols('x,y,z,n')

    assert collect(-x/8 + x*y, -x) == x*(y - Rational(1, 8))

    assert collect( 1 + x*(y**2), x*y ) == 1 + x*(y**2)
    assert collect( x*y + a*x*y, x*y) == x*y*(1 + a)
    assert collect( 1 + x*y + a*x*y, x*y) == 1 + x*y*(1 + a)
    assert collect(a*x*f(x) + b*(x*f(x)), x*f(x)) == x*(a + b)*f(x)

    assert collect(a*x*log(x) + b*(x*log(x)), x*log(x)) == x*(a + b)*log(x)
    assert collect(a*x**2*log(x)**2 + b*(x*log(x))**2, x*log(x)) == \
        x**2*log(x)**2*(a + b)

    # with respect to a product of three symbols
    assert collect(y*x*z + a*x*y*z, x*y*z) == (1 + a)*x*y*z

