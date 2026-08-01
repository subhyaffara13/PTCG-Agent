
def test_spmatrix_subscriptable():
    result = csr_matrix[np.int8]
    assert isinstance(result, GenericAlias)
    assert result.__origin__ is csr_matrix
    assert result.__args__ == (np.int8,)

