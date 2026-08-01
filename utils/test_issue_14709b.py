
def test_issue_14709b():
    h = Symbol('h', positive=True)
    i = integrate(x*acos(1 - 2*x/h), (x, 0, h))
    assert i == 5*h**2*pi/16

