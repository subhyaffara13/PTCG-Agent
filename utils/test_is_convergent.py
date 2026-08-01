
def test_is_convergent():
    # divergence tests --
    assert Sum(n/(2*n + 1), (n, 1, oo)).is_convergent() is S.false
    assert Sum(factorial(n)/5**n, (n, 1, oo)).is_convergent() is S.false
    assert Sum(3**(-2*n - 1)*n**n, (n, 1, oo)).is_convergent() is S.false
    assert Sum((-1)**n*n, (n, 3, oo)).is_convergent() is S.false
    assert Sum((-1)**n, (n, 1, oo)).is_convergent() is S.false
    assert Sum(log(1/n), (n, 2, oo)).is_convergent() is S.false
    assert Sum(sin(n), (n, 1, oo)).is_convergent() is S.false

    # Raabe's test --
    assert Sum(Product((3*m),(m,1,n))/Product((3*m+4),(m,1,n)),(n,1,oo)).is_convergent() is S.true

    # root test --
    assert Sum((-12)**n/n, (n, 1, oo)).is_convergent() is S.false

    # integral test --

    # p-series test --
    assert Sum(1/(n**2 + 1), (n, 1, oo)).is_convergent() is S.true
    assert Sum(1/n**Rational(6, 5), (n, 1, oo)).is_convergent() is S.true
    assert Sum(2/(n*sqrt(n - 1)), (n, 2, oo)).is_convergent() is S.true
    assert Sum(1/(sqrt(n)*sqrt(n)), (n, 2, oo)).is_convergent() is S.false
    assert Sum(factorial(n) / factorial(n+2), (n, 1, oo)).is_convergent() is S.true
    assert Sum(rf(5,n)/rf(7,n),(n,1,oo)).is_convergent() is S.true
    assert Sum((rf(1, n)*rf(2, n))/(rf(3, n)*factorial(n)),(n,1,oo)).is_convergent() is S.false

    # comparison test --
    assert Sum(1/(n + log(n)), (n, 1, oo)).is_convergent() is S.false
    assert Sum(1/(n**2*log(n)), (n, 2, oo)).is_convergent() is S.true
    assert Sum(1/(n*log(n)), (n, 2, oo)).is_convergent() is S.false
    assert Sum(2/(n*log(n)*log(log(n))**2), (n, 5, oo)).is_convergent() is S.true
    assert Sum(2/(n*log(n)**2), (n, 2, oo)).is_convergent() is S.true
    assert Sum((n - 1)/(n**2*log(n)**3), (n, 2, oo)).is_convergent() is S.true
    assert Sum(1/(n*log(n)*log(log(n))), (n, 5, oo)).is_convergent() is S.false
    assert Sum((n - 1)/(n*log(n)**3), (n, 3, oo)).is_convergent() is S.false
    assert Sum(2/(n**2*log(n)), (n, 2, oo)).is_convergent() is S.true
    assert Sum(1/(n*sqrt(log(n))*log(log(n))), (n, 100, oo)).is_convergent() is S.false
    assert Sum(log(log(n))/(n*log(n)**2), (n, 100, oo)).is_convergent() is S.true
    assert Sum(log(n)/n**2, (n, 5, oo)).is_convergent() is S.true

    # alternating series tests --
    assert Sum((-1)**(n - 1)/(n**2 - 1), (n, 3, oo)).is_convergent() is S.true

    # with -negativeInfinite Limits
    assert Sum(1/(n**2 + 1), (n, -oo, 1)).is_convergent() is S.true
    assert Sum(1/(n - 1), (n, -oo, -1)).is_convergent() is S.false
    assert Sum(1/(n**2 - 1), (n, -oo, -5)).is_convergent() is S.true
    assert Sum(1/(n**2 - 1), (n, -oo, 2)).is_convergent() is S.true
    assert Sum(1/(n**2 - 1), (n, -oo, oo)).is_convergent() is S.true

    # piecewise functions
    f = Piecewise((n**(-2), n <= 1), (n**2, n > 1))
    assert Sum(f, (n, 1, oo)).is_convergent() is S.false
    assert Sum(f, (n, -oo, oo)).is_convergent() is S.false
    assert Sum(f, (n, 1, 100)).is_convergent() is S.true
    #assert Sum(f, (n, -oo, 1)).is_convergent() is S.true

    # integral test

    assert Sum(log(n)/n**3, (n, 1, oo)).is_convergent() is S.true
    assert Sum(-log(n)/n**3, (n, 1, oo)).is_convergent() is S.true
    # the following function has maxima located at (x, y) =
    # (1.2, 0.43), (3.0, -0.25) and (6.8, 0.050)
    eq = (x - 2)*(x**2 - 6*x + 4)*exp(-x)
    assert Sum(eq, (x, 1, oo)).is_convergent() is S.true
    assert Sum(eq, (x, 1, 2)).is_convergent() is S.true
    assert Sum(1/(x**3), (x, 1, oo)).is_convergent() is S.true
    assert Sum(1/(x**S.Half), (x, 1, oo)).is_convergent() is S.false

    # issue 19545
    assert Sum(1/n - 3/(3*n +2), (n, 1, oo)).is_convergent() is S.true

    # issue 19836
    assert Sum(4/(n + 2) - 5/(n + 1) + 1/n,(n, 7, oo)).is_convergent() is S.true

