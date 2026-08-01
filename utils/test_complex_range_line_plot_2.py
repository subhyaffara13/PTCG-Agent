
def test_complex_range_line_plot_2():
    # verify that univariate functions are evaluated with a complex
    # data range (with non-zero imaginary part). There shouldn't be any
    # NaN value in the output.
    if not np:
        skip("numpy not installed.")

    # NOTE: xfail because sympy's adaptive algorithm is unable to deal with
    # complex number.

    x, u = symbols("x, u")

    # adaptive and uniform meshing should produce the same data.
    # because of the adaptive nature, just compare the first and last points
    # of both series.
    s1 = LineOver1DRangeSeries(abs(sqrt(x)), (x, -5-2j, 5-2j), adaptive=True)
    s2 = LineOver1DRangeSeries(abs(sqrt(x)), (x, -5-2j, 5-2j), adaptive=False,
        n=10)
    with warns(
            RuntimeWarning,
            match="invalid value encountered in sqrt",
            test_stacklevel=False,
        ):
        d1 = s1.get_data()
        d2 = s2.get_data()
        xx1 = [d1[0][0], d1[0][-1]]
        xx2 = [d2[0][0], d2[0][-1]]
        yy1 = [d1[1][0], d1[1][-1]]
        yy2 = [d2[1][0], d2[1][-1]]
        assert np.allclose(xx1, xx2)
        assert np.allclose(yy1, yy2)

