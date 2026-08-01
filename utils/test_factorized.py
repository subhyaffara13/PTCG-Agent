
def test_factorized(B):
    if B.__class__.__name__[:3] != 'csc':
        return

    LU = spla.factorized(B)
    npt.assert_allclose(
        LU(np.array([1, 2])),
        np.linalg.solve(B.todense(), [1, 2])
    )

