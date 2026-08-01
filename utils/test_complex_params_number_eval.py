
def test_complex_params_number_eval():
    # The main expression contains terms like sqrt(xi - 1), with
    # parameter (0 <= xi <= 1).
    # There shouldn't be any NaN values on the output.
    if not np:
        skip("numpy not installed.")

    xi, wn, x0, v0, t = symbols("xi, omega_n, x0, v0, t")
    x = Function("x")(t)
    eq = x.diff(t, 2) + 2 * xi * wn * x.diff(t) + wn**2 * x
    sol = dsolve(eq, x, ics={x.subs(t, 0): x0, x.diff(t).subs(t, 0): v0})
    params = {
        wn: 0.5,
        xi: 0.25,
        x0: 0.45,
        v0: 0.0
    }
    s = LineOver1DRangeSeries(sol.rhs, (t, 0, 100), adaptive=False, n=5,
        params=params)
    x, y = s.get_data()
    assert not np.isnan(x).any()
    assert not np.isnan(y).any()


    # Fourier Series of a sawtooth wave
    # The main expression contains a Sum with a symbolic upper range.
    # The lambdified code looks like:
    #       sum(blablabla for for n in range(1, m+1))
    # But range requires integer numbers, whereas per above example, the series
    # casts parameters to complex. Verify that the series is able to detect
    # upper bounds in summations and cast it to int in order to get successful
    # evaluation
    x, T, n, m = symbols("x, T, n, m")
    fs = S(1) / 2 - (1 / pi) * Sum(sin(2 * n * pi * x / T) / n, (n, 1, m))
    params = {
        T: 4.5,
        m: 5
    }
    s = LineOver1DRangeSeries(fs, (x, 0, 10), adaptive=False, n=5,
        params=params)
    x, y = s.get_data()
    assert not np.isnan(x).any()
    assert not np.isnan(y).any()

