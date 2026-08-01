
def test_solvers(B, solver):
    if solver == "minres":
        kwargs = {}
    else:
        kwargs = {'atol': 1e-5}

    x, info = getattr(spla, solver)(B, np.array([1, 2]), **kwargs)
    assert info >= 0  # no errors, even if perhaps did not converge fully
    npt.assert_allclose(x, [1, 1], atol=1e-1)

