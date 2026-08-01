
def test_gh_14486_converged_false():
    """Test that zero slope with secant method results in a converged=False"""
    def lhs(x):
        return x * np.exp(-x*x) - 0.07

    with pytest.warns(RuntimeWarning, match='Tolerance of'):
        res = root_scalar(lhs, method='secant', x0=-0.15, x1=1.0)
    assert not res.converged
    assert res.flag == 'convergence error'

    with pytest.warns(RuntimeWarning, match='Tolerance of'):
        res = newton(lhs, x0=-0.15, x1=1.0, disp=False, full_output=True)[1]
    assert not res.converged
    assert res.flag == 'convergence error'

