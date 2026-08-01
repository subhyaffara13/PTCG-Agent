
def test_integrate_units():
    m = units.m
    s = units.s
    assert integrate(x * m/s, (x, 1*s, 5*s)) == 12*m*s

