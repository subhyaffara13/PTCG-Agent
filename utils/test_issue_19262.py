
def test_issue_19262():
    Delta = symbols('Delta', positive=True)
    knots = [i*Delta for i in range(4)]
    basis = bspline_basis_set(1, knots, x)
    y = symbols('y', nonnegative=True)
    basis2 = bspline_basis_set(1, knots, y)
    assert basis[0].subs(x, y) == basis2[0]
    assert interpolating_spline(1, x,
        [Delta*i for i in [1, 2, 4, 7]], [3, 6, 5, 7]
        )  == Piecewise((3*x/Delta, (Delta <= x) & (x <= 2*Delta)),
        (7 - x/(2*Delta), (x >= 2*Delta) & (x <= 4*Delta)),
        (Rational(7, 3) + 2*x/(3*Delta), (x >= 4*Delta) & (x <= 7*Delta)))

