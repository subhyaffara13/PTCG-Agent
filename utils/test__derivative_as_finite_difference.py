
def test_Derivative_as_finite_difference():
    # Central 1st derivative at gridpoint
    x, h = symbols('x h', real=True)
    dfdx = f(x).diff(x)
    assert (dfdx.as_finite_difference([x-2, x-1, x, x+1, x+2]) -
            (S.One/12*(f(x-2)-f(x+2)) + Rational(2, 3)*(f(x+1)-f(x-1)))).simplify() == 0

    # Central 1st derivative "half-way"
    assert (dfdx.as_finite_difference() -
            (f(x + S.Half)-f(x - S.Half))).simplify() == 0
    assert (dfdx.as_finite_difference(h) -
            (f(x + h/S(2))-f(x - h/S(2)))/h).simplify() == 0
    assert (dfdx.as_finite_difference([x - 3*h, x-h, x+h, x + 3*h]) -
            (S(9)/(8*2*h)*(f(x+h) - f(x-h)) +
             S.One/(24*2*h)*(f(x - 3*h) - f(x + 3*h)))).simplify() == 0

    # One sided 1st derivative at gridpoint
    assert (dfdx.as_finite_difference([0, 1, 2], 0) -
            (Rational(-3, 2)*f(0) + 2*f(1) - f(2)/2)).simplify() == 0
    assert (dfdx.as_finite_difference([x, x+h], x) -
            (f(x+h) - f(x))/h).simplify() == 0
    assert (dfdx.as_finite_difference([x-h, x, x+h], x-h) -
            (-S(3)/(2*h)*f(x-h) + 2/h*f(x) -
             S.One/(2*h)*f(x+h))).simplify() == 0

    # One sided 1st derivative "half-way"
    assert (dfdx.as_finite_difference([x-h, x+h, x + 3*h, x + 5*h, x + 7*h])
            - 1/(2*h)*(-S(11)/(12)*f(x-h) + S(17)/(24)*f(x+h)
                       + Rational(3, 8)*f(x + 3*h) - Rational(5, 24)*f(x + 5*h)
                       + S.One/24*f(x + 7*h))).simplify() == 0

    d2fdx2 = f(x).diff(x, 2)
    # Central 2nd derivative at gridpoint
    assert (d2fdx2.as_finite_difference([x-h, x, x+h]) -
            h**-2 * (f(x-h) + f(x+h) - 2*f(x))).simplify() == 0

    assert (d2fdx2.as_finite_difference([x - 2*h, x-h, x, x+h, x + 2*h]) -
            h**-2 * (Rational(-1, 12)*(f(x - 2*h) + f(x + 2*h)) +
                     Rational(4, 3)*(f(x+h) + f(x-h)) - Rational(5, 2)*f(x))).simplify() == 0

    # Central 2nd derivative "half-way"
    assert (d2fdx2.as_finite_difference([x - 3*h, x-h, x+h, x + 3*h]) -
            (2*h)**-2 * (S.Half*(f(x - 3*h) + f(x + 3*h)) -
                         S.Half*(f(x+h) + f(x-h)))).simplify() == 0

    # One sided 2nd derivative at gridpoint
    assert (d2fdx2.as_finite_difference([x, x+h, x + 2*h, x + 3*h]) -
            h**-2 * (2*f(x) - 5*f(x+h) +
                     4*f(x+2*h) - f(x+3*h))).simplify() == 0

    # One sided 2nd derivative at "half-way"
    assert (d2fdx2.as_finite_difference([x-h, x+h, x + 3*h, x + 5*h]) -
            (2*h)**-2 * (Rational(3, 2)*f(x-h) - Rational(7, 2)*f(x+h) + Rational(5, 2)*f(x + 3*h) -
                         S.Half*f(x + 5*h))).simplify() == 0

    d3fdx3 = f(x).diff(x, 3)
    # Central 3rd derivative at gridpoint
    assert (d3fdx3.as_finite_difference() -
            (-f(x - Rational(3, 2)) + 3*f(x - S.Half) -
             3*f(x + S.Half) + f(x + Rational(3, 2)))).simplify() == 0

    assert (d3fdx3.as_finite_difference(
        [x - 3*h, x - 2*h, x-h, x, x+h, x + 2*h, x + 3*h]) -
        h**-3 * (S.One/8*(f(x - 3*h) - f(x + 3*h)) - f(x - 2*h) +
                 f(x + 2*h) + Rational(13, 8)*(f(x-h) - f(x+h)))).simplify() == 0

    # Central 3rd derivative at "half-way"
    assert (d3fdx3.as_finite_difference([x - 3*h, x-h, x+h, x + 3*h]) -
            (2*h)**-3 * (f(x + 3*h)-f(x - 3*h) +
                         3*(f(x-h)-f(x+h)))).simplify() == 0

    # One sided 3rd derivative at gridpoint
    assert (d3fdx3.as_finite_difference([x, x+h, x + 2*h, x + 3*h]) -
            h**-3 * (f(x + 3*h)-f(x) + 3*(f(x+h)-f(x + 2*h)))).simplify() == 0

    # One sided 3rd derivative at "half-way"
    assert (d3fdx3.as_finite_difference([x-h, x+h, x + 3*h, x + 5*h]) -
            (2*h)**-3 * (f(x + 5*h)-f(x-h) +
                         3*(f(x+h)-f(x + 3*h)))).simplify() == 0

    # issue 11007
    y = Symbol('y', real=True)
    d2fdxdy = f(x, y).diff(x, y)

    ref0 = Derivative(f(x + S.Half, y), y) - Derivative(f(x - S.Half, y), y)
    assert (d2fdxdy.as_finite_difference(wrt=x) - ref0).simplify() == 0

    half = S.Half
    xm, xp, ym, yp = x-half, x+half, y-half, y+half
    ref2 = f(xm, ym) + f(xp, yp) - f(xp, ym) - f(xm, yp)
    assert (d2fdxdy.as_finite_difference() - ref2).simplify() == 0

