
def test_beta():
    a, b = symbols('alpha beta', positive=True)
    B = Beta('x', a, b)

    assert pspace(B).domain.set == Interval(0, 1)
    assert characteristic_function(B)(x) == hyper((a,), (a + b,), I*x)
    assert density(B)(x) == x**(a - 1)*(1 - x)**(b - 1)/beta(a, b)

    assert simplify(E(B)) == a / (a + b)
    assert simplify(variance(B)) == a*b / (a**3 + 3*a**2*b + a**2 + 3*a*b**2 + 2*a*b + b**3 + b**2)

    # Full symbolic solution is too much, test with numeric version
    a, b = 1, 2
    B = Beta('x', a, b)
    assert expand_func(E(B)) == a / S(a + b)
    assert expand_func(variance(B)) == (a*b) / S((a + b)**2 * (a + b + 1))
    assert median(B) == FiniteSet(1 - 1/sqrt(2))


def test_beta():
    from sympy.functions.special.beta_functions import beta

    expr = beta(x, y)

    prntr = SciPyPrinter()
    assert prntr.doprint(expr) == 'scipy.special.beta(x, y)'

    prntr = NumPyPrinter()
    assert prntr.doprint(expr) == '(math.gamma(x)*math.gamma(y)/math.gamma(x + y))'

    prntr = PythonCodePrinter()
    assert prntr.doprint(expr) == '(math.gamma(x)*math.gamma(y)/math.gamma(x + y))'

    prntr = PythonCodePrinter({'allow_unknown_functions': True})
    assert prntr.doprint(expr) == '(math.gamma(x)*math.gamma(y)/math.gamma(x + y))'

    prntr = MpmathPrinter()
    assert prntr.doprint(expr) ==  'mpmath.beta(x, y)'


def test_beta():
    assert xpretty(beta(x,y), use_unicode=True) == 'Β(x, y)'
    assert xpretty(beta(x,y), use_unicode=False) == 'B(x, y)'
    assert xpretty(beta, use_unicode=True) == 'Β'
    assert xpretty(beta, use_unicode=False) == 'B'
    mybeta = Function('beta')
    assert xpretty(mybeta(x), use_unicode=True) == 'β(x)'
    assert xpretty(mybeta(x, y, z), use_unicode=False) == 'beta(x, y, z)'
    assert xpretty(mybeta, use_unicode=True) == 'β'


def test_beta():
    a, b, x = symbols("a b x", positive=True)
    e = x**(a - 1)*(-x + 1)**(b - 1)/beta(a, b)
    Q = QQ[a, b].get_field()
    h1 = expr_to_holonomic(e, x, domain=Q)

    _, Dx = DifferentialOperators(Q.old_poly_ring(x), 'Dx')
    h2 = HolonomicFunction((a + x*(-a - b + 2) - 1) + (x**2 - x)*Dx, x)

    assert h1 == h2


def test_beta():
    x, y = symbols('x y')
    t = Dummy('t')

    assert unchanged(beta, x, y)
    assert unchanged(beta, x, x)

    assert beta(5, -3).is_real == True
    assert beta(3, y).is_real is None

    assert expand_func(beta(x, y)) == gamma(x)*gamma(y)/gamma(x + y)
    assert expand_func(beta(x, y) - beta(y, x)) == 0  # Symmetric
    assert expand_func(beta(x, y)) == expand_func(beta(x, y + 1) + beta(x + 1, y)).simplify()

    assert diff(beta(x, y), x) == beta(x, y)*(polygamma(0, x) - polygamma(0, x + y))
    assert diff(beta(x, y), y) == beta(x, y)*(polygamma(0, y) - polygamma(0, x + y))

    assert conjugate(beta(x, y)) == beta(conjugate(x), conjugate(y))

    raises(ArgumentIndexError, lambda: beta(x, y).fdiff(3))

    assert beta(x, y).rewrite(gamma) == gamma(x)*gamma(y)/gamma(x + y)
    assert beta(x).rewrite(gamma) == gamma(x)**2/gamma(2*x)
    assert beta(x, y).rewrite(Integral).dummy_eq(Integral(t**(x - 1) * (1 - t)**(y - 1), (t, 0, 1)))
    assert beta(Rational(-19, 10), Rational(-1, 10)) == S.Zero
    assert beta(Rational(-19, 10), Rational(-9, 10)) == \
        800*2**(S(4)/5)*sqrt(pi)*gamma(S.One/10)/(171*gamma(-S(7)/5))
    assert beta(Rational(19, 10), Rational(29, 10)) == 100/(551*catalan(Rational(19, 10)))
    assert beta(1, 0) == S.ComplexInfinity
    assert beta(0, 1) == S.ComplexInfinity
    assert beta(2, 3) == S.One/12
    assert unchanged(beta, x, x + 1)
    assert unchanged(beta, x, 1)
    assert unchanged(beta, 1, y)
    assert beta(x, x + 1).doit() == 1/(x*(x+1)*catalan(x))
    assert beta(1, y).doit() == 1/y
    assert beta(x, 1).doit() == 1/x
    assert beta(Rational(-19, 10), Rational(-1, 10), evaluate=False).doit() == S.Zero
    assert beta(2) == beta(2, 2)
    assert beta(x, evaluate=False) != beta(x, x)
    assert beta(x, evaluate=False).doit() == beta(x, x)


def test_beta():
    """
    Test fitting beta shape parameters to interval-censored data.

    Calculation in R:

    > library(fitdistrplus)
    > data <- data.frame(left=c(0.10, 0.50, 0.75, 0.80),
    +                    right=c(0.20, 0.55, 0.90, 0.95))
    > result = fitdistcens(data, 'beta', control=list(reltol=1e-14))

    > result
    Fitting of the distribution ' beta ' on censored data by maximum likelihood
    Parameters:
           estimate
    shape1 1.419941
    shape2 1.027066
    > result$sd
       shape1    shape2
    0.9914177 0.6866565
    """
    data = CensoredData(interval=[[0.10, 0.20],
                                  [0.50, 0.55],
                                  [0.75, 0.90],
                                  [0.80, 0.95]])

    # For this test, fit only the shape parameters; loc and scale are fixed.
    a, b, loc, scale = beta.fit(data, floc=0, fscale=1, optimizer=optimizer)

    assert_allclose(a, 1.419941, rtol=5e-6)
    assert_allclose(b, 1.027066, rtol=5e-6)
    assert loc == 0
    assert scale == 1


def test_beta():
    np.random.seed(1234)

    b = np.r_[np.logspace(-200, 200, 4),
              np.logspace(-10, 10, 4),
              np.logspace(-1, 1, 4),
              np.arange(-10, 11, 1),
              np.arange(-10, 11, 1) + 0.5,
              -1, -2.3, -3, -100.3, -10003.4]
    a = b

    ab = np.array(np.broadcast_arrays(a[:,None], b[None,:])).reshape(2, -1).T

    old_dps, old_prec = mpmath.mp.dps, mpmath.mp.prec
    try:
        mpmath.mp.dps = 400

        assert_func_equal(sc.beta,
                          lambda a, b: float(mpmath.beta(a, b)),
                          ab,
                          vectorized=False,
                          rtol=1e-10,
                          ignore_inf_sign=True)

        assert_func_equal(
            sc.betaln,
            lambda a, b: float(mpmath.log(abs(mpmath.beta(a, b)))),
            ab,
            vectorized=False,
            rtol=1e-10)
    finally:
        mpmath.mp.dps, mpmath.mp.prec = old_dps, old_prec

