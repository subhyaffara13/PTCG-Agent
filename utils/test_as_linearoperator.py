
def test_as_linearoperator(A):
    L = spla.aslinearoperator(A)
    npt.assert_allclose(L * [1, 2, 3, 4], A @ [1, 2, 3, 4])

