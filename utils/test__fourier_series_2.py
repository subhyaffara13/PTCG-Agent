
def test_FourierSeries_2():
    p = Piecewise((0, x < 0), (x, True))
    f = fourier_series(p, (x, -2, 2))

    assert f.term(3) == (2*sin(3*pi*x / 2) / (3*pi) -
                         4*cos(3*pi*x / 2) / (9*pi**2))
    assert f.truncate() == (2*sin(pi*x / 2) / pi - sin(pi*x) / pi -
                            4*cos(pi*x / 2) / pi**2 + S.Half)

