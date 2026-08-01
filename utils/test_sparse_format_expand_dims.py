
def test_sparse_format_expand_dims(format):
    A = np.array([[2, 0], [3, 5]])
    SA = coo_array(A).asformat(format)

    out = construct.expand_dims(SA, axis=1)
    assert out.format == "coo"
    assert out.shape == (2, 1, 2)
    assert_equal(out.toarray(), np.expand_dims(A, axis=1))
    assert SA.tocoo().has_canonical_format == out.has_canonical_format

