
def test_I4():
    assert refine(cos(pi*cos(n*pi)) + sin(pi/2*cos(n*pi)), Q.integer(n)) == (-1)**n - 1

