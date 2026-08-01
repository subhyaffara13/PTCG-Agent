
def test_FourierSeries__add__sub():
    fo, fe, fp = _get_examples()

    assert fo + fo == fo.scale(2)
    assert fo - fo == 0
    assert -fe - fe == fe.scale(-2)

    assert (fo + fe).truncate() == 2*sin(x) - sin(2*x) - 4*cos(x) + cos(2*x) \
        + pi**2 / 3
    assert (fo - fe).truncate() == 2*sin(x) - sin(2*x) + 4*cos(x) - cos(2*x) \
        - pi**2 / 3

    assert isinstance(fo + 1, Add)

    raises(ValueError, lambda: fo + fourier_series(x, (x, 0, 2)))

