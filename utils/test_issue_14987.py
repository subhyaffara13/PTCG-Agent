
def test_issue_14987():
    raises(ValueError, lambda: linear_eq_to_matrix(
        [x**2], x))
    raises(ValueError, lambda: linear_eq_to_matrix(
        [x*(-3/x + 1) + 2*y - a], [x, y]))
    raises(ValueError, lambda: linear_eq_to_matrix(
        [(x**2 - 3*x)/(x - 3) - 3], x))
    raises(ValueError, lambda: linear_eq_to_matrix(
        [(x + 1)**3 - x**3 - 3*x**2 + 7], x))
    raises(ValueError, lambda: linear_eq_to_matrix(
        [x*(1/x + 1) + y], [x, y]))
    raises(ValueError, lambda: linear_eq_to_matrix(
        [(x + 1)*y], [x, y]))
    raises(ValueError, lambda: linear_eq_to_matrix(
        [Eq(1/x, 1/x + y)], [x, y]))
    raises(ValueError, lambda: linear_eq_to_matrix(
        [Eq(y/x, y/x + y)], [x, y]))
    raises(ValueError, lambda: linear_eq_to_matrix(
        [Eq(x*(x + 1), x**2 + y)], [x, y]))

