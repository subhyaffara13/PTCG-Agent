
def test_elementwise_rmul(A):
    with pytest.raises(TypeError):
        None * A

    with pytest.raises(ValueError):
        np.eye(3) * scipy.sparse.csr_array(np.arange(6).reshape(2, 3))

    assert np.all((2 * A) == (A.todense() * 2))

    assert np.all((A.todense() * A) == (A.todense() ** 2))

