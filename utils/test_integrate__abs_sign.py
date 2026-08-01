
def test_integrate_Abs_sign():
    assert integrate(Abs(x), (x, -2, 1)) == Rational(5, 2)
    assert integrate(Abs(x), (x, 0, 1)) == S.Half
    assert integrate(Abs(x + 1), (x, 0, 1)) == Rational(3, 2)
    assert integrate(Abs(x**2 - 1), (x, -2, 2)) == 4
    assert integrate(Abs(x**2 - 3*x), (x, -15, 15)) == 2259
    assert integrate(sign(x), (x, -1, 2)) == 1
    assert integrate(sign(x)*sin(x), (x, -pi, pi)) == 4
    assert integrate(sign(x - 2) * x**2, (x, 0, 3)) == Rational(11, 3)

    t, s = symbols('t s', real=True)
    assert integrate(Abs(t), t) == Piecewise(
        (-t**2/2, t <= 0), (t**2/2, True))
    assert integrate(Abs(2*t - 6), t) == Piecewise(
        (-t**2 + 6*t, t <= 3), (t**2 - 6*t + 18, True))
    assert (integrate(abs(t - s**2), (t, 0, 2)) ==
        2*s**2*Min(2, s**2) - 2*s**2 - Min(2, s**2)**2 + 2)
    assert integrate(exp(-Abs(t)), t) == Piecewise(
        (exp(t), t <= 0), (2 - exp(-t), True))
    assert integrate(sign(2*t - 6), t) == Piecewise(
        (-t, t < 3), (t - 6, True))
    assert integrate(2*t*sign(t**2 - 1), t) == Piecewise(
        (t**2, t < -1), (-t**2 + 2, t < 1), (t**2, True))
    assert integrate(sign(t), (t, s + 1)) == Piecewise(
        (s + 1, s + 1 > 0), (-s - 1, s + 1 < 0), (0, True))

