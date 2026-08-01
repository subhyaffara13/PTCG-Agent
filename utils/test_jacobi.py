
def test_jacobi():
    x, w = gauss_jacobi(1, Rational(-1, 2), S.Half, 17)
    assert [str(r) for r in x] == ['0.50000000000000000']
    assert [str(r) for r in w] == ['3.1415926535897932']

    x, w = gauss_jacobi(2, Rational(-1, 2), S.Half, 17)
    assert [str(r) for r in x] == [
            '-0.30901699437494742',
            '0.80901699437494742']
    assert [str(r) for r in w] == [
            '0.86831485369082398',
            '2.2732777998989693']

    x, w = gauss_jacobi(3, Rational(-1, 2), S.Half, 17)
    assert [str(r) for r in x] == [
            '-0.62348980185873353',
            '0.22252093395631440',
            '0.90096886790241913']
    assert [str(r) for r in w] == [
            '0.33795476356635433',
            '1.0973322242791115',
            '1.7063056657443274']

    x, w = gauss_jacobi(4, Rational(-1, 2), S.Half, 17)
    assert [str(r) for r in x] == [
            '-0.76604444311897804',
            '-0.17364817766693035',
            '0.50000000000000000',
            '0.93969262078590838']
    assert [str(r) for r in w] == [
            '0.16333179083642836',
            '0.57690240318269103',
            '1.0471975511965977',
            '1.3541609083740761']

    x, w = gauss_jacobi(5, Rational(-1, 2), S.Half, 17)
    assert [str(r) for r in x] == [
            '-0.84125353283118117',
            '-0.41541501300188643',
            '0.14231483827328514',
            '0.65486073394528506',
            '0.95949297361449739']
    assert [str(r) for r in w] == [
            '0.090675770007435372',
            '0.33391416373675607',
            '0.65248870981926643',
            '0.94525424081394926',
            '1.1192597692123861']

    x, w = gauss_jacobi(1, 2, 3, 17)
    assert [str(r) for r in x] == ['0.14285714285714286']
    assert [str(r) for r in w] == ['1.0666666666666667']

    x, w = gauss_jacobi(2, 2, 3, 17)
    assert [str(r) for r in x] == [
            '-0.24025307335204215',
            '0.46247529557426437']
    assert [str(r) for r in w] == [
            '0.48514624517838660',
            '0.58152042148828007']

    x, w = gauss_jacobi(3, 2, 3, 17)
    assert [str(r) for r in x] == [
            '-0.46115870378089762',
            '0.10438533038323902',
            '0.62950064612493132']
    assert [str(r) for r in w] == [
            '0.17937613502213266',
            '0.61595640991147154',
            '0.27133412173306246']

    x, w = gauss_jacobi(4, 2, 3, 17)
    assert [str(r) for r in x] == [
            '-0.59903470850824782',
            '-0.14761105199952565',
            '0.32554377081188859',
            '0.72879429738819258']
    assert [str(r) for r in w] == [
            '0.067809641836772187',
            '0.38956404952032481',
            '0.47995970868024150',
            '0.12933326662932816']

    x, w = gauss_jacobi(5, 2, 3, 17)
    assert [str(r) for r in x] == [
            '-0.69045775012676106',
            '-0.32651993134900065',
            '0.082337849552034905',
            '0.47517887061283164',
            '0.79279429464422850']
    assert [str(r) for r in w] == [
            '0.027410178066337099',
            '0.21291786060364828',
            '0.43908437944395081',
            '0.32220656547221822',
            '0.065047683080512268']


