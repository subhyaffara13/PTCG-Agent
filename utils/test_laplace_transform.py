import re

def test_laplace_transform():
    LT = laplace_transform
    ILT = inverse_laplace_transform
    a, b, c = symbols('a, b, c', positive=True)
    np = symbols('np', integer=True, positive=True)
    t, w, x = symbols('t, w, x')
    f = Function('f')
    F = Function('F')
    g = Function('g')
    y = Function('y')
    Y = Function('Y')

    # Test helper functions
    assert (
        _laplace_deep_collect(exp((t+a)*(t+b)) +
                              besselj(2, exp((t+a)*(t+b)-t**2)), t) ==
        exp(a*b + t**2 + t*(a + b)) + besselj(2, exp(a*b + t*(a + b))))
    L = laplace_transform(diff(y(t), t, 3), t, s, noconds=True)
    L = laplace_correspondence(L, {y: Y})
    L = laplace_initial_conds(L, t, {y: [2, 4, 8, 16, 32]})
    assert L == s**3*Y(s) - 2*s**2 - 4*s - 8
    # Test whether `noconds=True` in `doit`:
    assert (2*LaplaceTransform(exp(t), t, s) - 1).doit() == -1 + 2/(s - 1)
    assert (LT(a*t+t**2+t**(S(5)/2), t, s) ==
            (a/s**2 + 2/s**3 + 15*sqrt(pi)/(8*s**(S(7)/2)), 0, True))
    assert LT(b/(t+a), t, s) == (-b*exp(-a*s)*Ei(-a*s), 0, True)
    assert (LT(1/sqrt(t+a), t, s) ==
            (sqrt(pi)*sqrt(1/s)*exp(a*s)*erfc(sqrt(a)*sqrt(s)), 0, True))
    assert (LT(sqrt(t)/(t+a), t, s) ==
            (-pi*sqrt(a)*exp(a*s)*erfc(sqrt(a)*sqrt(s)) + sqrt(pi)*sqrt(1/s),
             0, True))
    assert (LT((t+a)**(-S(3)/2), t, s) ==
            (-2*sqrt(pi)*sqrt(s)*exp(a*s)*erfc(sqrt(a)*sqrt(s)) + 2/sqrt(a),
             0, True))
    assert (LT(t**(S(1)/2)*(t+a)**(-1), t, s) ==
            (-pi*sqrt(a)*exp(a*s)*erfc(sqrt(a)*sqrt(s)) + sqrt(pi)*sqrt(1/s),
             0, True))
    assert (LT(1/(a*sqrt(t) + t**(3/2)), t, s) ==
            (pi*sqrt(a)*exp(a*s)*erfc(sqrt(a)*sqrt(s)), 0, True))
    assert (LT((t+a)**b, t, s) ==
            (s**(-b - 1)*exp(-a*s)*uppergamma(b + 1, a*s), 0, True))
    assert LT(t**5/(t+a), t, s) == (120*a**5*uppergamma(-5, a*s), 0, True)
    assert LT(exp(t), t, s) == (1/(s - 1), 1, True)
    assert LT(exp(2*t), t, s) == (1/(s - 2), 2, True)
    assert LT(exp(a*t), t, s) == (1/(s - a), a, True)
    assert LT(exp(a*(t-b)), t, s) == (exp(-a*b)/(-a + s), a, True)
    assert LT(t*exp(-a*(t)), t, s) == ((a + s)**(-2), -a, True)
    assert LT(t*exp(-a*(t-b)), t, s) == (exp(a*b)/(a + s)**2, -a, True)
    assert LT(b*t*exp(-a*t), t, s) == (b/(a + s)**2, -a, True)
    assert LT(exp(-a*exp(-t)), t, s) == (lowergamma(s, a)/a**s, 0, True)
    assert LT(exp(-a*exp(t)), t, s) == (a**s*uppergamma(-s, a), 0, True)
    assert (LT(t**(S(7)/4)*exp(-8*t)/gamma(S(11)/4), t, s) ==
            ((s + 8)**(-S(11)/4), -8, True))
    assert (LT(t**(S(3)/2)*exp(-8*t), t, s) ==
            (3*sqrt(pi)/(4*(s + 8)**(S(5)/2)), -8, True))
    assert LT(t**a*exp(-a*t), t, s) == ((a+s)**(-a-1)*gamma(a+1), -a, True)
    assert (LT(b*exp(-a*t**2), t, s) ==
            (sqrt(pi)*b*exp(s**2/(4*a))*erfc(s/(2*sqrt(a)))/(2*sqrt(a)),
             0, True))
    assert (LT(exp(-2*t**2), t, s) ==
            (sqrt(2)*sqrt(pi)*exp(s**2/8)*erfc(sqrt(2)*s/4)/4, 0, True))
    assert (LT(b*exp(2*t**2), t, s) ==
            (b*LaplaceTransform(exp(2*t**2), t, s), -oo, True))
    assert (LT(t*exp(-a*t**2), t, s) ==
            (1/(2*a) - s*erfc(s/(2*sqrt(a)))/(4*sqrt(pi)*a**(S(3)/2)),
             0, True))
    assert (LT(exp(-a/t), t, s) ==
            (2*sqrt(a)*sqrt(1/s)*besselk(1, 2*sqrt(a)*sqrt(s)), 0, True))
    assert LT(sqrt(t)*exp(-a/t), t, s, simplify=True) == (
        sqrt(pi)*(sqrt(a)*sqrt(s) + 1/S(2))*sqrt(s**(-3)) *
        exp(-2*sqrt(a)*sqrt(s)), 0, True)
    assert (LT(exp(-a/t)/sqrt(t), t, s) ==
            (sqrt(pi)*sqrt(1/s)*exp(-2*sqrt(a)*sqrt(s)), 0, True))
    assert (LT(exp(-a/t)/(t*sqrt(t)), t, s) ==
            (sqrt(pi)*sqrt(1/a)*exp(-2*sqrt(a)*sqrt(s)), 0, True))
    # TODO: rules with sqrt(a*t) and sqrt(a/t) have stopped working after
    #       changes to as_base_exp
    # assert (
    #     LT(exp(-2*sqrt(a*t)), t, s) ==
    #     (1/s - sqrt(pi)*sqrt(a) * exp(a/s)*erfc(sqrt(a)*sqrt(1/s)) /
    #      s**(S(3)/2), 0, True))
    # assert LT(exp(-2*sqrt(a*t))/sqrt(t), t, s) == (
    #     exp(a/s)*erfc(sqrt(a) * sqrt(1/s))*(sqrt(pi)*sqrt(1/s)), 0, True)
    assert (LT(t**4*exp(-2/t), t, s) ==
            (8*sqrt(2)*(1/s)**(S(5)/2)*besselk(5, 2*sqrt(2)*sqrt(s)),
             0, True))
    assert LT(sinh(a*t), t, s) == (a/(-a**2 + s**2), a, True)
    assert (LT(b*sinh(a*t)**2, t, s) ==
            (2*a**2*b/(-4*a**2*s + s**3), 2*a, True))
    assert (LT(b*sinh(a*t)**2, t, s, simplify=True) ==
            (2*a**2*b/(s*(-4*a**2 + s**2)), 2*a, True))
    # The following line confirms that issue #21202 is solved
    assert LT(cosh(2*t), t, s) == (s/(-4 + s**2), 2, True)
    assert LT(cosh(a*t), t, s) == (s/(-a**2 + s**2), a, True)
    assert (LT(cosh(a*t)**2, t, s, simplify=True) ==
            ((2*a**2 - s**2)/(s*(4*a**2 - s**2)), 2*a, True))
    assert (LT(sinh(x+3), x, s, simplify=True) ==
            ((s*sinh(3) + cosh(3))/(s**2 - 1), 1, True))
    L, _, _ = LT(42*sin(w*t+x)**2, t, s)
    assert (
        L -
        21*(s**2 + s*(-s*cos(2*x) + 2*w*sin(2*x)) +
            4*w**2)/(s*(s**2 + 4*w**2))).simplify() == 0
    # The following line replaces the old test test_issue_7173()
    assert LT(sinh(a*t)*cosh(a*t), t, s, simplify=True) == (a/(-4*a**2 + s**2),
                                                            2*a, True)
    assert LT(sinh(a*t)/t, t, s) == (log((a + s)/(-a + s))/2, a, True)
    assert (LT(t**(-S(3)/2)*sinh(a*t), t, s) ==
            (-sqrt(pi)*(sqrt(-a + s) - sqrt(a + s)), a, True))
    # assert (LT(sinh(2*sqrt(a*t)), t, s) ==
    #         (sqrt(pi)*sqrt(a)*exp(a/s)/s**(S(3)/2), 0, True))
    # assert (LT(sqrt(t)*sinh(2*sqrt(a*t)), t, s, simplify=True) ==
    #         ((-sqrt(a)*s**(S(5)/2) + sqrt(pi)*s**2*(2*a + s)*exp(a/s) *
    #           erf(sqrt(a)*sqrt(1/s))/2)/s**(S(9)/2), 0, True))
    # assert (LT(sinh(2*sqrt(a*t))/sqrt(t), t, s) ==
    #         (sqrt(pi)*exp(a/s)*erf(sqrt(a)*sqrt(1/s))/sqrt(s), 0, True))
    # assert (LT(sinh(sqrt(a*t))**2/sqrt(t), t, s) ==
    #         (sqrt(pi)*(exp(a/s) - 1)/(2*sqrt(s)), 0, True))
    assert (LT(t**(S(3)/7)*cosh(a*t), t, s) ==
            (((a + s)**(-S(10)/7) + (-a+s)**(-S(10)/7))*gamma(S(10)/7)/2,
             a, True))
    # assert (LT(cosh(2*sqrt(a*t)), t, s) ==
    #         (sqrt(pi)*sqrt(a)*exp(a/s)*erf(sqrt(a)*sqrt(1/s))/s**(S(3)/2) +
    #          1/s, 0, True))
    # assert (LT(sqrt(t)*cosh(2*sqrt(a*t)), t, s) ==
    #         (sqrt(pi)*(a + s/2)*exp(a/s)/s**(S(5)/2), 0, True))
    # assert (LT(cosh(2*sqrt(a*t))/sqrt(t), t, s) ==
    #         (sqrt(pi)*exp(a/s)/sqrt(s), 0, True))
    # assert (LT(cosh(sqrt(a*t))**2/sqrt(t), t, s) ==
    #         (sqrt(pi)*(exp(a/s) + 1)/(2*sqrt(s)), 0, True))
    assert LT(log(t), t, s, simplify=True) == (
        (-log(s) - EulerGamma)/s, 0, True)
    assert (LT(-log(t/a), t, s, simplify=True) ==
            ((log(a) + log(s) + EulerGamma)/s, 0, True))
    assert LT(log(1+a*t), t, s) == (-exp(s/a)*Ei(-s/a)/s, 0, True)
    assert (LT(log(t+a), t, s, simplify=True) ==
            ((s*log(a) - exp(s/a)*Ei(-s/a))/s**2, 0, True))
    assert (LT(log(t)/sqrt(t), t, s, simplify=True) ==
            (sqrt(pi)*(-log(s) - log(4) - EulerGamma)/sqrt(s), 0, True))
    assert (LT(t**(S(5)/2)*log(t), t, s, simplify=True) ==
            (sqrt(pi)*(-15*log(s) - log(1073741824) - 15*EulerGamma + 46) /
             (8*s**(S(7)/2)), 0, True))
    assert (LT(t**3*log(t), t, s, noconds=True, simplify=True) -
            6*(-log(s) - S.EulerGamma + S(11)/6)/s**4).simplify() == S.Zero
    assert (LT(log(t)**2, t, s, simplify=True) ==
            (((log(s) + EulerGamma)**2 + pi**2/6)/s, 0, True))
    assert (LT(exp(-a*t)*log(t), t, s, simplify=True) ==
            ((-log(a + s) - EulerGamma)/(a + s), -a, True))
    assert LT(sin(a*t), t, s) == (a/(a**2 + s**2), 0, True)
    assert (LT(Abs(sin(a*t)), t, s) ==
            (a*coth(pi*s/(2*a))/(a**2 + s**2), 0, True))
    assert LT(sin(a*t)/t, t, s) == (atan(a/s), 0, True)
    assert LT(sin(a*t)**2/t, t, s) == (log(4*a**2/s**2 + 1)/4, 0, True)
    assert (LT(sin(a*t)**2/t**2, t, s) ==
            (a*atan(2*a/s) - s*log(4*a**2/s**2 + 1)/4, 0, True))
    # assert (LT(sin(2*sqrt(a*t)), t, s) ==
    #         (sqrt(pi)*sqrt(a)*exp(-a/s)/s**(S(3)/2), 0, True))
    # assert LT(sin(2*sqrt(a*t))/t, t, s) == (pi*erf(sqrt(a)*sqrt(1/s)), 0, True)
    assert LT(cos(a*t), t, s) == (s/(a**2 + s**2), 0, True)
    assert (LT(cos(a*t)**2, t, s) ==
            ((2*a**2 + s**2)/(s*(4*a**2 + s**2)), 0, True))
    # assert (LT(sqrt(t)*cos(2*sqrt(a*t)), t, s, simplify=True) ==
    #         (sqrt(pi)*(-a + s/2)*exp(-a/s)/s**(S(5)/2), 0, True))
    # assert (LT(cos(2*sqrt(a*t))/sqrt(t), t, s) ==
    #         (sqrt(pi)*sqrt(1/s)*exp(-a/s), 0, True))
    assert (LT(sin(a*t)*sin(b*t), t, s) ==
            (2*a*b*s/((s**2 + (a - b)**2)*(s**2 + (a + b)**2)), 0, True))
    assert (LT(cos(a*t)*sin(b*t), t, s) ==
            (b*(-a**2 + b**2 + s**2)/((s**2 + (a - b)**2)*(s**2 + (a + b)**2)),
             0, True))
    assert (LT(cos(a*t)*cos(b*t), t, s) ==
            (s*(a**2 + b**2 + s**2)/((s**2 + (a - b)**2)*(s**2 + (a + b)**2)),
             0, True))
    assert (LT(-a*t*cos(a*t) + sin(a*t), t, s, simplify=True) ==
            (2*a**3/(a**4 + 2*a**2*s**2 + s**4), 0, True))
    assert LT(c*exp(-b*t)*sin(a*t), t, s) == (a *
                                              c/(a**2 + (b + s)**2), -b, True)
    assert LT(c*exp(-b*t)*cos(a*t), t, s) == (c*(b + s)/(a**2 + (b + s)**2),
                                              -b, True)
    L, plane, cond = LT(cos(x + 3), x, s, simplify=True)
    assert plane == 0
    assert L - (s*cos(3) - sin(3))/(s**2 + 1) == 0
    # Error functions (laplace7.pdf)
    assert LT(erf(a*t), t, s) == (exp(s**2/(4*a**2))*erfc(s/(2*a))/s, 0, True)
    # assert LT(erf(sqrt(a*t)), t, s) == (sqrt(a)/(s*sqrt(a + s)), 0, True)
    # assert (LT(exp(a*t)*erf(sqrt(a*t)), t, s, simplify=True) ==
    #         (-sqrt(a)/(sqrt(s)*(a - s)), a, True))
    # assert (LT(erf(sqrt(a/t)/2), t, s, simplify=True) ==
    #         (1/s - exp(-sqrt(a)*sqrt(s))/s, 0, True))
    # assert (LT(erfc(sqrt(a*t)), t, s, simplify=True) ==
    #         (-sqrt(a)/(s*sqrt(a + s)) + 1/s, -a, True))
    # assert (LT(exp(a*t)*erfc(sqrt(a*t)), t, s) ==
    #         (1/(sqrt(a)*sqrt(s) + s), 0, True))
    # assert LT(erfc(sqrt(a/t)/2), t, s) == (exp(-sqrt(a)*sqrt(s))/s, 0, True)
    # Bessel functions (laplace8.pdf)
    assert LT(besselj(0, a*t), t, s) == (1/sqrt(a**2 + s**2), 0, True)
    assert (LT(besselj(1, a*t), t, s, simplify=True) ==
            (a/(a**2 + s**2 + s*sqrt(a**2 + s**2)), 0, True))
    assert (LT(besselj(2, a*t), t, s, simplify=True) ==
            (a**2/(sqrt(a**2 + s**2)*(s + sqrt(a**2 + s**2))**2), 0, True))
    assert (LT(t*besselj(0, a*t), t, s) ==
            (s/(a**2 + s**2)**(S(3)/2), 0, True))
    assert (LT(t*besselj(1, a*t), t, s) ==
            (a/(a**2 + s**2)**(S(3)/2), 0, True))
    assert (LT(t**2*besselj(2, a*t), t, s) ==
            (3*a**2/(a**2 + s**2)**(S(5)/2), 0, True))
    # assert LT(besselj(0, 2*sqrt(a*t)), t, s) == (exp(-a/s)/s, 0, True)
    # assert (LT(t**(S(3)/2)*besselj(3, 2*sqrt(a*t)), t, s) ==
    #         (a**(S(3)/2)*exp(-a/s)/s**4, 0, True))
    assert (LT(besselj(0, a*sqrt(t**2+b*t)), t, s, simplify=True) ==
            (exp(b*(s - sqrt(a**2 + s**2)))/sqrt(a**2 + s**2), 0, True))
    assert LT(besseli(0, a*t), t, s) == (1/sqrt(-a**2 + s**2), a, True)
    assert (LT(besseli(1, a*t), t, s, simplify=True) ==
            (a/(-a**2 + s**2 + s*sqrt(-a**2 + s**2)), a, True))
    assert (LT(besseli(2, a*t), t, s, simplify=True) ==
            (a**2/(sqrt(-a**2 + s**2)*(s + sqrt(-a**2 + s**2))**2), a, True))
    assert LT(t*besseli(0, a*t), t, s) == (s/(-a**2 + s**2)**(S(3)/2), a, True)
    assert LT(t*besseli(1, a*t), t, s) == (a/(-a**2 + s**2)**(S(3)/2), a, True)
    assert (LT(t**2*besseli(2, a*t), t, s) ==
            (3*a**2/(-a**2 + s**2)**(S(5)/2), a, True))
    # assert (LT(t**(S(3)/2)*besseli(3, 2*sqrt(a*t)), t, s) ==
    #         (a**(S(3)/2)*exp(a/s)/s**4, 0, True))
    assert (LT(bessely(0, a*t), t, s) ==
            (-2*asinh(s/a)/(pi*sqrt(a**2 + s**2)), 0, True))
    assert (LT(besselk(0, a*t), t, s) ==
            (log((s + sqrt(-a**2 + s**2))/a)/sqrt(-a**2 + s**2), -a, True))
    assert (LT(sin(a*t)**4, t, s, simplify=True) ==
            (24*a**4/(s*(64*a**4 + 20*a**2*s**2 + s**4)), 0, True))
    # Test general rules and unevaluated forms
    # These all also test whether issue #7219 is solved.
    assert LT(Heaviside(t-1)*cos(t-1), t, s) == (s*exp(-s)/(s**2 + 1), 0, True)
    assert LT(a*f(t), t, w) == (a*LaplaceTransform(f(t), t, w), -oo, True)
    assert (LT(a*Heaviside(t+1)*f(t+1), t, s) ==
            (a*LaplaceTransform(f(t + 1), t, s), -oo, True))
    assert (LT(a*Heaviside(t-1)*f(t-1), t, s) ==
            (a*LaplaceTransform(f(t), t, s)*exp(-s), -oo, True))
    assert (LT(b*f(t/a), t, s) ==
            (a*b*LaplaceTransform(f(t), t, a*s), -oo, True))
    assert LT(exp(-f(x)*t), t, s) == (1/(s + f(x)), -re(f(x)), True)
    assert (LT(exp(-a*t)*f(t), t, s) ==
            (LaplaceTransform(f(t), t, a + s), -oo, True))
    # assert (LT(exp(-a*t)*erfc(sqrt(b/t)/2), t, s) ==
    #         (exp(-sqrt(b)*sqrt(a + s))/(a + s), -a, True))
    assert (LT(sinh(a*t)*f(t), t, s) ==
            (LaplaceTransform(f(t), t, -a + s)/2 -
             LaplaceTransform(f(t), t, a + s)/2, -oo, True))
    assert (LT(sinh(a*t)*t, t, s, simplify=True) ==
            (2*a*s/(a**4 - 2*a**2*s**2 + s**4), a, True))
    assert (LT(cosh(a*t)*f(t), t, s) ==
            (LaplaceTransform(f(t), t, -a + s)/2 +
             LaplaceTransform(f(t), t, a + s)/2, -oo, True))
    assert (LT(cosh(a*t)*t, t, s, simplify=True) ==
            (1/(2*(a + s)**2) + 1/(2*(a - s)**2), a, True))
    assert (LT(sin(a*t)*f(t), t, s, simplify=True) ==
            (I*(-LaplaceTransform(f(t), t, -I*a + s) +
                LaplaceTransform(f(t), t, I*a + s))/2, -oo, True))
    assert (LT(sin(f(t)), t, s) ==
            (LaplaceTransform(sin(f(t)), t, s), -oo, True))
    assert (LT(sin(a*t)*t, t, s, simplify=True) ==
            (2*a*s/(a**4 + 2*a**2*s**2 + s**4), 0, True))
    assert (LT(cos(a*t)*f(t), t, s) ==
            (LaplaceTransform(f(t), t, -I*a + s)/2 +
             LaplaceTransform(f(t), t, I*a + s)/2, -oo, True))
    assert (LT(cos(a*t)*t, t, s, simplify=True) ==
            ((-a**2 + s**2)/(a**4 + 2*a**2*s**2 + s**4), 0, True))
    L, plane, _ = LT(sin(a*t+b)**2*f(t), t, s)
    assert plane == -oo
    assert (
        -L + (
            LaplaceTransform(f(t), t, s)/2 -
            LaplaceTransform(f(t), t, -2*I*a + s)*exp(2*I*b)/4 -
            LaplaceTransform(f(t), t, 2*I*a + s)*exp(-2*I*b)/4)) == 0
    L = LT(sin(a*t+b)**2*f(t), t, s, noconds=True)
    assert (
        laplace_correspondence(L, {f: F}) ==
        F(s)/2 - F(-2*I*a + s)*exp(2*I*b)/4 -
        F(2*I*a + s)*exp(-2*I*b)/4)
    L, plane, _ = LT(sin(a*t)**3*cosh(b*t), t, s)
    assert plane == b
    assert (
        -L - 3*a/(8*(9*a**2 + b**2 + 2*b*s + s**2)) -
        3*a/(8*(9*a**2 + b**2 - 2*b*s + s**2)) +
        3*a/(8*(a**2 + b**2 + 2*b*s + s**2)) +
        3*a/(8*(a**2 + b**2 - 2*b*s + s**2))).simplify() == 0
    assert (LT(t**2*exp(-t**2), t, s) ==
            (sqrt(pi)*s**2*exp(s**2/4)*erfc(s/2)/8 - s/4 +
             sqrt(pi)*exp(s**2/4)*erfc(s/2)/4, 0, True))
    assert (LT((a*t**2 + b*t + c)*f(t), t, s) ==
            (a*Derivative(LaplaceTransform(f(t), t, s), (s, 2)) -
             b*Derivative(LaplaceTransform(f(t), t, s), s) +
            c*LaplaceTransform(f(t), t, s), -oo, True))
    assert (LT(t**np*g(t), t, s) ==
            ((-1)**np*Derivative(LaplaceTransform(g(t), t, s), (s, np)),
             -oo, True))
    # The following tests check whether _piecewise_to_heaviside works:
    x1 = Piecewise((0, t <= 0), (1, t <= 1), (0, True))
    X1 = LT(x1, t, s)[0]
    assert X1 == 1/s - exp(-s)/s
    y1 = ILT(X1, s, t)
    assert y1 == Heaviside(t) - Heaviside(t - 1)
    x1 = Piecewise((0, t <= 0), (t, t <= 1), (2-t, t <= 2), (0, True))
    X1 = LT(x1, t, s)[0].simplify()
    assert X1 == (exp(2*s) - 2*exp(s) + 1)*exp(-2*s)/s**2
    y1 = ILT(X1, s, t)
    assert (
        -y1 + t*Heaviside(t) + (t - 2)*Heaviside(t - 2) -
        2*(t - 1)*Heaviside(t - 1)).simplify() == 0
    x1 = Piecewise((exp(t), t <= 0), (1, t <= 1), (exp(-(t)), True))
    X1 = LT(x1, t, s)[0]
    assert X1 == exp(-1)*exp(-s)/(s + 1) + 1/s - exp(-s)/s
    y1 = ILT(X1, s, t)
    assert y1 == (
        exp(-1)*exp(1 - t)*Heaviside(t - 1) + Heaviside(t) - Heaviside(t - 1))
    x1 = Piecewise((0, x <= 0), (1, x <= 1), (0, True))
    X1 = LT(x1, t, s)[0]
    assert X1 == Piecewise((0, x <= 0), (1, x <= 1), (0, True))/s
    x1 = [
        a*Piecewise((1, And(t > 1, t <= 3)), (2, True)),
        a*Piecewise((1, And(t >= 1, t <= 3)), (2, True)),
        a*Piecewise((1, And(t >= 1, t < 3)), (2, True)),
        a*Piecewise((1, And(t > 1, t < 3)), (2, True))]
    for x2 in x1:
        assert LT(x2, t, s)[0].expand() == 2*a/s - a*exp(-s)/s + a*exp(-3*s)/s
    assert (
        LT(Piecewise((1, Eq(t, 1)), (2, True)), t, s)[0] ==
        LaplaceTransform(Piecewise((1, Eq(t, 1)), (2, True)), t, s))
    # The following lines test whether _laplace_transform successfully
    # removes Heaviside(1) before processing espressions. It fails if
    # Heaviside(t) remains because then meijerg functions will appear.
    X1 = 1/sqrt(a*s**2-b)
    x1 = ILT(X1, s, t)
    Y1 = LT(x1, t, s)[0]
    Z1 = (Y1**2/X1**2).simplify()
    assert Z1 == 1
    # The following two lines test whether issues #5813 and #7176 are solved.
    assert (LT(diff(f(t), (t, 1)), t, s, noconds=True) ==
            s*LaplaceTransform(f(t), t, s) - f(0))
    assert (LT(diff(f(t), (t, 3)), t, s, noconds=True) ==
            s**3*LaplaceTransform(f(t), t, s) - s**2*f(0) -
            s*Subs(Derivative(f(t), t), t, 0) -
            Subs(Derivative(f(t), (t, 2)), t, 0))
    # Issue #7219
    assert (LT(diff(f(x, t, w), t, 2), t, s) ==
            (s**2*LaplaceTransform(f(x, t, w), t, s) - s*f(x, 0, w) -
             Subs(Derivative(f(x, t, w), t), t, 0), -oo, True))
    # Issue #23307
    assert (LT(10*diff(f(t), (t, 1)), t, s, noconds=True) ==
            10*s*LaplaceTransform(f(t), t, s) - 10*f(0))
    assert (LT(a*f(b*t)+g(c*t), t, s, noconds=True) ==
            a*LaplaceTransform(f(t), t, s/b)/b +
            LaplaceTransform(g(t), t, s/c)/c)
    assert inverse_laplace_transform(
        f(w), w, t, plane=0) == InverseLaplaceTransform(f(w), w, t, 0)
    assert (LT(f(t)*g(t), t, s, noconds=True) ==
            LaplaceTransform(f(t)*g(t), t, s))
    # Issue #24294
    assert (LT(b*f(a*t), t, s, noconds=True) ==
            b*LaplaceTransform(f(t), t, s/a)/a)
    assert LT(3*exp(t)*Heaviside(t), t, s) == (3/(s - 1), 1, True)
    assert (LT(2*sin(t)*Heaviside(t), t, s, simplify=True) ==
            (2/(s**2 + 1), 0, True))
    # Issue #25293
    assert (
        LT((1/(t-1))*sin(4*pi*(t-1))*DiracDelta(t-1) *
           (Heaviside(t-1/4) - Heaviside(t-2)), t, s)[0] == 4*pi*exp(-s))
    # additional basic tests from wikipedia
    assert (LT((t - a)**b*exp(-c*(t - a))*Heaviside(t - a), t, s) ==
            ((c + s)**(-b - 1)*exp(-a*s)*gamma(b + 1), -c, True))
    assert (
        LT((exp(2*t)-1)*exp(-b-t)*Heaviside(t)/2, t, s, noconds=True,
           simplify=True) ==
        exp(-b)/(s**2 - 1))
    # DiracDelta function: standard cases
    assert LT(DiracDelta(t), t, s) == (1, -oo, True)
    assert LT(DiracDelta(a*t), t, s) == (1/a, -oo, True)
    assert LT(DiracDelta(t/42), t, s) == (42, -oo, True)
    assert LT(DiracDelta(t+42), t, s) == (0, -oo, True)
    assert (LT(DiracDelta(t)+DiracDelta(t-42), t, s) ==
            (1 + exp(-42*s), -oo, True))
    assert (LT(DiracDelta(t)-a*exp(-a*t), t, s, simplify=True) ==
            (s/(a + s), -a, True))
    assert (
        LT(exp(-t)*(DiracDelta(t)+DiracDelta(t-42)), t, s, simplify=True) ==
        (exp(-42*s - 42) + 1, -oo, True))
    assert LT(f(t)*DiracDelta(t-42), t, s) == (f(42)*exp(-42*s), -oo, True)
    assert LT(f(t)*DiracDelta(b*t-a), t, s) == (f(a/b)*exp(-a*s/b)/b,
                                                -oo, True)
    assert LT(f(t)*DiracDelta(b*t+a), t, s) == (0, -oo, True)
    # SingularityFunction
    assert LT(SingularityFunction(t, a, -1), t, s)[0] == exp(-a*s)
    assert LT(SingularityFunction(t, a, 1), t, s)[0] == exp(-a*s)/s**2
    assert LT(SingularityFunction(t, a, x), t, s)[0] == (
        LaplaceTransform(SingularityFunction(t, a, x), t, s))
    # Collection of cases that cannot be fully evaluated and/or would catch
    # some common implementation errors
    assert (LT(DiracDelta(t**2), t, s, noconds=True) ==
            LaplaceTransform(DiracDelta(t**2), t, s))
    assert LT(DiracDelta(t**2 - 1), t, s) == (exp(-s)/2, -oo, True)
    assert LT(DiracDelta(t*(1 - t)), t, s) == (1 - exp(-s), -oo, True)
    assert (LT((DiracDelta(t) + 1)*(DiracDelta(t - 1) + 1), t, s) ==
            (LaplaceTransform(DiracDelta(t)*DiracDelta(t - 1), t, s) +
             1 + exp(-s) + 1/s, 0, True))
    assert LT(DiracDelta(2*t-2*exp(a)), t, s) == (exp(-s*exp(a))/2, -oo, True)
    assert LT(DiracDelta(-2*t+2*exp(a)), t, s) == (exp(-s*exp(a))/2, -oo, True)
    # Heaviside tests
    assert LT(Heaviside(t), t, s) == (1/s, 0, True)
    assert LT(Heaviside(t - a), t, s) == (exp(-a*s)/s, 0, True)
    assert LT(Heaviside(t-1), t, s) == (exp(-s)/s, 0, True)
    assert LT(Heaviside(2*t-4), t, s) == (exp(-2*s)/s, 0, True)
    assert LT(Heaviside(2*t+4), t, s) == (1/s, 0, True)
    assert (LT(Heaviside(-2*t+4), t, s, simplify=True) ==
            (1/s - exp(-2*s)/s, 0, True))
    assert (LT(g(t)*Heaviside(t - w), t, s) ==
            (LaplaceTransform(g(t)*Heaviside(t - w), t, s), -oo, True))
    assert (
        LT(Heaviside(t-a)*g(t), t, s) ==
        (LaplaceTransform(g(a + t), t, s)*exp(-a*s), -oo, True))
    assert (
        LT(Heaviside(t+a)*g(t), t, s) ==
        (LaplaceTransform(g(t), t, s), -oo, True))
    assert (
        LT(Heaviside(-t+a)*g(t), t, s) ==
        (LaplaceTransform(g(t), t, s) -
         LaplaceTransform(g(a + t), t, s)*exp(-a*s), -oo, True))
    assert (
        LT(Heaviside(-t-a)*g(t), t, s) == (0, 0, True))
    # Fresnel functions
    assert (laplace_transform(fresnels(t), t, s, simplify=True) ==
            ((-sin(s**2/(2*pi))*fresnels(s/pi) +
              sqrt(2)*sin(s**2/(2*pi) + pi/4)/2 -
              cos(s**2/(2*pi))*fresnelc(s/pi))/s, 0, True))
    assert (laplace_transform(fresnelc(t), t, s, simplify=True) ==
            ((sin(s**2/(2*pi))*fresnelc(s/pi) -
              cos(s**2/(2*pi))*fresnels(s/pi) +
              sqrt(2)*cos(s**2/(2*pi) + pi/4)/2)/s, 0, True))
    # Matrix tests
    Mt = Matrix([[exp(t), t*exp(-t)], [t*exp(-t), exp(t)]])
    Ms = Matrix([[1/(s - 1), (s + 1)**(-2)],
                 [(s + 1)**(-2),     1/(s - 1)]])
    # The default behaviour for Laplace transform of a Matrix returns a Matrix
    # of Tuples and is deprecated:
    with warns_deprecated_sympy():
        Ms_conds = Matrix(
            [[(1/(s - 1), 1, True), ((s + 1)**(-2), -1, True)],
             [((s + 1)**(-2), -1, True), (1/(s - 1), 1, True)]])
    with warns_deprecated_sympy():
        assert LT(Mt, t, s) == Ms_conds
    # The new behavior is to return a tuple of a Matrix and the convergence
    # conditions for the matrix as a whole:
    assert LT(Mt, t, s, legacy_matrix=False) == (Ms, 1, True)
    # With noconds=True the transformed matrix is returned without conditions
    # either way:
    assert LT(Mt, t, s, noconds=True) == Ms
    assert LT(Mt, t, s, legacy_matrix=False, noconds=True) == Ms

