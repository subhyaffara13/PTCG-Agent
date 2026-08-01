
def test_triangular():
    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")

    X = Triangular('x', a, b, c)
    assert pspace(X).domain.set == Interval(a, b)
    assert str(density(X)(x)) == ("Piecewise(((-2*a + 2*x)/((-a + b)*(-a + c)), (a <= x) & (c > x)), "
    "(2/(-a + b), Eq(c, x)), ((2*b - 2*x)/((-a + b)*(b - c)), (b >= x) & (c < x)), (0, True))")

    #Tests moment_generating_function
    assert moment_generating_function(X)(x).expand() == \
    ((-2*(-a + b)*exp(c*x) + 2*(-a + c)*exp(b*x) + 2*(b - c)*exp(a*x))/(x**2*(-a + b)*(-a + c)*(b - c))).expand()
    assert str(characteristic_function(X)(x)) == \
    '(2*(-a + b)*exp(I*c*x) - 2*(-a + c)*exp(I*b*x) - 2*(b - c)*exp(I*a*x))/(x**2*(-a + b)*(-a + c)*(b - c))'


def test_triangular():
    assert ask(Q.upper_triangular(X + Z.T + Identity(2)), Q.upper_triangular(X) &
            Q.lower_triangular(Z)) is True
    assert ask(Q.upper_triangular(X*Z.T), Q.upper_triangular(X) &
            Q.lower_triangular(Z)) is True
    assert ask(Q.lower_triangular(Identity(3))) is True
    assert ask(Q.lower_triangular(ZeroMatrix(3, 3))) is True
    assert ask(Q.upper_triangular(ZeroMatrix(3, 3))) is True
    assert ask(Q.lower_triangular(OneMatrix(1, 1))) is True
    assert ask(Q.upper_triangular(OneMatrix(1, 1))) is True
    assert ask(Q.lower_triangular(OneMatrix(3, 3))) is False
    assert ask(Q.upper_triangular(OneMatrix(3, 3))) is False
    assert ask(Q.triangular(X), Q.unit_triangular(X))
    assert ask(Q.upper_triangular(X**3), Q.upper_triangular(X))
    assert ask(Q.lower_triangular(X**3), Q.lower_triangular(X))

