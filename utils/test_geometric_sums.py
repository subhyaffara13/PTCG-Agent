
def test_geometric_sums():
    assert summation(pi**n, (n, 0, b)) == (1 - pi**(b + 1)) / (1 - pi)
    assert summation(2 * 3**n, (n, 0, b)) == 3**(b + 1) - 1
    assert summation(S.Half**n, (n, 1, oo)) == 1
    assert summation(2**n, (n, 0, b)) == 2**(b + 1) - 1
    assert summation(2**n, (n, 1, oo)) is oo
    assert summation(2**(-n), (n, 1, oo)) == 1
    assert summation(3**(-n), (n, 4, oo)) == Rational(1, 54)
    assert summation(2**(-4*n + 3), (n, 1, oo)) == Rational(8, 15)
    assert summation(2**(n + 1), (n, 1, b)).expand() == 4*(2**b - 1)

    # issue 6664:
    assert summation(x**n, (n, 0, oo)) == \
        Piecewise((1/(-x + 1), Abs(x) < 1), (Sum(x**n, (n, 0, oo)), True))

    assert summation(-2**n, (n, 0, oo)) is -oo
    assert summation(I**n, (n, 0, oo)) == Sum(I**n, (n, 0, oo))

    # issue 6802:
    assert summation((-1)**(2*x + 2), (x, 0, n)) == n + 1
    assert summation((-2)**(2*x + 2), (x, 0, n)) == 4*4**(n + 1)/S(3) - Rational(4, 3)
    assert summation((-1)**x, (x, 0, n)) == -(-1)**(n + 1)/S(2) + S.Half
    assert summation(y**x, (x, a, b)) == \
        Piecewise((-a + b + 1, Eq(y, 1)), ((y**a - y**(b + 1))/(-y + 1), True))
    assert summation((-2)**(y*x + 2), (x, 0, n)) == \
        4*Piecewise((n + 1, Eq((-2)**y, 1)),
                    ((-(-2)**(y*(n + 1)) + 1)/(-(-2)**y + 1), True))

    # issue 8251:
    assert summation((1/(n + 1)**2)*n**2, (n, 0, oo)) is oo

    #issue 9908:
    assert Sum(1/(n**3 - 1), (n, -oo, -2)).doit() == summation(1/(n**3 - 1), (n, -oo, -2))

    #issue 11642:
    result = Sum(0.5**n, (n, 1, oo)).doit()
    assert result == 1.0
    assert result.is_Float

    result = Sum(0.25**n, (n, 1, oo)).doit()
    assert result == 1/3.
    assert result.is_Float

    result = Sum(0.99999**n, (n, 1, oo)).doit()
    assert result == 99999.0
    assert result.is_Float

    result = Sum(S.Half**n, (n, 1, oo)).doit()
    assert result == 1
    assert not result.is_Float

    result = Sum(Rational(3, 5)**n, (n, 1, oo)).doit()
    assert result == Rational(3, 2)
    assert not result.is_Float

    assert Sum(1.0**n, (n, 1, oo)).doit() is oo
    assert Sum(2.43**n, (n, 1, oo)).doit() is oo

    # Issue 13979
    i, k, q = symbols('i k q', integer=True)
    result = summation(
        exp(-2*I*pi*k*i/n) * exp(2*I*pi*q*i/n) / n, (i, 0, n - 1)
    )
    assert result.simplify() == Piecewise(
            (1, Eq(exp(-2*I*pi*(k - q)/n), 1)), (0, True)
    )

    #Issue 23491
    assert Sum(1/(n**2 + 1), (n, 1, oo)).doit() == S(-1)/2 + pi/(2*tanh(pi))

