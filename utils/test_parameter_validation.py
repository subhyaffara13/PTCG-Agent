
def test_parameter_validation():
    x = [0, 1, 0.5]
    y = np.zeros((2, 3))
    assert_raises(ValueError, solve_bvp, exp_fun, exp_bc, x, y)

    x = np.linspace(0, 1, 5)
    y = np.zeros((2, 4))
    assert_raises(ValueError, solve_bvp, exp_fun, exp_bc, x, y)

    def fun(x, y, p):
        return exp_fun(x, y)
    def bc(ya, yb, p):
        return exp_bc(ya, yb)

    y = np.zeros((2, x.shape[0]))
    assert_raises(ValueError, solve_bvp, fun, bc, x, y, p=[1])

    def wrong_shape_fun(x, y):
        return np.zeros(3)

    assert_raises(ValueError, solve_bvp, wrong_shape_fun, bc, x, y)

    S = np.array([[0, 0]])
    assert_raises(ValueError, solve_bvp, exp_fun, exp_bc, x, y, S=S)

