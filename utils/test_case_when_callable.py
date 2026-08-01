
def test_case_when_callable():
    """
    Test output on a callable
    """
    # https://numpy.org/doc/stable/reference/generated/numpy.piecewise.html
    x = np.linspace(-2.5, 2.5, 6)
    ser = Series(x)
    result = ser.case_when(
        caselist=[
            (lambda df: df < 0, lambda df: -df),
            (lambda df: df >= 0, lambda df: df),
        ]
    )
    expected = np.piecewise(x, [x < 0, x >= 0], [lambda x: -x, lambda x: x])
    tm.assert_series_equal(result, Series(expected))

