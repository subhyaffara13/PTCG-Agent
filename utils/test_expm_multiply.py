
def test_expm_multiply(B):
    if B.__class__.__name__[:3] != 'csc':
        return

    npt.assert_allclose(
        spla.expm_multiply(B, np.array([1, 2])),
        spla.expm(B) @ [1, 2]
    )


def test_expm_multiply(matrices):
    A_dense, A_sparse, b = matrices
    x0 = splin.expm_multiply(A_dense, b)
    x = splin.expm_multiply(A_sparse, b)
    assert_allclose(x, x0)

    x0 = splin.expm_multiply(A_dense, A_dense)
    x = splin.expm_multiply(A_sparse, A_sparse)
    assert_allclose(x.todense(), x0)

