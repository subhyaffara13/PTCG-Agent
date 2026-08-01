
def test_apply_finite_diff():
    x, h = symbols('x h')
    f = Function('f')
    assert (apply_finite_diff(1, [x-h, x+h], [f(x-h), f(x+h)], x) -
            (f(x+h)-f(x-h))/(2*h)).simplify() == 0

    assert (apply_finite_diff(1, [5, 6, 7], [f(5), f(6), f(7)], 5) -
            (Rational(-3, 2)*f(5) + 2*f(6) - S.Half*f(7))).simplify() == 0
    raises(ValueError, lambda: apply_finite_diff(1, [x, h], [f(x)]))

