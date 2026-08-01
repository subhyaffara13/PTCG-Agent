
def test_V2():
    assert integrate(Piecewise((-x, x < 0), (x, x >= 0)), x
        ) == Piecewise((-x**2/2, x < 0), (x**2/2, True))

