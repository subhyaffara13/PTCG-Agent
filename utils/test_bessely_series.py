
def test_bessely_series():
    const = 2*S.EulerGamma/pi - 2*log(2)/pi + 2*log(x)/pi
    assert bessely(0, x).series(x, n=4) == const + x**2*(-log(x)/(2*pi)\
        + (2 - 2*S.EulerGamma)/(4*pi) + log(2)/(2*pi)) + O(x**4*log(x))
    assert bessely(1, x).series(x, n=4) == -2/(pi*x) + x*(log(x)/pi - log(2)/pi - \
        (1 - 2*S.EulerGamma)/(2*pi)) + x**3*(-log(x)/(8*pi) + \
        (S(5)/2 - 2*S.EulerGamma)/(16*pi) + log(2)/(8*pi)) + O(x**4*log(x))
    assert bessely(2, x).series(x, n=4) == -4/(pi*x**2) - 1/pi + x**2*(log(x)/(4*pi) - \
        log(2)/(4*pi) - (S(3)/2 - 2*S.EulerGamma)/(8*pi)) + O(x**4*log(x))
    assert bessely(3, x).series(x, n=4) == -16/(pi*x**3) - 2/(pi*x) - \
        x/(4*pi) + x**3*(log(x)/(24*pi) - log(2)/(24*pi) - \
        (S(11)/6 - 2*S.EulerGamma)/(48*pi)) + O(x**4*log(x))
    assert bessely(0, x**(1.1)).series(x, n=4) == 2*S.EulerGamma/pi\
        - 2*log(2)/pi + 2.2*log(x)/pi + x**2.2*(-0.55*log(x)/pi\
        + (2 - 2*S.EulerGamma)/(4*pi) + log(2)/(2*pi)) + O(x**4*log(x))
    assert bessely(0, x**2 + x).series(x, n=4) == \
        const - (2 - 2*S.EulerGamma)*(-x**3/(2*pi) - x**2/(4*pi)) + 2*x/pi\
        + x**2*(-log(x)/(2*pi) - 1/pi + log(2)/(2*pi))\
        + x**3*(-log(x)/pi + 1/(6*pi) + log(2)/pi) + O(x**4*log(x))
    assert bessely(0, x/(1 - x)).series(x, n=3) == const\
        + 2*x/pi + x**2*(-log(x)/(2*pi) + (2 - 2*S.EulerGamma)/(4*pi)\
        + log(2)/(2*pi) + 1/pi) + O(x**3*log(x))
    assert bessely(0, log(1 + x)).series(x, n=3) == const\
        - x/pi + x**2*(-log(x)/(2*pi) + (2 - 2*S.EulerGamma)/(4*pi)\
        + log(2)/(2*pi) + 5/(12*pi)) + O(x**3*log(x))
    assert bessely(1, sin(x)).series(x, n=4) == -1/(pi*(-x**3/12 + x/2)) - \
        (1 - 2*S.EulerGamma)*(-x**3/12 + x/2)/pi + x*(log(x)/pi - log(2)/pi) + \
        x**3*(-7*log(x)/(24*pi) - 1/(6*pi) + (S(5)/2 - 2*S.EulerGamma)/(16*pi) +
        7*log(2)/(24*pi)) + O(x**4*log(x))
    assert bessely(1, 2*sqrt(x)).series(x, n=3) == -1/(pi*sqrt(x)) + \
        sqrt(x)*(log(x)/pi - (1 - 2*S.EulerGamma)/pi) + x**(S(3)/2)*(-log(x)/(2*pi) + \
        (S(5)/2 - 2*S.EulerGamma)/(2*pi)) + x**(S(5)/2)*(log(x)/(12*pi) - \
        (S(10)/3 - 2*S.EulerGamma)/(12*pi)) + O(x**3*log(x))
    assert bessely(-2, sin(x)).series(x, n=4) == bessely(2, sin(x)).series(x, n=4)

