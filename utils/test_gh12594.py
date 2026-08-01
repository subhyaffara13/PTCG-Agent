
def test_gh12594():
    # gh-12594 reported an error in `_linesearch_powell` and
    # `_line_for_search` when `Bounds` was passed lists instead of arrays.
    # Check that results are the same whether the inputs are lists or arrays.

    def f(x):
        return x[0]**2 + (x[1] - 1)**2

    bounds = Bounds(lb=[-10, -10], ub=[10, 10])
    res = optimize.minimize(f, x0=(0, 0), method='Powell', bounds=bounds)
    bounds = Bounds(lb=np.array([-10, -10]), ub=np.array([10, 10]))
    ref = optimize.minimize(f, x0=(0, 0), method='Powell', bounds=bounds)

    assert_allclose(res.fun, ref.fun)
    assert_allclose(res.x, ref.x)

