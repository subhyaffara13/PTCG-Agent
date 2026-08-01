
def test_hermite():
    x, w = gauss_hermite(1, 17)
    assert [str(r) for r in x] == ['0']
    assert [str(r) for r in w] == ['1.7724538509055160']

    x, w = gauss_hermite(2, 17)
    assert [str(r) for r in x] == [
            '-0.70710678118654752',
            '0.70710678118654752']
    assert [str(r) for r in w] == [
            '0.88622692545275801',
            '0.88622692545275801']

    x, w = gauss_hermite(3, 17)
    assert [str(r) for r in x] == [
            '-1.2247448713915890',
            '0',
            '1.2247448713915890']
    assert [str(r) for r in w] == [
            '0.29540897515091934',
            '1.1816359006036774',
            '0.29540897515091934']

    x, w = gauss_hermite(4, 17)
    assert [str(r) for r in x] == [
            '-1.6506801238857846',
            '-0.52464762327529032',
            '0.52464762327529032',
            '1.6506801238857846']
    assert [str(r) for r in w] == [
            '0.081312835447245177',
            '0.80491409000551284',
            '0.80491409000551284',
            '0.081312835447245177']

    x, w = gauss_hermite(5, 17)
    assert [str(r) for r in x] == [
            '-2.0201828704560856',
            '-0.95857246461381851',
            '0',
            '0.95857246461381851',
            '2.0201828704560856']
    assert [str(r) for r in w] == [
            '0.019953242059045913',
            '0.39361932315224116',
            '0.94530872048294188',
            '0.39361932315224116',
            '0.019953242059045913']


def test_hermite():
    assert hermite(0, x) == 1
    assert hermite(1, x) == 2*x
    assert hermite(2, x) == 4*x**2 - 2
    assert hermite(3, x) == 8*x**3 - 12*x
    assert hermite(4, x) == 16*x**4 - 48*x**2 + 12
    assert hermite(6, x) == 64*x**6 - 480*x**4 + 720*x**2 - 120

    n = Symbol("n")
    assert unchanged(hermite, n, x)
    assert hermite(n, -x) == (-1)**n*hermite(n, x)
    assert unchanged(hermite, -n, x)

    assert hermite(n, 0) == 2**n*sqrt(pi)/gamma(S.Half - n/2)
    assert hermite(n, oo) is oo

    assert conjugate(hermite(n, x)) == hermite(n, conjugate(x))

    _k = Dummy('k')
    assert hermite(n, x).rewrite(Sum).dummy_eq(factorial(n)*Sum((-1)
        **_k*(2*x)**(-2*_k + n)/(factorial(_k)*factorial(-2*_k + n)), (_k,
        0, floor(n/2))))
    assert hermite(n, x).rewrite("polynomial").dummy_eq(factorial(n)*Sum((-1)
        **_k*(2*x)**(-2*_k + n)/(factorial(_k)*factorial(-2*_k + n)), (_k,
        0, floor(n/2))))

    assert diff(hermite(n, x), x) == 2*n*hermite(n - 1, x)
    assert diff(hermite(n, x), n) == Derivative(hermite(n, x), n)
    raises(ArgumentIndexError, lambda: hermite(n, x).fdiff(3))

    assert hermite(n, x).rewrite(hermite_prob) == \
            sqrt(2)**n * hermite_prob(n, x*sqrt(2))


def test_hermite():
    mp.dps = 15
    assert hermite(-2, 0).ae(0.5)
    assert hermite(-1, 0).ae(0.88622692545275801365)
    assert hermite(0, 0).ae(1)
    assert hermite(1, 0) == 0
    assert hermite(2, 0).ae(-2)
    assert hermite(0, 2).ae(1)
    assert hermite(1, 2).ae(4)
    assert hermite(1, -2).ae(-4)
    assert hermite(2, -2).ae(14)
    assert hermite(0.5, 0).ae(0.69136733903629335053)
    assert hermite(9, 0) == 0
    assert hermite(4,4).ae(3340)
    assert hermite(3,4).ae(464)
    assert hermite(-4,4).ae(0.00018623860287512396181)
    assert hermite(-3,4).ae(0.0016540169879668766270)
    assert hermite(9, 2.5j).ae(13638725j)
    assert hermite(9, -2.5j).ae(-13638725j)
    assert hermite(9, 100).ae(511078883759363024000)
    assert hermite(9, -100).ae(-511078883759363024000)
    assert hermite(9, 100j).ae(512922083920643024000j)
    assert hermite(9, -100j).ae(-512922083920643024000j)
    assert hermite(-9.5, 2.5j).ae(-2.9004951258126778174e-6 + 1.7601372934039951100e-6j)
    assert hermite(-9.5, -2.5j).ae(-2.9004951258126778174e-6 - 1.7601372934039951100e-6j)
    assert hermite(-9.5, 100).ae(1.3776300722767084162e-22, abs_eps=0, rel_eps=eps)
    assert hermite(-9.5, -100).ae('1.3106082028470671626e4355')
    assert hermite(-9.5, 100j).ae(-9.7900218581864768430e-23 - 9.7900218581864768430e-23j, abs_eps=0, rel_eps=eps)
    assert hermite(-9.5, -100j).ae(-9.7900218581864768430e-23 + 9.7900218581864768430e-23j, abs_eps=0, rel_eps=eps)
    assert hermite(2+3j, -1-j).ae(851.3677063883687676 - 1496.4373467871007997j)

