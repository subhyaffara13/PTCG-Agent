
def test_inverse_laplace_transform():
    s = symbols('s')
    k, n, t = symbols('k, n, t', real=True)
    a, b, c, d = symbols('a, b, c, d', positive=True)
    f = Function('f')
    F = Function('F')

    def ILT(g):
        return inverse_laplace_transform(g, s, t)

    def ILTS(g):
        return inverse_laplace_transform(g, s, t, simplify=True)

    def ILTF(g):
        return laplace_correspondence(
            inverse_laplace_transform(g, s, t), {f: F})

    # Tests for the rules in Bateman54.

    # Section 4.1: Some of the Laplace transform rules can also be used well
    #     in the inverse transform.
    assert ILTF(exp(-a*s)*F(s)) == f(-a + t)
    assert ILTF(k*F(s-a)) == k*f(t)*exp(-a*t)
    assert ILTF(diff(F(s), s, 3)) == -t**3*f(t)
    assert ILTF(diff(F(s), s, 4)) == t**4*f(t)

    # Section 5.1: Most rules are impractical for a computer algebra system.

    # Section 5.2: Rational functions
    assert ILT(2) == 2*DiracDelta(t)
    assert ILT(1/s) == Heaviside(t)
    assert ILT(1/s**2) == t*Heaviside(t)
    assert ILT(1/s**5) == t**4*Heaviside(t)/24
    assert ILT(1/s**n) == t**(n - 1)*Heaviside(t)/gamma(n)
    assert ILT(a/(a + s)) == a*exp(-a*t)*Heaviside(t)
    assert ILT(s/(a + s)) == -a*exp(-a*t)*Heaviside(t) + DiracDelta(t)
    assert (ILT(b*s/(s+a)**2) ==
            b*(-a*t*exp(-a*t)*Heaviside(t) + exp(-a*t)*Heaviside(t)))
    assert (ILTS(c/((s+a)*(s+b))) ==
            c*(exp(a*t) - exp(b*t))*exp(-t*(a + b))*Heaviside(t)/(a - b))
    assert (ILTS(c*s/((s+a)*(s+b))) ==
            c*(a*exp(b*t) - b*exp(a*t))*exp(-t*(a + b))*Heaviside(t)/(a - b))
    assert ILTS(s/(a + s)**3) == t*(-a*t + 2)*exp(-a*t)*Heaviside(t)/2
    assert ILTS(1/(s*(a + s)**3)) == (
        -a**2*t**2 - 2*a*t + 2*exp(a*t) - 2)*exp(-a*t)*Heaviside(t)/(2*a**3)
    assert ILT(1/(s*(a + s)**n)) == (
        Heaviside(t)*lowergamma(n, a*t)/(a**n*gamma(n)))
    assert ILT((s-a)**(-b)) == t**(b - 1)*exp(a*t)*Heaviside(t)/gamma(b)
    assert ILT((a + s)**(-2)) == t*exp(-a*t)*Heaviside(t)
    assert ILT((a + s)**(-5)) == t**4*exp(-a*t)*Heaviside(t)/24
    assert ILT(s**2/(s**2 + 1)) == -sin(t)*Heaviside(t) + DiracDelta(t)
    assert ILT(1 - 1/(s**2 + 1)) == -sin(t)*Heaviside(t) + DiracDelta(t)
    assert ILT(a/(a**2 + s**2)) == sin(a*t)*Heaviside(t)
    assert ILT(s/(s**2 + a**2)) == cos(a*t)*Heaviside(t)
    assert ILT(b/(b**2 + (a + s)**2)) == exp(-a*t)*sin(b*t)*Heaviside(t)
    assert (ILT(b*s/(b**2 + (a + s)**2)) ==
            b*(-a*exp(-a*t)*sin(b*t)/b + exp(-a*t)*cos(b*t))*Heaviside(t))
    assert ILT(1/(s**2*(s**2 + 1))) == t*Heaviside(t) - sin(t)*Heaviside(t)
    assert (ILTS(c*s/(d**2*(s+a)**2+b**2)) ==
            c*(-a*d*sin(b*t/d) + b*cos(b*t/d))*exp(-a*t)*Heaviside(t)/(b*d**2))
    assert ILTS((b*s**2 + d)/(a**2 + s**2)**2) == (
        2*a**2*b*sin(a*t) + (a**2*b - d)*(a*t*cos(a*t) -
                                          sin(a*t)))*Heaviside(t)/(2*a**3)
    assert ILTS(b/(s**2-a**2)) == b*sinh(a*t)*Heaviside(t)/a
    assert (ILT(b/(s**2-a**2)) ==
            b*(exp(a*t)*Heaviside(t)/(2*a) - exp(-a*t)*Heaviside(t)/(2*a)))
    assert ILTS(b*s/(s**2-a**2)) == b*cosh(a*t)*Heaviside(t)
    assert (ILT(b/(s*(s+a))) ==
            b*(Heaviside(t)/a - exp(-a*t)*Heaviside(t)/a))
    # Issue #24424
    assert (ILTS((s + 8)/((s + 2)*(s**2 + 2*s + 10))) ==
            ((8*sin(3*t) - 9*cos(3*t))*exp(t) + 9)*exp(-2*t)*Heaviside(t)/15)
    # Issue #8514; this is not important anymore, since this function
    # is not solved by integration anymore
    assert (ILT(1/(a*s**2+b*s+c)) ==
            2*exp(-b*t/(2*a))*sin(t*sqrt(4*a*c - b**2)/(2*a)) *
            Heaviside(t)/sqrt(4*a*c - b**2))

    # Section 5.3: Irrational algebraic functions
    assert (  # (1)
        ILT(1/sqrt(s)/(b*s-a)) ==
        exp(a*t/b)*Heaviside(t)*erf(sqrt(a)*sqrt(t)/sqrt(b))/(sqrt(a)*sqrt(b)))
    assert (  # (2)
        ILT(1/sqrt(k*s)/(c*s-a)/s) ==
        (-2*c*sqrt(t)/(sqrt(pi)*a) +
         c**(S(3)/2)*exp(a*t/c)*erf(sqrt(a)*sqrt(t)/sqrt(c))/a**(S(3)/2)) *
        Heaviside(t)/(c*sqrt(k)))
    assert (  # (4)
        ILT(1/(sqrt(c*s)+a)) == (-a*exp(a**2*t/c)*erfc(a*sqrt(t)/sqrt(c))/c +
                                 1/(sqrt(pi)*sqrt(c)*sqrt(t)))*Heaviside(t))
    assert (  # (5)
        ILT(a/s/(b*sqrt(s)+a)) ==
        (-exp(a**2*t/b**2)*erfc(a*sqrt(t)/b) + 1)*Heaviside(t))
    assert (  # (6)
            ILT((a-b)*sqrt(s)/(sqrt(s)+sqrt(a))/(s-b)) ==
            (sqrt(a)*sqrt(b)*exp(b*t)*erfc(sqrt(b)*sqrt(t)) +
             a*exp(a*t)*erfc(sqrt(a)*sqrt(t)) - b*exp(b*t))*Heaviside(t))
    assert (  # (7)
            ILT(1/sqrt(s)/(sqrt(b*s)+a)) ==
            exp(a**2*t/b)*Heaviside(t)*erfc(a*sqrt(t)/sqrt(b))/sqrt(b))
    assert (  # (8)
            ILT(a**2/(sqrt(s)+a)/s**(S(3)/2)) ==
            (2*a*sqrt(t)/sqrt(pi) + exp(a**2*t)*erfc(a*sqrt(t)) - 1) *
            Heaviside(t))
    assert (  # (9)
            ILT((a-b)*sqrt(b)/(s-b)/sqrt(s)/(sqrt(s)+sqrt(a))) ==
            (sqrt(a)*exp(b*t)*erf(sqrt(b)*sqrt(t)) +
             sqrt(b)*exp(a*t)*erfc(sqrt(a)*sqrt(t)) -
             sqrt(b)*exp(b*t))*Heaviside(t))
    assert (  # (10)
            ILT(1/(sqrt(s)+sqrt(a))**2) ==
            (-2*sqrt(a)*sqrt(t)/sqrt(pi) +
             (-2*a*t + 1)*(erf(sqrt(a)*sqrt(t)) -
                           1)*exp(a*t) + 1)*Heaviside(t))
    assert (  # (11)
            ILT(1/(sqrt(s)+sqrt(a))**2/s) ==
            ((2*t - 1/a)*exp(a*t)*erfc(sqrt(a)*sqrt(t)) + 1/a -
             2*sqrt(t)/(sqrt(pi)*sqrt(a)))*Heaviside(t))
    assert (  # (12)
            ILT(1/(sqrt(s)+a)**2/sqrt(s)) ==
            (-2*a*t*exp(a**2*t)*erfc(a*sqrt(t)) +
             2*sqrt(t)/sqrt(pi))*Heaviside(t))
    assert (  # (13)
            ILT(1/(sqrt(s)+a)**3) ==
            (-a*t*(2*a**2*t + 3)*exp(a**2*t)*erfc(a*sqrt(t)) +
             2*sqrt(t)*(a**2*t + 1)/sqrt(pi))*Heaviside(t))
    x = (
        - ILT(sqrt(s)/(sqrt(s)+a)**3) +
        2*(sqrt(pi)*a**2*t*(-2*sqrt(pi)*erfc(a*sqrt(t)) +
                            2*exp(-a**2*t)/(a*sqrt(t))) *
           (-a**4*t**2 - 5*a**2*t/2 - S.Half) * exp(a**2*t)/2 +
           sqrt(pi)*a*sqrt(t)*(a**2*t + 1)/2) *
        Heaviside(t)/(pi*a**2*t)).simplify()
    assert (  # (14)
            x == 0)
    x = (
        - ILT(1/sqrt(s)/(sqrt(s)+a)**3) +
        Heaviside(t)*(sqrt(t)*((2*a**2*t + 1) *
                               (sqrt(pi)*a*sqrt(t)*exp(a**2*t) *
                                erfc(a*sqrt(t)) - 1) + 1) /
                      (sqrt(pi)*a))).simplify()
    assert (  # (15)
            x == 0)
    assert (  # (16)
            factor_terms(ILT(3/(sqrt(s)+a)**4)) ==
            3*(-2*a**3*t**(S(5)/2)*(2*a**2*t + 5)/(3*sqrt(pi)) +
               t*(4*a**4*t**2 + 12*a**2*t + 3)*exp(a**2*t) *
               erfc(a*sqrt(t))/3)*Heaviside(t))
    assert (  # (17)
            ILT((sqrt(s)-a)/(s*(sqrt(s)+a))) ==
            (2*exp(a**2*t)*erfc(a*sqrt(t))-1)*Heaviside(t))
    assert (  # (18)
            ILT((sqrt(s)-a)**2/(s*(sqrt(s)+a)**2)) == (
                1 + 8*a**2*t*exp(a**2*t)*erfc(a*sqrt(t)) -
                8/sqrt(pi)*a*sqrt(t))*Heaviside(t))
    assert (  # (19)
            ILT((sqrt(s)-a)**3/(s*(sqrt(s)+a)**3)) == Heaviside(t)*(
                2*(8*a**4*t**2+8*a**2*t+1)*exp(a**2*t) *
                erfc(a*sqrt(t))-8/sqrt(pi)*a*sqrt(t)*(2*a**2*t+1)-1))
    assert (  # (22)
            ILT(sqrt(s+a)/(s+b)) == Heaviside(t)*(
                exp(-a*t)/sqrt(t)/sqrt(pi) +
                sqrt(a-b)*exp(-b*t)*erf(sqrt(a-b)*sqrt(t))))
    assert (  # (23)
            ILT(1/sqrt(s+b)/(s+a)) == Heaviside(t)*(
                1/sqrt(b-a)*exp(-a*t)*erf(sqrt(b-a)*sqrt(t))))
    assert (  # (35)
            ILT(1/sqrt(s**2+a**2)) == Heaviside(t)*(
                besselj(0, a*t)))
    assert (  # (44)
            ILT(1/sqrt(s**2-a**2)) == Heaviside(t)*(
                besseli(0, a*t)))

    # Miscellaneous tests
    # Can _inverse_laplace_time_shift deal with positive exponents?
    assert (
        - ILT((s**2*exp(2*s) + 4*exp(s) - 4)*exp(-2*s)/(s*(s**2 + 1))) +
        cos(t)*Heaviside(t) + 4*cos(t - 2)*Heaviside(t - 2) -
        4*cos(t - 1)*Heaviside(t - 1) - 4*Heaviside(t - 2) +
        4*Heaviside(t - 1)).simplify() == 0

