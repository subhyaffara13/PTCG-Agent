
def test_sympy__series__fourier__FourierSeries():
    from sympy.series.fourier import fourier_series
    assert _test_args(fourier_series(x, (x, -pi, pi)))

