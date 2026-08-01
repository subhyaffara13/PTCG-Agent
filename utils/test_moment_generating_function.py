
def test_moment_generating_function():
    t = symbols('t', positive=True)

    # Symbolic tests
    a, b, c = symbols('a b c')

    mgf = moment_generating_function(Beta('x', a, b))(t)
    assert mgf == hyper((a,), (a + b,), t)

    mgf = moment_generating_function(Chi('x', a))(t)
    assert mgf == sqrt(2)*t*gamma(a/2 + S.Half)*\
        hyper((a/2 + S.Half,), (Rational(3, 2),), t**2/2)/gamma(a/2) +\
        hyper((a/2,), (S.Half,), t**2/2)

    mgf = moment_generating_function(ChiSquared('x', a))(t)
    assert mgf == (1 - 2*t)**(-a/2)

    mgf = moment_generating_function(Erlang('x', a, b))(t)
    assert mgf == (1 - t/b)**(-a)

    mgf = moment_generating_function(ExGaussian("x", a, b, c))(t)
    assert mgf == exp(a*t + b**2*t**2/2)/(1 - t/c)

    mgf = moment_generating_function(Exponential('x', a))(t)
    assert mgf == a/(a - t)

    mgf = moment_generating_function(Gamma('x', a, b))(t)
    assert mgf == (-b*t + 1)**(-a)

    mgf = moment_generating_function(Gumbel('x', a, b))(t)
    assert mgf == exp(b*t)*gamma(-a*t + 1)

    mgf = moment_generating_function(Gompertz('x', a, b))(t)
    assert mgf == b*exp(b)*expint(t/a, b)

    mgf = moment_generating_function(Laplace('x', a, b))(t)
    assert mgf == exp(a*t)/(-b**2*t**2 + 1)

    mgf = moment_generating_function(Logistic('x', a, b))(t)
    assert mgf == exp(a*t)*beta(-b*t + 1, b*t + 1)

    mgf = moment_generating_function(Normal('x', a, b))(t)
    assert mgf == exp(a*t + b**2*t**2/2)

    mgf = moment_generating_function(Pareto('x', a, b))(t)
    assert mgf == b*(-a*t)**b*uppergamma(-b, -a*t)

    mgf = moment_generating_function(QuadraticU('x', a, b))(t)
    assert str(mgf) == ("(3*(t*(-4*b + (a + b)**2) + 4)*exp(b*t) - "
    "3*(t*(a**2 + 2*a*(b - 2) + b**2) + 4)*exp(a*t))/(t**2*(a - b)**3)")

    mgf = moment_generating_function(RaisedCosine('x', a, b))(t)
    assert mgf == pi**2*exp(a*t)*sinh(b*t)/(b*t*(b**2*t**2 + pi**2))

    mgf = moment_generating_function(Rayleigh('x', a))(t)
    assert mgf == sqrt(2)*sqrt(pi)*a*t*(erf(sqrt(2)*a*t/2) + 1)\
        *exp(a**2*t**2/2)/2 + 1

    mgf = moment_generating_function(Triangular('x', a, b, c))(t)
    assert str(mgf) == ("(-2*(-a + b)*exp(c*t) + 2*(-a + c)*exp(b*t) + "
    "2*(b - c)*exp(a*t))/(t**2*(-a + b)*(-a + c)*(b - c))")

    mgf = moment_generating_function(Uniform('x', a, b))(t)
    assert mgf == (-exp(a*t) + exp(b*t))/(t*(-a + b))

    mgf = moment_generating_function(UniformSum('x', a))(t)
    assert mgf == ((exp(t) - 1)/t)**a

    mgf = moment_generating_function(WignerSemicircle('x', a))(t)
    assert mgf == 2*besseli(1, a*t)/(a*t)

    # Numeric tests

    mgf = moment_generating_function(Beta('x', 1, 1))(t)
    assert mgf.diff(t).subs(t, 1) == hyper((2,), (3,), 1)/2

    mgf = moment_generating_function(Chi('x', 1))(t)
    assert mgf.diff(t).subs(t, 1) == sqrt(2)*hyper((1,), (Rational(3, 2),), S.Half
    )/sqrt(pi) + hyper((Rational(3, 2),), (Rational(3, 2),), S.Half) + 2*sqrt(2)*hyper((2,),
    (Rational(5, 2),), S.Half)/(3*sqrt(pi))

    mgf = moment_generating_function(ChiSquared('x', 1))(t)
    assert mgf.diff(t).subs(t, 1) == I

    mgf = moment_generating_function(Erlang('x', 1, 1))(t)
    assert mgf.diff(t).subs(t, 0) == 1

    mgf = moment_generating_function(ExGaussian("x", 0, 1, 1))(t)
    assert mgf.diff(t).subs(t, 2) == -exp(2)

    mgf = moment_generating_function(Exponential('x', 1))(t)
    assert mgf.diff(t).subs(t, 0) == 1

    mgf = moment_generating_function(Gamma('x', 1, 1))(t)
    assert mgf.diff(t).subs(t, 0) == 1

    mgf = moment_generating_function(Gumbel('x', 1, 1))(t)
    assert mgf.diff(t).subs(t, 0) == EulerGamma + 1

    mgf = moment_generating_function(Gompertz('x', 1, 1))(t)
    assert mgf.diff(t).subs(t, 1) == -e*meijerg(((), (1, 1)),
    ((0, 0, 0), ()), 1)

    mgf = moment_generating_function(Laplace('x', 1, 1))(t)
    assert mgf.diff(t).subs(t, 0) == 1

    mgf = moment_generating_function(Logistic('x', 1, 1))(t)
    assert mgf.diff(t).subs(t, 0) == beta(1, 1)

    mgf = moment_generating_function(Normal('x', 0, 1))(t)
    assert mgf.diff(t).subs(t, 1) == exp(S.Half)

    mgf = moment_generating_function(Pareto('x', 1, 1))(t)
    assert mgf.diff(t).subs(t, 0) == expint(1, 0)

    mgf = moment_generating_function(QuadraticU('x', 1, 2))(t)
    assert mgf.diff(t).subs(t, 1) == -12*e - 3*exp(2)

    mgf = moment_generating_function(RaisedCosine('x', 1, 1))(t)
    assert mgf.diff(t).subs(t, 1) == -2*e*pi**2*sinh(1)/\
    (1 + pi**2)**2 + e*pi**2*cosh(1)/(1 + pi**2)

    mgf = moment_generating_function(Rayleigh('x', 1))(t)
    assert mgf.diff(t).subs(t, 0) == sqrt(2)*sqrt(pi)/2

    mgf = moment_generating_function(Triangular('x', 1, 3, 2))(t)
    assert mgf.diff(t).subs(t, 1) == -e + exp(3)

    mgf = moment_generating_function(Uniform('x', 0, 1))(t)
    assert mgf.diff(t).subs(t, 1) == 1

    mgf = moment_generating_function(UniformSum('x', 1))(t)
    assert mgf.diff(t).subs(t, 1) == 1

    mgf = moment_generating_function(WignerSemicircle('x', 1))(t)
    assert mgf.diff(t).subs(t, 1) == -2*besseli(1, 1) + besseli(2, 1) +\
        besseli(0, 1)


def test_moment_generating_function():

    X = Normal('X',0,1)
    Y = DiscreteUniform('Y', [1,2,7])
    Z = Poisson('Z', 2)
    t = symbols('_t')
    P = Lambda(t, exp(t**2/2))
    Q = Lambda(t, (exp(7*t)/3 + exp(2*t)/3 + exp(t)/3))
    R = Lambda(t, exp(2 * exp(t) - 2))


    assert moment_generating_function(X).dummy_eq(P)
    assert moment_generating_function(Y).dummy_eq(Q)
    assert moment_generating_function(Z).dummy_eq(R)

