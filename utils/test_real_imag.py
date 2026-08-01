
def test_real_imag():
    a, b = symbols('a b', real=True)
    z = a + b*I
    for deep in [True, False]:
        assert sin(
            z).as_real_imag(deep=deep) == (sin(a)*cosh(b), cos(a)*sinh(b))
        assert cos(
            z).as_real_imag(deep=deep) == (cos(a)*cosh(b), -sin(a)*sinh(b))
        assert tan(z).as_real_imag(deep=deep) == (sin(2*a)/(cos(2*a) +
            cosh(2*b)), sinh(2*b)/(cos(2*a) + cosh(2*b)))
        assert cot(z).as_real_imag(deep=deep) == (-sin(2*a)/(cos(2*a) -
            cosh(2*b)), sinh(2*b)/(cos(2*a) - cosh(2*b)))
        assert sin(a).as_real_imag(deep=deep) == (sin(a), 0)
        assert cos(a).as_real_imag(deep=deep) == (cos(a), 0)
        assert tan(a).as_real_imag(deep=deep) == (tan(a), 0)
        assert cot(a).as_real_imag(deep=deep) == (cot(a), 0)


def test_real_imag():
    x, y, z = symbols('x, y, z')
    X, Y, Z = symbols('X, Y, Z', commutative=False)
    a = Symbol('a', real=True)
    assert (2*a*x).as_real_imag() == (2*a*re(x), 2*a*im(x))

    # issue 5395:
    assert (x*x.conjugate()).as_real_imag() == (Abs(x)**2, 0)
    assert im(x*x.conjugate()) == 0
    assert im(x*y.conjugate()*z*y) == im(x*z)*Abs(y)**2
    assert im(x*y.conjugate()*x*y) == im(x**2)*Abs(y)**2
    assert im(Z*y.conjugate()*X*y) == im(Z*X)*Abs(y)**2
    assert im(X*X.conjugate()) == im(X*X.conjugate(), evaluate=False)
    assert (sin(x)*sin(x).conjugate()).as_real_imag() == \
        (Abs(sin(x))**2, 0)

    # issue 6573:
    assert (x**2).as_real_imag() == (re(x)**2 - im(x)**2, 2*re(x)*im(x))

    # issue 6428:
    r = Symbol('r', real=True)
    i = Symbol('i', imaginary=True)
    assert (i*r*x).as_real_imag() == (I*i*r*im(x), -I*i*r*re(x))
    assert (i*r*x*(y + 2)).as_real_imag() == (
        I*i*r*(re(y) + 2)*im(x) + I*i*r*re(x)*im(y),
        -I*i*r*(re(y) + 2)*re(x) + I*i*r*im(x)*im(y))

    # issue 7106:
    assert ((1 + I)/(1 - I)).as_real_imag() == (0, 1)
    assert ((1 + 2*I)*(1 + 3*I)).as_real_imag() == (-5, 5)

