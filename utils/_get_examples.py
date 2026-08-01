
def _get_examples():
    fo = fourier_series(x, (x, -pi, pi))
    fe = fourier_series(x**2, (-pi, pi))
    fp = fourier_series(Piecewise((0, x < 0), (pi, True)), (x, -pi, pi))
    return fo, fe, fp

