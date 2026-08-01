
def test_legendre():
    x, w = gauss_legendre(1, 17)
    assert [str(r) for r in x] == ['0']
    assert [str(r) for r in w] == ['2.0000000000000000']

    x, w = gauss_legendre(2, 17)
    assert [str(r) for r in x] == [
            '-0.57735026918962576',
            '0.57735026918962576']
    assert [str(r) for r in w] == [
            '1.0000000000000000',
            '1.0000000000000000']

    x, w = gauss_legendre(3, 17)
    assert [str(r) for r in x] == [
            '-0.77459666924148338',
            '0',
            '0.77459666924148338']
    assert [str(r) for r in w] == [
            '0.55555555555555556',
            '0.88888888888888889',
            '0.55555555555555556']

    x, w = gauss_legendre(4, 17)
    assert [str(r) for r in x] == [
            '-0.86113631159405258',
            '-0.33998104358485626',
            '0.33998104358485626',
            '0.86113631159405258']
    assert [str(r) for r in w] == [
            '0.34785484513745386',
            '0.65214515486254614',
            '0.65214515486254614',
            '0.34785484513745386']


def test_legendre():
    assert legendre(0, x) == 1
    assert legendre(1, x) == x
    assert legendre(2, x) == ((3*x**2 - 1)/2).expand()
    assert legendre(3, x) == ((5*x**3 - 3*x)/2).expand()
    assert legendre(4, x) == ((35*x**4 - 30*x**2 + 3)/8).expand()
    assert legendre(5, x) == ((63*x**5 - 70*x**3 + 15*x)/8).expand()
    assert legendre(6, x) == ((231*x**6 - 315*x**4 + 105*x**2 - 5)/16).expand()

    assert legendre(10, -1) == 1
    assert legendre(11, -1) == -1
    assert legendre(10, 1) == 1
    assert legendre(11, 1) == 1
    assert legendre(10, 0) != 0
    assert legendre(11, 0) == 0

    assert legendre(-1, x) == 1
    k = Symbol('k')
    assert legendre(5 - k, x).subs(k, 2) == ((5*x**3 - 3*x)/2).expand()

    assert roots(legendre(4, x), x) == {
        sqrt(Rational(3, 7) - Rational(2, 35)*sqrt(30)): 1,
        -sqrt(Rational(3, 7) - Rational(2, 35)*sqrt(30)): 1,
        sqrt(Rational(3, 7) + Rational(2, 35)*sqrt(30)): 1,
        -sqrt(Rational(3, 7) + Rational(2, 35)*sqrt(30)): 1,
    }

    n = Symbol("n")

    X = legendre(n, x)
    assert isinstance(X, legendre)
    assert unchanged(legendre, n, x)

    assert legendre(n, 0) == sqrt(pi)/(gamma(S.Half - n/2)*gamma(n/2 + 1))
    assert legendre(n, 1) == 1
    assert legendre(n, oo) is oo
    assert legendre(-n, x) == legendre(n - 1, x)
    assert legendre(n, -x) == (-1)**n*legendre(n, x)
    assert unchanged(legendre, -n + k, x)

    assert conjugate(legendre(n, x)) == legendre(n, conjugate(x))

    assert diff(legendre(n, x), x) == \
        n*(x*legendre(n, x) - legendre(n - 1, x))/(x**2 - 1)
    assert diff(legendre(n, x), n) == Derivative(legendre(n, x), n)

    _k = Dummy('k')
    assert legendre(n, x).rewrite(Sum).dummy_eq(Sum((-1)**_k*(S.Half -
            x/2)**_k*(x/2 + S.Half)**(-_k + n)*binomial(n, _k)**2, (_k, 0, n)))
    assert legendre(n, x).rewrite("polynomial").dummy_eq(Sum((-1)**_k*(S.Half -
            x/2)**_k*(x/2 + S.Half)**(-_k + n)*binomial(n, _k)**2, (_k, 0, n)))
    raises(ArgumentIndexError, lambda: legendre(n, x).fdiff(1))
    raises(ArgumentIndexError, lambda: legendre(n, x).fdiff(3))

