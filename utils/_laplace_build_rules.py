import re

def _laplace_build_rules():
    """
    This is an internal helper function that returns the table of Laplace
    transform rules in terms of the time variable `t` and the frequency
    variable `s`.  It is used by ``_laplace_apply_rules``.  Each entry is a
    tuple containing:

        (time domain pattern,
         frequency-domain replacement,
         condition for the rule to be applied,
         convergence plane,
         preparation function)

    The preparation function is a function with one argument that is applied
    to the expression before matching. For most rules it should be
    ``_laplace_deep_collect``.
    """
    t = Dummy('t')
    s = Dummy('s')
    a = Wild('a', exclude=[t])
    b = Wild('b', exclude=[t])
    n = Wild('n', exclude=[t])
    tau = Wild('tau', exclude=[t])
    omega = Wild('omega', exclude=[t])
    def dco(f): return _laplace_deep_collect(f, t)
    _debug('_laplace_build_rules is building rules')

    laplace_transform_rules = [
        (a, a/s,
         S.true, S.Zero, dco),  # 4.2.1
        (DiracDelta(a*t-b), exp(-s*b/a)/Abs(a),
         Or(And(a > 0, b >= 0), And(a < 0, b <= 0)),
         S.NegativeInfinity, dco),  # Not in Bateman54
        (DiracDelta(a*t-b), S(0),
         Or(And(a < 0, b >= 0), And(a > 0, b <= 0)),
         S.NegativeInfinity, dco),  # Not in Bateman54
        (Heaviside(a*t-b), exp(-s*b/a)/s,
         And(a > 0, b > 0), S.Zero, dco),  # 4.4.1
        (Heaviside(a*t-b), (1-exp(-s*b/a))/s,
         And(a < 0, b < 0), S.Zero, dco),  # 4.4.1
        (Heaviside(a*t-b), 1/s,
         And(a > 0, b <= 0), S.Zero, dco),  # 4.4.1
        (Heaviside(a*t-b), 0,
         And(a < 0, b > 0), S.Zero, dco),  # 4.4.1
        (t, 1/s**2,
         S.true, S.Zero, dco),  # 4.2.3
        (1/(a*t+b), -exp(-b/a*s)*Ei(-b/a*s)/a,
         Abs(arg(b/a)) < pi, S.Zero, dco),  # 4.2.6
        (1/sqrt(a*t+b), sqrt(a*pi/s)*exp(b/a*s)*erfc(sqrt(b/a*s))/a,
         Abs(arg(b/a)) < pi, S.Zero, dco),  # 4.2.18
        ((a*t+b)**(-S(3)/2),
         2*b**(-S(1)/2)-2*(pi*s/a)**(S(1)/2)*exp(b/a*s) * erfc(sqrt(b/a*s))/a,
         Abs(arg(b/a)) < pi, S.Zero, dco),  # 4.2.20
        (sqrt(t)/(t+b), sqrt(pi/s)-pi*sqrt(b)*exp(b*s)*erfc(sqrt(b*s)),
         Abs(arg(b)) < pi, S.Zero, dco),  # 4.2.22
        (1/(a*sqrt(t) + t**(3/2)), pi*a**(S(1)/2)*exp(a*s)*erfc(sqrt(a*s)),
         S.true, S.Zero, dco),  # Not in Bateman54
        (t**n, gamma(n+1)/s**(n+1),
         n > -1, S.Zero, dco),  # 4.3.1
        ((a*t+b)**n, uppergamma(n+1, b/a*s)*exp(-b/a*s)/s**(n+1)/a,
         And(n > -1, Abs(arg(b/a)) < pi), S.Zero, dco),  # 4.3.4
        (t**n/(t+a), a**n*gamma(n+1)*uppergamma(-n, a*s),
         And(n > -1, Abs(arg(a)) < pi), S.Zero, dco),  # 4.3.7
        (exp(a*t-tau), exp(-tau)/(s-a),
         S.true, re(a), dco),  # 4.5.1
        (t*exp(a*t-tau), exp(-tau)/(s-a)**2,
         S.true, re(a), dco),  # 4.5.2
        (t**n*exp(a*t), gamma(n+1)/(s-a)**(n+1),
         re(n) > -1, re(a), dco),  # 4.5.3
        (exp(-a*t**2), sqrt(pi/4/a)*exp(s**2/4/a)*erfc(s/sqrt(4*a)),
         re(a) > 0, S.Zero, dco),  # 4.5.21
        (t*exp(-a*t**2),
         1/(2*a)-2/sqrt(pi)/(4*a)**(S(3)/2)*s*erfc(s/sqrt(4*a)),
         re(a) > 0, S.Zero, dco),  # 4.5.22
        (exp(-a/t), 2*sqrt(a/s)*besselk(1, 2*sqrt(a*s)),
         re(a) >= 0, S.Zero, dco),  # 4.5.25
        (sqrt(t)*exp(-a/t),
         S(1)/2*sqrt(pi/s**3)*(1+2*sqrt(a*s))*exp(-2*sqrt(a*s)),
         re(a) >= 0, S.Zero, dco),  # 4.5.26
        (exp(-a/t)/sqrt(t), sqrt(pi/s)*exp(-2*sqrt(a*s)),
         re(a) >= 0, S.Zero, dco),  # 4.5.27
        (exp(-a/t)/(t*sqrt(t)), sqrt(pi/a)*exp(-2*sqrt(a*s)),
         re(a) > 0, S.Zero, dco),  # 4.5.28
        (t**n*exp(-a/t), 2*(a/s)**((n+1)/2)*besselk(n+1, 2*sqrt(a*s)),
         re(a) > 0, S.Zero, dco),  # 4.5.29
        # TODO: rules with sqrt(a*t) and sqrt(a/t) have stopped working after
        #       changes to as_base_exp
        # (exp(-2*sqrt(a*t)),
        #  s**(-1)-sqrt(pi*a)*s**(-S(3)/2)*exp(a/s) * erfc(sqrt(a/s)),
        #  Abs(arg(a)) < pi, S.Zero, dco),  # 4.5.31
        # (exp(-2*sqrt(a*t))/sqrt(t), (pi/s)**(S(1)/2)*exp(a/s)*erfc(sqrt(a/s)),
        #  Abs(arg(a)) < pi, S.Zero, dco),  # 4.5.33
        (exp(-a*exp(-t)), a**(-s)*lowergamma(s, a),
         S.true, S.Zero, dco),  # 4.5.36
        (exp(-a*exp(t)), a**s*uppergamma(-s, a),
         re(a) > 0, S.Zero, dco),  # 4.5.37
        (log(a*t), -log(exp(S.EulerGamma)*s/a)/s,
         a > 0, S.Zero, dco),  # 4.6.1
        (log(1+a*t), -exp(s/a)/s*Ei(-s/a),
         Abs(arg(a)) < pi, S.Zero, dco),  # 4.6.4
        (log(a*t+b), (log(b)-exp(s/b/a)/s*a*Ei(-s/b))/s*a,
         And(a > 0, Abs(arg(b)) < pi), S.Zero, dco),  # 4.6.5
        (log(t)/sqrt(t), -sqrt(pi/s)*log(4*s*exp(S.EulerGamma)),
         S.true, S.Zero, dco),  # 4.6.9
        (t**n*log(t), gamma(n+1)*s**(-n-1)*(digamma(n+1)-log(s)),
         re(n) > -1, S.Zero, dco),  # 4.6.11
        (log(a*t)**2, (log(exp(S.EulerGamma)*s/a)**2+pi**2/6)/s,
         a > 0, S.Zero, dco),  # 4.6.13
        (sin(omega*t), omega/(s**2+omega**2),
         S.true, Abs(im(omega)), dco),  # 4,7,1
        (Abs(sin(omega*t)), omega/(s**2+omega**2)*coth(pi*s/2/omega),
         omega > 0, S.Zero, dco),  # 4.7.2
        (sin(omega*t)/t, atan(omega/s),
         S.true, Abs(im(omega)), dco),  # 4.7.16
        (sin(omega*t)**2/t, log(1+4*omega**2/s**2)/4,
         S.true, 2*Abs(im(omega)), dco),  # 4.7.17
        (sin(omega*t)**2/t**2,
         omega*atan(2*omega/s)-s*log(1+4*omega**2/s**2)/4,
         S.true, 2*Abs(im(omega)), dco),  # 4.7.20
        # (sin(2*sqrt(a*t)), sqrt(pi*a)/s/sqrt(s)*exp(-a/s),
        #  S.true, S.Zero, dco),  # 4.7.32
        # (sin(2*sqrt(a*t))/t, pi*erf(sqrt(a/s)),
        #  S.true, S.Zero, dco),  # 4.7.34
        (cos(omega*t), s/(s**2+omega**2),
         S.true, Abs(im(omega)), dco),  # 4.7.43
        (cos(omega*t)**2, (s**2+2*omega**2)/(s**2+4*omega**2)/s,
         S.true, 2*Abs(im(omega)), dco),  # 4.7.45
        # (sqrt(t)*cos(2*sqrt(a*t)), sqrt(pi)/2*s**(-S(5)/2)*(s-2*a)*exp(-a/s),
        #  S.true, S.Zero, dco),  # 4.7.66
        # (cos(2*sqrt(a*t))/sqrt(t), sqrt(pi/s)*exp(-a/s),
        #  S.true, S.Zero, dco),  # 4.7.67
        (sin(a*t)*sin(b*t), 2*a*b*s/(s**2+(a+b)**2)/(s**2+(a-b)**2),
         S.true, Abs(im(a))+Abs(im(b)), dco),  # 4.7.78
        (cos(a*t)*sin(b*t), b*(s**2-a**2+b**2)/(s**2+(a+b)**2)/(s**2+(a-b)**2),
         S.true, Abs(im(a))+Abs(im(b)), dco),  # 4.7.79
        (cos(a*t)*cos(b*t), s*(s**2+a**2+b**2)/(s**2+(a+b)**2)/(s**2+(a-b)**2),
         S.true, Abs(im(a))+Abs(im(b)), dco),  # 4.7.80
        (sinh(a*t), a/(s**2-a**2),
         S.true, Abs(re(a)), dco),  # 4.9.1
        (cosh(a*t), s/(s**2-a**2),
         S.true, Abs(re(a)), dco),  # 4.9.2
        (sinh(a*t)**2, 2*a**2/(s**3-4*a**2*s),
         S.true, 2*Abs(re(a)), dco),  # 4.9.3
        (cosh(a*t)**2, (s**2-2*a**2)/(s**3-4*a**2*s),
         S.true, 2*Abs(re(a)), dco),  # 4.9.4
        (sinh(a*t)/t, log((s+a)/(s-a))/2,
         S.true, Abs(re(a)), dco),  # 4.9.12
        (t**n*sinh(a*t), gamma(n+1)/2*((s-a)**(-n-1)-(s+a)**(-n-1)),
         n > -2, Abs(a), dco),  # 4.9.18
        (t**n*cosh(a*t), gamma(n+1)/2*((s-a)**(-n-1)+(s+a)**(-n-1)),
         n > -1, Abs(a), dco),  # 4.9.19
        # TODO
        # (sinh(2*sqrt(a*t)), sqrt(pi*a)/s/sqrt(s)*exp(a/s),
        #  S.true, S.Zero, dco),  # 4.9.34
        # (cosh(2*sqrt(a*t)), 1/s+sqrt(pi*a)/s/sqrt(s)*exp(a/s)*erf(sqrt(a/s)),
        #  S.true, S.Zero, dco),  # 4.9.35
        # (
        #     sqrt(t)*sinh(2*sqrt(a*t)),
        #     pi**(S(1)/2)*s**(-S(5)/2)*(s/2+a) *
        #     exp(a/s)*erf(sqrt(a/s))-a**(S(1)/2)*s**(-2),
        #     S.true, S.Zero, dco),  # 4.9.36
        # (sqrt(t)*cosh(2*sqrt(a*t)), pi**(S(1)/2)*s**(-S(5)/2)*(s/2+a)*exp(a/s),
        #   S.true, S.Zero, dco),  # 4.9.37
        # (sinh(2*sqrt(a*t))/sqrt(t),
        #  pi**(S(1)/2)*s**(-S(1)/2)*exp(a/s) * erf(sqrt(a/s)),
        #     S.true, S.Zero, dco),  # 4.9.38
        # (cosh(2*sqrt(a*t))/sqrt(t), pi**(S(1)/2)*s**(-S(1)/2)*exp(a/s),
        #  S.true, S.Zero, dco),  # 4.9.39
        # (sinh(sqrt(a*t))**2/sqrt(t), pi**(S(1)/2)/2*s**(-S(1)/2)*(exp(a/s)-1),
        #  S.true, S.Zero, dco),  # 4.9.40
        # (cosh(sqrt(a*t))**2/sqrt(t), pi**(S(1)/2)/2*s**(-S(1)/2)*(exp(a/s)+1),
        #  S.true, S.Zero, dco),  # 4.9.41
        (erf(a*t), exp(s**2/(2*a)**2)*erfc(s/(2*a))/s,
         4*Abs(arg(a)) < pi, S.Zero, dco),  # 4.12.2
        # (erf(sqrt(a*t)), sqrt(a)/sqrt(s+a)/s,
        #  S.true, Max(S.Zero, -re(a)), dco),  # 4.12.4
        # (exp(a*t)*erf(sqrt(a*t)), sqrt(a)/sqrt(s)/(s-a),
        #  S.true, Max(S.Zero, re(a)), dco),  # 4.12.5
        # (erf(sqrt(a/t)/2), (1-exp(-sqrt(a*s)))/s,
        #  re(a) > 0, S.Zero, dco),  # 4.12.6
        # (erfc(sqrt(a*t)), (sqrt(s+a)-sqrt(a))/sqrt(s+a)/s,
        #  S.true, -re(a), dco),  # 4.12.9
        # (exp(a*t)*erfc(sqrt(a*t)), 1/(s+sqrt(a*s)),
        #  S.true, S.Zero, dco),  # 4.12.10
        # (erfc(sqrt(a/t)/2), exp(-sqrt(a*s))/s,
        #  re(a) > 0, S.Zero, dco),  # 4.2.11
        (besselj(n, a*t), a**n/(sqrt(s**2+a**2)*(s+sqrt(s**2+a**2))**n),
         re(n) > -1, Abs(im(a)), dco),  # 4.14.1
        (t**b*besselj(n, a*t),
         2**n/sqrt(pi)*gamma(n+S.Half)*a**n*(s**2+a**2)**(-n-S.Half),
         And(re(n) > -S.Half, Eq(b, n)), Abs(im(a)), dco),  # 4.14.7
        (t**b*besselj(n, a*t),
         2**(n+1)/sqrt(pi)*gamma(n+S(3)/2)*a**n*s*(s**2+a**2)**(-n-S(3)/2),
         And(re(n) > -1, Eq(b, n+1)), Abs(im(a)), dco),  # 4.14.8
        # (besselj(0, 2*sqrt(a*t)), exp(-a/s)/s,
        #  S.true, S.Zero, dco),  # 4.14.25
        # (t**(b)*besselj(n, 2*sqrt(a*t)), a**(n/2)*s**(-n-1)*exp(-a/s),
        #  And(re(n) > -1, Eq(b, n*S.Half)), S.Zero, dco),  # 4.14.30
        (besselj(0, a*sqrt(t**2+b*t)),
         exp(b*s-b*sqrt(s**2+a**2))/sqrt(s**2+a**2),
         Abs(arg(b)) < pi, Abs(im(a)), dco),  # 4.15.19
        (besseli(n, a*t), a**n/(sqrt(s**2-a**2)*(s+sqrt(s**2-a**2))**n),
         re(n) > -1, Abs(re(a)), dco),  # 4.16.1
        (t**b*besseli(n, a*t),
         2**n/sqrt(pi)*gamma(n+S.Half)*a**n*(s**2-a**2)**(-n-S.Half),
         And(re(n) > -S.Half, Eq(b, n)), Abs(re(a)), dco),  # 4.16.6
        (t**b*besseli(n, a*t),
         2**(n+1)/sqrt(pi)*gamma(n+S(3)/2)*a**n*s*(s**2-a**2)**(-n-S(3)/2),
         And(re(n) > -1, Eq(b, n+1)), Abs(re(a)), dco),  # 4.16.7
        # (t**(b)*besseli(n, 2*sqrt(a*t)), a**(n/2)*s**(-n-1)*exp(a/s),
        #  And(re(n) > -1, Eq(b, n*S.Half)), S.Zero, dco),  # 4.16.18
        (bessely(0, a*t), -2/pi*asinh(s/a)/sqrt(s**2+a**2),
         S.true, Abs(im(a)), dco),  # 4.15.44
        (besselk(0, a*t), log((s + sqrt(s**2-a**2))/a)/(sqrt(s**2-a**2)),
         S.true, -re(a), dco)  # 4.16.23
    ]
    return laplace_transform_rules, t, s