def test_jacobi():
    n = Symbol("n")
    a = Symbol("a")
    b = Symbol("b")

    assert jacobi(0, a, b, x) == 1
    assert jacobi(1, a, b, x) == a/2 - b/2 + x*(a/2 + b/2 + 1)

    assert jacobi(n, a, a, x) == RisingFactorial(
        a + 1, n)*gegenbauer(n, a + S.Half, x)/RisingFactorial(2*a + 1, n)
    assert jacobi(n, a, -a, x) == ((-1)**a*(-x + 1)**(-a/2)*(x + 1)**(a/2)*assoc_legendre(n, a, x)*
                                   factorial(-a + n)*gamma(a + n + 1)/(factorial(a + n)*gamma(n + 1)))
    assert jacobi(n, -b, b, x) == ((-x + 1)**(b/2)*(x + 1)**(-b/2)*assoc_legendre(n, b, x)*
                                   gamma(-b + n + 1)/gamma(n + 1))
    assert jacobi(n, 0, 0, x) == legendre(n, x)
    assert jacobi(n, S.Half, S.Half, x) == RisingFactorial(
        Rational(3, 2), n)*chebyshevu(n, x)/factorial(n + 1)
    assert jacobi(n, Rational(-1, 2), Rational(-1, 2), x) == RisingFactorial(
        S.Half, n)*chebyshevt(n, x)/factorial(n)

    X = jacobi(n, a, b, x)
    assert isinstance(X, jacobi)

    assert jacobi(n, a, b, -x) == (-1)**n*jacobi(n, b, a, x)
    assert jacobi(n, a, b, 0) == 2**(-n)*gamma(a + n + 1)*hyper(
        (-b - n, -n), (a + 1,), -1)/(factorial(n)*gamma(a + 1))
    assert jacobi(n, a, b, 1) == RisingFactorial(a + 1, n)/factorial(n)

    m = Symbol("m", positive=True)
    assert jacobi(m, a, b, oo) == oo*RisingFactorial(a + b + m + 1, m)
    assert unchanged(jacobi, n, a, b, oo)

    assert conjugate(jacobi(m, a, b, x)) == \
        jacobi(m, conjugate(a), conjugate(b), conjugate(x))

    _k = Dummy('k')
    assert diff(jacobi(n, a, b, x), n) == Derivative(jacobi(n, a, b, x), n)
    assert diff(jacobi(n, a, b, x), a).dummy_eq(Sum((jacobi(n, a, b, x) +
        (2*_k + a + b + 1)*RisingFactorial(_k + b + 1, -_k + n)*jacobi(_k, a,
        b, x)/((-_k + n)*RisingFactorial(_k + a + b + 1, -_k + n)))/(_k + a
        + b + n + 1), (_k, 0, n - 1)))
    assert diff(jacobi(n, a, b, x), b).dummy_eq(Sum(((-1)**(-_k + n)*(2*_k +
        a + b + 1)*RisingFactorial(_k + a + 1, -_k + n)*jacobi(_k, a, b, x)/
        ((-_k + n)*RisingFactorial(_k + a + b + 1, -_k + n)) + jacobi(n, a,
        b, x))/(_k + a + b + n + 1), (_k, 0, n - 1)))
    assert diff(jacobi(n, a, b, x), x) == \
        (a/2 + b/2 + n/2 + S.Half)*jacobi(n - 1, a + 1, b + 1, x)

    assert jacobi_normalized(n, a, b, x) == \
           (jacobi(n, a, b, x)/sqrt(2**(a + b + 1)*gamma(a + n + 1)*gamma(b + n + 1)
                                    /((a + b + 2*n + 1)*factorial(n)*gamma(a + b + n + 1))))

    raises(ValueError, lambda: jacobi(-2.1, a, b, x))
    raises(ValueError, lambda: jacobi(Dummy(positive=True, integer=True), 1, 2, oo))

    assert jacobi(n, a, b, x).rewrite(Sum).dummy_eq(Sum((S.Half - x/2)
        **_k*RisingFactorial(-n, _k)*RisingFactorial(_k + a + 1, -_k + n)*
        RisingFactorial(a + b + n + 1, _k)/factorial(_k), (_k, 0, n))/factorial(n))
    assert jacobi(n, a, b, x).rewrite("polynomial").dummy_eq(Sum((S.Half - x/2)
        **_k*RisingFactorial(-n, _k)*RisingFactorial(_k + a + 1, -_k + n)*
        RisingFactorial(a + b + n + 1, _k)/factorial(_k), (_k, 0, n))/factorial(n))
    raises(ArgumentIndexError, lambda: jacobi(n, a, b, x).fdiff(5))

