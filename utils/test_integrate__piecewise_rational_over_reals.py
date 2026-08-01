
def test_integrate_Piecewise_rational_over_reals():
    f = Piecewise(
        (0,                                              t - 478.515625*pi <  0),
        (13.2075145209219*pi/(0.000871222*t + 0.995)**2, t - 478.515625*pi >= 0))

    assert abs((integrate(f, (t, 0, oo)) - 15235.9375*pi).evalf()) <= 1e-7

