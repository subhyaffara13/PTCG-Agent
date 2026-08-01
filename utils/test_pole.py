
def test_pole():
    raises(PoleError, lambda: sin(1/x).series(x, 0, 5))
    raises(PoleError, lambda: sin(1 + 1/x).series(x, 0, 5))
    raises(PoleError, lambda: (x*sin(1/x)).series(x, 0, 5))

