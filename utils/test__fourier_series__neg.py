
def test_FourierSeries__neg():
    fo, fe, fp = _get_examples()

    assert (-fo).truncate() == -2*sin(x) + sin(2*x) - (2*sin(3*x) / 3)
    assert (-fe).truncate() == +4*cos(x) - cos(2*x) - pi**2 / 3

