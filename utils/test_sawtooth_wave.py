
def test_sawtooth_wave():
    s = fourier_series(x, (x, 0, pi))
    assert s.truncate(4) == \
        pi/2 - sin(2*x) - sin(4*x)/2 - sin(6*x)/3
    s = fourier_series(x, (x, 0, 1))
    assert s.truncate(4) == \
        S.Half - sin(2*pi*x)/pi - sin(4*pi*x)/(2*pi) - sin(6*pi*x)/(3*pi)

