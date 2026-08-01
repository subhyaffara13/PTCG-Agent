
def test_sympy__series__fourier__FiniteFourierSeries():
    from sympy.series.fourier import fourier_series
    assert _test_args(fourier_series(sin(pi*x), (x, -1, 1)))

