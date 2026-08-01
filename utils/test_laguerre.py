
def test_laguerre():
    x, w = gauss_laguerre(1, 17)
    assert [str(r) for r in x] == ['1.0000000000000000']
    assert [str(r) for r in w] == ['1.0000000000000000']

    x, w = gauss_laguerre(2, 17)
    assert [str(r) for r in x] == [
            '0.58578643762690495',
            '3.4142135623730950']
    assert [str(r) for r in w] == [
            '0.85355339059327376',
            '0.14644660940672624']

    x, w = gauss_laguerre(3, 17)
    assert [str(r) for r in x] == [
            '0.41577455678347908',
            '2.2942803602790417',
            '6.2899450829374792',
            ]
    assert [str(r) for r in w] == [
            '0.71109300992917302',
            '0.27851773356924085',
            '0.010389256501586136',
            ]

    x, w = gauss_laguerre(4, 17)
    assert [str(r) for r in x] == [
            '0.32254768961939231',
            '1.7457611011583466',
            '4.5366202969211280',
            '9.3950709123011331']
    assert [str(r) for r in w] == [
            '0.60315410434163360',
            '0.35741869243779969',
            '0.038887908515005384',
            '0.00053929470556132745']

    x, w = gauss_laguerre(5, 17)
    assert [str(r) for r in x] == [
            '0.26356031971814091',
            '1.4134030591065168',
            '3.5964257710407221',
            '7.0858100058588376',
            '12.640800844275783']
    assert [str(r) for r in w] == [
            '0.52175561058280865',
            '0.39866681108317593',
            '0.075942449681707595',
            '0.0036117586799220485',
            '2.3369972385776228e-5']


def test_laguerre():
    n = Symbol("n")
    m = Symbol("m", negative=True)

    # Laguerre polynomials:
    assert laguerre(0, x) == 1
    assert laguerre(1, x) == -x + 1
    assert laguerre(2, x) == x**2/2 - 2*x + 1
    assert laguerre(3, x) == -x**3/6 + 3*x**2/2 - 3*x + 1
    assert laguerre(-2, x) == (x + 1)*exp(x)

    X = laguerre(n, x)
    assert isinstance(X, laguerre)

    assert laguerre(n, 0) == 1
    assert laguerre(n, oo) == (-1)**n*oo
    assert laguerre(n, -oo) is oo

    assert conjugate(laguerre(n, x)) == laguerre(n, conjugate(x))

    _k = Dummy('k')

    assert laguerre(n, x).rewrite(Sum).dummy_eq(
        Sum(x**_k*RisingFactorial(-n, _k)/factorial(_k)**2, (_k, 0, n)))
    assert laguerre(n, x).rewrite("polynomial").dummy_eq(
        Sum(x**_k*RisingFactorial(-n, _k)/factorial(_k)**2, (_k, 0, n)))
    assert laguerre(m, x).rewrite(Sum).dummy_eq(
        exp(x)*Sum((-x)**_k*RisingFactorial(m + 1, _k)/factorial(_k)**2,
            (_k, 0, -m - 1)))
    assert laguerre(m, x).rewrite("polynomial").dummy_eq(
        exp(x)*Sum((-x)**_k*RisingFactorial(m + 1, _k)/factorial(_k)**2,
            (_k, 0, -m - 1)))

    assert diff(laguerre(n, x), x) == -assoc_laguerre(n - 1, 1, x)

    k = Symbol('k')
    assert laguerre(-n, x) == exp(x)*laguerre(n - 1, -x)
    assert laguerre(-3, x) == exp(x)*laguerre(2, -x)
    assert unchanged(laguerre, -n + k, x)

    raises(ValueError, lambda: laguerre(-2.1, x))
    raises(ValueError, lambda: laguerre(Rational(5, 2), x))
    raises(ArgumentIndexError, lambda: laguerre(n, x).fdiff(1))
    raises(ArgumentIndexError, lambda: laguerre(n, x).fdiff(3))

