
def test_force_real_eval():
    # verify that force_real_eval=True produces inconsistent results when
    # compared with evaluation of complex domain.
    if not np:
        skip("numpy not installed.")

    x = symbols("x")

    expr = im(sqrt(x) * exp(-x**2))
    s1 = LineOver1DRangeSeries(expr, (x, -10, 10), adaptive=False, n=10,
        force_real_eval=False)
    s2 = LineOver1DRangeSeries(expr, (x, -10, 10), adaptive=False, n=10,
        force_real_eval=True)
    d1 = s1.get_data()
    with ignore_warnings(RuntimeWarning):
        d2 = s2.get_data()
    assert not np.allclose(d1[1], 0)
    assert np.allclose(d2[1], 0)

