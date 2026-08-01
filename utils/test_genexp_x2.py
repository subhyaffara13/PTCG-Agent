
def test_genexp_x2():
    p = Rational(3, 2)
    e = (2/x + 3/x**p)/(1/x + 1/x**p)
    assert e.nseries(x, 0, 3) == 3 + x + x**2 - sqrt(x) - x**(S(3)/2) - x**(S(5)/2) + O(x**3)

