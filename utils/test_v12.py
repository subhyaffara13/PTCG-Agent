
def test_V12():
    r1 = integrate(1/(5 + 3*cos(x) + 4*sin(x)), x)
    assert r1 == -1/(tan(x/2) + 2)

