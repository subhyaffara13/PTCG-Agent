
def test_3_points_degree_2():
    d = 2
    X = [-3, 10, 19]
    Y = [3, -4, 30]
    spline = interpolating_spline(d, x, X, Y)

    assert spline == Piecewise((505*x**2/2574 - x*Rational(4921, 2574) - Rational(1931, 429), (x >= -3) & (x <= 19)))

