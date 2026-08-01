
def test_assoc_legendre():
    Plm = assoc_legendre
    Q = sqrt(1 - x**2)

    assert Plm(0, 0, x) == 1
    assert Plm(1, 0, x) == x
    assert Plm(1, 1, x) == -Q
    assert Plm(2, 0, x) == (3*x**2 - 1)/2
    assert Plm(2, 1, x) == -3*x*Q
    assert Plm(2, 2, x) == 3*Q**2
    assert Plm(3, 0, x) == (5*x**3 - 3*x)/2
    assert Plm(3, 1, x).expand() == (( 3*(1 - 5*x**2)/2 ).expand() * Q).expand()
    assert Plm(3, 2, x) == 15*x * Q**2
    assert Plm(3, 3, x) == -15 * Q**3

    # negative m
    assert Plm(1, -1, x) == -Plm(1, 1, x)/2
    assert Plm(2, -2, x) == Plm(2, 2, x)/24
    assert Plm(2, -1, x) == -Plm(2, 1, x)/6
    assert Plm(3, -3, x) == -Plm(3, 3, x)/720
    assert Plm(3, -2, x) == Plm(3, 2, x)/120
    assert Plm(3, -1, x) == -Plm(3, 1, x)/12

    n = Symbol("n")
    m = Symbol("m")
    X = Plm(n, m, x)
    assert isinstance(X, assoc_legendre)

    assert Plm(n, 0, x) == legendre(n, x)
    assert Plm(n, m, 0) == 2**m*sqrt(pi)/(gamma(-m/2 - n/2 +
                           S.Half)*gamma(-m/2 + n/2 + 1))

    assert diff(Plm(m, n, x), x) == (m*x*assoc_legendre(m, n, x) -
                (m + n)*assoc_legendre(m - 1, n, x))/(x**2 - 1)

    _k = Dummy('k')
    assert Plm(m, n, x).rewrite(Sum).dummy_eq(
            (1 - x**2)**(n/2)*Sum((-1)**_k*2**(-m)*x**(-2*_k + m - n)*factorial
             (-2*_k + 2*m)/(factorial(_k)*factorial(-_k + m)*factorial(-2*_k + m
              - n)), (_k, 0, floor(m/2 - n/2))))
    assert Plm(m, n, x).rewrite("polynomial").dummy_eq(
            (1 - x**2)**(n/2)*Sum((-1)**_k*2**(-m)*x**(-2*_k + m - n)*factorial
             (-2*_k + 2*m)/(factorial(_k)*factorial(-_k + m)*factorial(-2*_k + m
              - n)), (_k, 0, floor(m/2 - n/2))))
    assert conjugate(assoc_legendre(n, m, x)) == \
        assoc_legendre(n, conjugate(m), conjugate(x))
    raises(ValueError, lambda: Plm(0, 1, x))
    raises(ValueError, lambda: Plm(-1, 1, x))
    raises(ArgumentIndexError, lambda: Plm(n, m, x).fdiff(1))
    raises(ArgumentIndexError, lambda: Plm(n, m, x).fdiff(2))
    raises(ArgumentIndexError, lambda: Plm(n, m, x).fdiff(4))

