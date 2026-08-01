
def test_complex_range_line_plot_1():
    # verify that univariate functions are evaluated with a complex
    # data range (with zero imaginary part). There shouldn't be any
    # NaN value in the output.
    if not np:
        skip("numpy not installed.")

    x, u = symbols("x, u")
    expr1 = im(sqrt(x) * exp(-x**2))
    expr2 = im(sqrt(u * x) * exp(-x**2))
    s1 = LineOver1DRangeSeries(expr1, (x, -10, 10), adaptive=True,
        adaptive_goal=0.1)
    s2 = LineOver1DRangeSeries(expr1, (x, -10, 10), adaptive=False, n=30)
    s3 = LineOver1DRangeSeries(expr2, (x, -10, 10), adaptive=False, n=30,
        params={u: 1})

    with ignore_warnings(RuntimeWarning):
        data1 = s1.get_data()
    data2 = s2.get_data()
    data3 = s3.get_data()

    assert not np.isnan(data1[1]).any()
    assert not np.isnan(data2[1]).any()
    assert not np.isnan(data3[1]).any()
    assert np.allclose(data2[0], data3[0]) and np.allclose(data2[1], data3[1])

