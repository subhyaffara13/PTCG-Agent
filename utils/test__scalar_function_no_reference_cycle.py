
def test_ScalarFunctionNoReferenceCycle():
    """Regression test for gh-20768."""
    ex = ExScalarFunction()
    x0 = np.zeros(3)
    with assert_deallocated(lambda: ScalarFunction(ex.fun, x0, (), ex.grad,
                            ex.hess, None, (-np.inf, np.inf))):
        pass

