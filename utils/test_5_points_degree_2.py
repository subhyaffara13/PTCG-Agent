
def test_5_points_degree_2():
    d = 2
    X = [-3, 2, 4, 5, 10]
    Y = [-1, 2, 5, 10, 14]
    spline = interpolating_spline(d, x, X, Y)

    assert spline == Piecewise((4*x**2/329 + x*Rational(1007, 1645) + Rational(1196, 1645), (x >= -3) & (x <= 3)),
                               (2701*x**2/1645 - x*Rational(15079, 1645) + Rational(5065, 329), (x >= 3) & (x <= Rational(9, 2))),
                               (-1319*x**2/1645 + x*Rational(21101, 1645) - Rational(11216, 329), (x >= Rational(9, 2)) & (x <= 10)))

