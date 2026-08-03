import sys

def test_bode():
    if not numpy:
        skip("NumPy is required for this test")

    def bode_phase_evalf(system, point):
        expr = system.to_expr()
        _w = Dummy("w", real=True)
        w_expr = expr.subs({system.var: I*_w})
        return arg(w_expr).subs({_w: point}).evalf()

    def bode_mag_evalf(system, point):
        expr = system.to_expr()
        _w = Dummy("w", real=True)
        w_expr = expr.subs({system.var: I*_w})
        return 20*log(Abs(w_expr), 10).subs({_w: point}).evalf()

    def test_bode_data(sys):
        return y_coordinate_equality(bode_magnitude_numerical_data, bode_mag_evalf, sys) \
            and y_coordinate_equality(bode_phase_numerical_data, bode_phase_evalf, sys)

    assert test_bode_data(tf1)
    assert test_bode_data(tf2)
    assert test_bode_data(tf3)
    assert test_bode_data(tf4)
    assert test_bode_data(tf5)

