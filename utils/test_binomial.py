
def test_binomial():
    x = Symbol('x')
    n = Symbol('n', integer=True)
    nz = Symbol('nz', integer=True, nonzero=True)
    k = Symbol('k', integer=True)
    kp = Symbol('kp', integer=True, positive=True)
    kn = Symbol('kn', integer=True, negative=True)
    u = Symbol('u', negative=True)
    v = Symbol('v', nonnegative=True)
    p = Symbol('p', positive=True)
    z = Symbol('z', zero=True)
    nt = Symbol('nt', integer=False)
    kt = Symbol('kt', integer=False)
    a = Symbol('a', integer=True, nonnegative=True)
    b = Symbol('b', integer=True, nonnegative=True)

    assert binomial(0, 0) == 1
    assert binomial(1, 1) == 1
    assert binomial(10, 10) == 1
    assert binomial(n, z) == 1
    assert binomial(1, 2) == 0
    assert binomial(-1, 2) == 1
    assert binomial(1, -1) == 0
    assert binomial(-1, 1) == -1
    assert binomial(-1, -1) == 0
    assert binomial(S.Half, S.Half) == 1
    assert binomial(-10, 1) == -10
    assert binomial(-10, 7) == -11440
    assert binomial(n, -1) == 0 # holds for all integers (negative, zero, positive)
    assert binomial(kp, -1) == 0
    assert binomial(nz, 0) == 1
    assert expand_func(binomial(n, 1)) == n
    assert expand_func(binomial(n, 2)) == n*(n - 1)/2
    assert expand_func(binomial(n, n - 2)) == n*(n - 1)/2
    assert expand_func(binomial(n, n - 1)) == n
    assert binomial(n, 3).func == binomial
    assert binomial(n, 3).expand(func=True) ==  n**3/6 - n**2/2 + n/3
    assert expand_func(binomial(n, 3)) ==  n*(n - 2)*(n - 1)/6
    assert binomial(n, n).func == binomial # e.g. (-1, -1) == 0, (2, 2) == 1
    assert binomial(n, n + 1).func == binomial  # e.g. (-1, 0) == 1
    assert binomial(kp, kp + 1) == 0
    assert binomial(kn, kn) == 0 # issue #14529
    assert binomial(n, u).func == binomial
    assert binomial(kp, u).func == binomial
    assert binomial(n, p).func == binomial
    assert binomial(n, k).func == binomial
    assert binomial(n, n + p).func == binomial
    assert binomial(kp, kp + p).func == binomial

    assert expand_func(binomial(n, n - 3)) == n*(n - 2)*(n - 1)/6

    assert binomial(n, k).is_integer
    assert binomial(nt, k).is_integer is None
    assert binomial(x, nt).is_integer is False

    assert binomial(gamma(25), 6) == 79232165267303928292058750056084441948572511312165380965440075720159859792344339983120618959044048198214221915637090855535036339620413440000
    assert binomial(1324, 47) == 906266255662694632984994480774946083064699457235920708992926525848438478406790323869952
    assert binomial(1735, 43) == 190910140420204130794758005450919715396159959034348676124678207874195064798202216379800
    assert binomial(2512, 53) == 213894469313832631145798303740098720367984955243020898718979538096223399813295457822575338958939834177325304000
    assert binomial(3383, 52) == 27922807788818096863529701501764372757272890613101645521813434902890007725667814813832027795881839396839287659777235
    assert binomial(4321, 51) == 124595639629264868916081001263541480185227731958274383287107643816863897851139048158022599533438936036467601690983780576

    assert binomial(a, b).is_nonnegative is True
    assert binomial(-1, 2, evaluate=False).is_nonnegative is True
    assert binomial(10, 5, evaluate=False).is_nonnegative is True
    assert binomial(10, -3, evaluate=False).is_nonnegative is True
    assert binomial(-10, -3, evaluate=False).is_nonnegative is True
    assert binomial(-10, 2, evaluate=False).is_nonnegative is True
    assert binomial(-10, 1, evaluate=False).is_nonnegative is False
    assert binomial(-10, 7, evaluate=False).is_nonnegative is False

    # issue #14625
    for _ in (pi, -pi, nt, v, a):
        assert binomial(_, _) == 1
        assert binomial(_, _ - 1) == _
    assert isinstance(binomial(u, u), binomial)
    assert isinstance(binomial(u, u - 1), binomial)
    assert isinstance(binomial(x, x), binomial)
    assert isinstance(binomial(x, x - 1), binomial)

    #issue #18802
    assert expand_func(binomial(x + 1, x)) == x + 1
    assert expand_func(binomial(x, x - 1)) == x
    assert expand_func(binomial(x + 1, x - 1)) == x*(x + 1)/2
    assert expand_func(binomial(x**2 + 1, x**2)) == x**2 + 1

    # issue #13980 and #13981
    assert binomial(-7, -5) == 0
    assert binomial(-23, -12) == 0
    assert binomial(Rational(13, 2), -10) == 0
    assert binomial(-49, -51) == 0

    assert binomial(19, Rational(-7, 2)) == S(-68719476736)/(911337863661225*pi)
    assert binomial(0, Rational(3, 2)) == S(-2)/(3*pi)
    assert binomial(-3, Rational(-7, 2)) is zoo
    assert binomial(kn, kt) is zoo

    assert binomial(nt, kt).func == binomial
    assert binomial(nt, Rational(15, 6)) == 8*gamma(nt + 1)/(15*sqrt(pi)*gamma(nt - Rational(3, 2)))
    assert binomial(Rational(20, 3), Rational(-10, 8)) == gamma(Rational(23, 3))/(gamma(Rational(-1, 4))*gamma(Rational(107, 12)))
    assert binomial(Rational(19, 2), Rational(-7, 2)) == Rational(-1615, 8388608)
    assert binomial(Rational(-13, 5), Rational(-7, 8)) == gamma(Rational(-8, 5))/(gamma(Rational(-29, 40))*gamma(Rational(1, 8)))
    assert binomial(Rational(-19, 8), Rational(-13, 5)) == gamma(Rational(-11, 8))/(gamma(Rational(-8, 5))*gamma(Rational(49, 40)))

    # binomial for complexes
    assert binomial(I, Rational(-89, 8)) == gamma(1 + I)/(gamma(Rational(-81, 8))*gamma(Rational(97, 8) + I))
    assert binomial(I, 2*I) == gamma(1 + I)/(gamma(1 - I)*gamma(1 + 2*I))
    assert binomial(-7, I) is zoo
    assert binomial(Rational(-7, 6), I) == gamma(Rational(-1, 6))/(gamma(Rational(-1, 6) - I)*gamma(1 + I))
    assert binomial((1+2*I), (1+3*I)) == gamma(2 + 2*I)/(gamma(1 - I)*gamma(2 + 3*I))
    assert binomial(I, 5) == Rational(1, 3) - I/S(12)
    assert binomial((2*I + 3), 7) == -13*I/S(63)
    assert isinstance(binomial(I, n), binomial)
    assert expand_func(binomial(3, 2, evaluate=False)) == 3
    assert expand_func(binomial(n, 0, evaluate=False)) == 1
    assert expand_func(binomial(n, -2, evaluate=False)) == 0
    assert expand_func(binomial(n, k)) == binomial(n, k)

