
def test_lstsqr(A, solver):
    x, *_ = getattr(spla, solver)(A, [1, 2, 3])
    npt.assert_allclose(A @ x, [1, 2, 3])

