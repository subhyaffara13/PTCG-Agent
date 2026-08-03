import re

def test_messy():
    from sympy.functions.elementary.hyperbolic import (acosh, acoth)
    from sympy.functions.elementary.trigonometric import (asin, atan)
    from sympy.functions.special.bessel import besselj
    from sympy.functions.special.error_functions import (Chi, E1, Shi, Si)
    from sympy.integrals.transforms import (fourier_transform, laplace_transform)
    assert (laplace_transform(Si(x), x, s, simplify=True) ==
            ((-atan(s) + pi/2)/s, 0, True))

    assert laplace_transform(Shi(x), x, s, simplify=True) == (
        acoth(s)/s, -oo, s**2 > 1)

    # where should the logs be simplified?
    assert laplace_transform(Chi(x), x, s, simplify=True) == (
        (log(s**(-2)) - log(1 - 1/s**2))/(2*s), -oo, s**2 > 1)

    # TODO maybe simplify the inequalities? when the simplification
    # allows for generators instead of symbols this will work
    assert laplace_transform(besselj(a, x), x, s)[1:] == \
        (0, (re(a) > -2) & (re(a) > -1))

    # NOTE s < 0 can be done, but argument reduction is not good enough yet
    ans = fourier_transform(besselj(1, x)/x, x, s, noconds=False)
    assert (ans[0].factor(deep=True).expand(), ans[1]) == \
        (Piecewise((0, (s > 1/(2*pi)) | (s < -1/(2*pi))),
                   (2*sqrt(-4*pi**2*s**2 + 1), True)), s > 0)
    # TODO FT(besselj(0,x)) - conditions are messy (but for acceptable reasons)
    #                       - folding could be better

    assert integrate(E1(x)*besselj(0, x), (x, 0, oo), meijerg=True) == \
        log(1 + sqrt(2))
    assert integrate(E1(x)*besselj(1, x), (x, 0, oo), meijerg=True) == \
        log(S.Half + sqrt(2)/2)

    assert integrate(1/x/sqrt(1 - x**2), x, meijerg=True) == \
        Piecewise((-acosh(1/x), abs(x**(-2)) > 1), (I*asin(1/x), True))

