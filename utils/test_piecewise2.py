
def test_piecewise2():
    func1 = 2*sqrt(x)*Piecewise(((4*x - 2)/Abs(sqrt(4 - 4*(2*x - 1)**2)), 4*x - 2\
            >= 0), ((2 - 4*x)/Abs(sqrt(4 - 4*(2*x - 1)**2)), True))
    func2 = Piecewise((x**2/2, x <= 0.5), (x/2 - 0.125, True))
    func3 = Piecewise(((x - 9) / 5, x < -1), ((x - 9) / 5, x > 4), (sqrt(Abs(x - 3)), True))
    assert limit(func1, x, 0) == 1
    assert limit(func2, x, 0) == 0
    assert limit(func3, x, -1) == 2

