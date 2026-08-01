
def test_VectorFunctionNoReferenceCycle():
    """Regression test for gh-20768."""
    ex = ExVectorialFunction()
    x0 = [1.0, 0.0]
    with assert_deallocated(lambda: VectorFunction(ex.fun, x0, ex.jac,
                            ex.hess, None, None, (-np.inf, np.inf), None)):
        pass

