
def test_sparse_format_swapaxes(format):
    A = np.array([[2, 0, 1], [3, 5, 0]])
    SA = coo_array(A).asformat(format)

    out = construct.swapaxes(SA, 1, 0)
    assert out.format == "coo"
    assert out.shape == (3, 2)
    assert_equal(out.toarray(), np.swapaxes(A, 1, 0))
    assert not out.has_canonical_format

