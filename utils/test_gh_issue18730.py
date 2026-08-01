
def test_gh_issue18730():
    # issue 18730 reported that l-bfgs-b did not work with objectives
    # returning single precision gradient arrays
    def fun_single_precision(x):
        x = x.astype(np.float32)
        return np.sum(x**2), (2*x)

    res = minimize(fun_single_precision, x0=np.array([1., 1.]), jac=True,
                   method="l-bfgs-b")
    np.testing.assert_allclose(res.fun, 0., atol=1e-15)

