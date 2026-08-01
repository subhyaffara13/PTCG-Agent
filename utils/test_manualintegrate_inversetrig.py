
def test_manualintegrate_inversetrig():
    # atan
    assert manualintegrate(exp(x) / (1 + exp(2*x)), x) == atan(exp(x))
    assert manualintegrate(1 / (4 + 9 * x**2), x) == atan(3 * x/2) / 6
    assert manualintegrate(1 / (16 + 16 * x**2), x) == atan(x) / 16
    assert manualintegrate(1 / (4 + x**2), x) == atan(x / 2) / 2
    assert manualintegrate(1 / (1 + 4 * x**2), x) == atan(2*x) / 2
    ra = Symbol('a', real=True)
    rb = Symbol('b', real=True)
    assert manualintegrate(1/(ra + rb*x**2), x) == \
        Piecewise((atan(x/sqrt(ra/rb))/(rb*sqrt(ra/rb)), ra/rb > 0),
                  ((log(x - sqrt(-ra/rb)) - log(x + sqrt(-ra/rb)))/(2*sqrt(rb)*sqrt(-ra)), True))
    assert manualintegrate(1/(4 + rb*x**2), x) == \
        Piecewise((atan(x/(2*sqrt(1/rb)))/(2*rb*sqrt(1/rb)), 1/rb > 0),
                  (-I*(log(x - 2*sqrt(-1/rb)) - log(x + 2*sqrt(-1/rb)))/(4*sqrt(rb)), True))
    assert manualintegrate(1/(ra + 4*x**2), x) == \
        Piecewise((atan(2*x/sqrt(ra))/(2*sqrt(ra)), ra > 0),
                  ((log(x - sqrt(-ra)/2) - log(x + sqrt(-ra)/2))/(4*sqrt(-ra)), True))
    assert manualintegrate(1/(4 + 4*x**2), x) == atan(x) / 4

    assert manualintegrate(1/(a + b*x**2), x) == Piecewise((atan(x/sqrt(a/b))/(b*sqrt(a/b)), Ne(a, 0)),
                                                           (-1/(b*x), True))

    # asin
    assert manualintegrate(1/sqrt(1-x**2), x) == asin(x)
    assert manualintegrate(1/sqrt(4-4*x**2), x) == asin(x)/2
    assert manualintegrate(3/sqrt(1-9*x**2), x) == asin(3*x)
    assert manualintegrate(1/sqrt(4-9*x**2), x) == asin(x*Rational(3, 2))/3

    # asinh
    assert manualintegrate(1/sqrt(x**2 + 1), x) == \
        asinh(x)
    assert manualintegrate(1/sqrt(x**2 + 4), x) == \
        asinh(x/2)
    assert manualintegrate(1/sqrt(4*x**2 + 4), x) == \
        asinh(x)/2
    assert manualintegrate(1/sqrt(4*x**2 + 1), x) == \
        asinh(2*x)/2
    assert manualintegrate(1/sqrt(ra*x**2 + 1), x) == \
        Piecewise((asin(x*sqrt(-ra))/sqrt(-ra), ra < 0), (asinh(sqrt(ra)*x)/sqrt(ra), ra > 0), (x, True))
    assert manualintegrate(1/sqrt(ra + x**2), x) == \
        Piecewise((asinh(x*sqrt(1/ra)), ra > 0), (log(2*x + 2*sqrt(ra + x**2)), True))

    # log
    assert manualintegrate(1/sqrt(x**2 - 1), x) == log(2*x + 2*sqrt(x**2 - 1))
    assert manualintegrate(1/sqrt(x**2 - 4), x) == log(2*x + 2*sqrt(x**2 - 4))
    assert manualintegrate(1/sqrt(4*x**2 - 4), x) == log(8*x + 4*sqrt(4*x**2 - 4))/2
    assert manualintegrate(1/sqrt(9*x**2 - 1), x) == log(18*x + 6*sqrt(9*x**2 - 1))/3
    assert manualintegrate(1/sqrt(ra*x**2 - 4), x) == \
           Piecewise((log(2*sqrt(ra)*sqrt(ra*x**2 - 4) + 2*ra*x)/sqrt(ra), Ne(ra, 0)), (-I*x/2, True))
    assert manualintegrate(1/sqrt(-ra + 4*x**2), x) == \
        Piecewise((asinh(2*x*sqrt(-1/ra))/2, ra < 0), (log(8*x + 4*sqrt(-ra + 4*x**2))/2, True))

    # From https://www.wikiwand.com/en/List_of_integrals_of_inverse_trigonometric_functions
    # asin
    assert manualintegrate(asin(x), x) == x*asin(x) + sqrt(1 - x**2)
    assert manualintegrate(asin(a*x), x) == Piecewise(((a*x*asin(a*x) + sqrt(-a**2*x**2 + 1))/a, Ne(a, 0)), (0, True))
    assert manualintegrate(x*asin(a*x), x) == \
           -a*Piecewise((-x*sqrt(-a**2*x**2 + 1)/(2*a**2) +
                         log(-2*a**2*x + 2*sqrt(-a**2)*sqrt(-a**2*x**2 + 1))/(2*a**2*sqrt(-a**2)), Ne(a**2, 0)),
                        (x**3/3, True))/2 + x**2*asin(a*x)/2
    # acos
    assert manualintegrate(acos(x), x) == x*acos(x) - sqrt(1 - x**2)
    assert manualintegrate(acos(a*x), x) == Piecewise(((a*x*acos(a*x) - sqrt(-a**2*x**2 + 1))/a, Ne(a, 0)), (pi*x/2, True))
    assert manualintegrate(x*acos(a*x), x) == \
           a*Piecewise((-x*sqrt(-a**2*x**2 + 1)/(2*a**2) +
                        log(-2*a**2*x + 2*sqrt(-a**2)*sqrt(-a**2*x**2 + 1))/(2*a**2*sqrt(-a**2)), Ne(a**2, 0)),
                       (x**3/3, True))/2 + x**2*acos(a*x)/2
    # atan
    assert manualintegrate(atan(x), x) == x*atan(x) - log(x**2 + 1)/2
    assert manualintegrate(atan(a*x), x) == Piecewise(((a*x*atan(a*x) - log(a**2*x**2 + 1)/2)/a, Ne(a, 0)), (0, True))
    assert manualintegrate(x*atan(a*x), x) == -a*(x/a**2 - atan(x/sqrt(a**(-2)))/(a**4*sqrt(a**(-2))))/2 + x**2*atan(a*x)/2
    # acsc
    assert manualintegrate(acsc(x), x) == x*acsc(x) + Integral(1/(x*sqrt(1 - 1/x**2)), x)
    assert manualintegrate(acsc(a*x), x) == x*acsc(a*x) + Integral(1/(x*sqrt(1 - 1/(a**2*x**2))), x)/a
    assert manualintegrate(x*acsc(a*x), x) == x**2*acsc(a*x)/2 + Integral(1/sqrt(1 - 1/(a**2*x**2)), x)/(2*a)
    # asec
    assert manualintegrate(asec(x), x) == x*asec(x) - Integral(1/(x*sqrt(1 - 1/x**2)), x)
    assert manualintegrate(asec(a*x), x) == x*asec(a*x) - Integral(1/(x*sqrt(1 - 1/(a**2*x**2))), x)/a
    assert manualintegrate(x*asec(a*x), x) == x**2*asec(a*x)/2 - Integral(1/sqrt(1 - 1/(a**2*x**2)), x)/(2*a)
    # acot
    assert manualintegrate(acot(x), x) == x*acot(x) + log(x**2 + 1)/2
    assert manualintegrate(acot(a*x), x) == Piecewise(((a*x*acot(a*x) + log(a**2*x**2 + 1)/2)/a, Ne(a, 0)), (pi*x/2, True))
    assert manualintegrate(x*acot(a*x), x) == a*(x/a**2 - atan(x/sqrt(a**(-2)))/(a**4*sqrt(a**(-2))))/2 + x**2*acot(a*x)/2

    # piecewise
    assert manualintegrate(1/sqrt(ra-rb*x**2), x) == \
        Piecewise((asin(x*sqrt(rb/ra))/sqrt(rb), And(-rb < 0, ra > 0)),
                  (asinh(x*sqrt(-rb/ra))/sqrt(-rb), And(-rb > 0, ra > 0)),
                  (log(-2*rb*x + 2*sqrt(-rb)*sqrt(ra - rb*x**2))/sqrt(-rb), Ne(rb, 0)),
                  (x/sqrt(ra), True))
    assert manualintegrate(1/sqrt(ra + rb*x**2), x) == \
        Piecewise((asin(x*sqrt(-rb/ra))/sqrt(-rb), And(ra > 0, rb < 0)),
                  (asinh(x*sqrt(rb/ra))/sqrt(rb), And(ra > 0, rb > 0)),
                  (log(2*sqrt(rb)*sqrt(ra + rb*x**2) + 2*rb*x)/sqrt(rb), Ne(rb, 0)),
                  (x/sqrt(ra), True))

