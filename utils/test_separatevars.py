
def test_separatevars():
    x, y, z, n = symbols('x,y,z,n')
    assert separatevars(2*n*x*z + 2*x*y*z) == 2*x*z*(n + y)
    assert separatevars(x*z + x*y*z) == x*z*(1 + y)
    assert separatevars(pi*x*z + pi*x*y*z) == pi*x*z*(1 + y)
    assert separatevars(x*y**2*sin(x) + x*sin(x)*sin(y)) == \
        x*(sin(y) + y**2)*sin(x)
    assert separatevars(x*exp(x + y) + x*exp(x)) == x*(1 + exp(y))*exp(x)
    assert separatevars((x*(y + 1))**z).is_Pow  # != x**z*(1 + y)**z
    assert separatevars(1 + x + y + x*y) == (x + 1)*(y + 1)
    assert separatevars(y/pi*exp(-(z - x)/cos(n))) == \
        y*exp(x/cos(n))*exp(-z/cos(n))/pi
    assert separatevars((x + y)*(x - y) + y**2 + 2*x + 1) == (x + 1)**2
    # issue 4858
    p = Symbol('p', positive=True)
    assert separatevars(sqrt(p**2 + x*p**2)) == p*sqrt(1 + x)
    assert separatevars(sqrt(y*(p**2 + x*p**2))) == p*sqrt(y*(1 + x))
    assert separatevars(sqrt(y*(p**2 + x*p**2)), force=True) == \
        p*sqrt(y)*sqrt(1 + x)
    # issue 4865
    assert separatevars(sqrt(x*y)).is_Pow
    assert separatevars(sqrt(x*y), force=True) == sqrt(x)*sqrt(y)
    # issue 4957
    # any type sequence for symbols is fine
    assert separatevars(((2*x + 2)*y), dict=True, symbols=()) == \
        {'coeff': 1, x: 2*x + 2, y: y}
    # separable
    assert separatevars(((2*x + 2)*y), dict=True, symbols=[x]) == \
        {'coeff': y, x: 2*x + 2}
    assert separatevars(((2*x + 2)*y), dict=True, symbols=[]) == \
        {'coeff': 1, x: 2*x + 2, y: y}
    assert separatevars(((2*x + 2)*y), dict=True) == \
        {'coeff': 1, x: 2*x + 2, y: y}
    assert separatevars(((2*x + 2)*y), dict=True, symbols=None) == \
        {'coeff': y*(2*x + 2)}
    # not separable
    assert separatevars(3, dict=True) is None
    assert separatevars(2*x + y, dict=True, symbols=()) is None
    assert separatevars(2*x + y, dict=True) is None
    assert separatevars(2*x + y, dict=True, symbols=None) == {'coeff': 2*x + y}
    # issue 4808
    n, m = symbols('n,m', commutative=False)
    assert separatevars(m + n*m) == (1 + n)*m
    assert separatevars(x + x*n) == x*(1 + n)
    # issue 4910
    f = Function('f')
    assert separatevars(f(x) + x*f(x)) == f(x) + x*f(x)
    # a noncommutable object present
    eq = x*(1 + hyper((), (), y*z))
    assert separatevars(eq) == eq

    s = separatevars(abs(x*y))
    assert s == abs(x)*abs(y) and s.is_Mul
    z = cos(1)**2 + sin(1)**2 - 1
    a = abs(x*z)
    s = separatevars(a)
    assert not a.is_Mul and s.is_Mul and s == abs(x)*abs(z)
    s = separatevars(abs(x*y*z))
    assert s == abs(x)*abs(y)*abs(z)

    # abs(x+y)/abs(z) would be better but we test this here to
    # see that it doesn't raise
    assert separatevars(abs((x+y)/z)) == abs((x+y)/z)

