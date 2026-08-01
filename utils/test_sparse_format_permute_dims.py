
def test_sparse_format_permute_dims(format):
    A = np.array([[2, 0, 1], [3, 5, 0]])
    SA = coo_array(A).asformat(format)

    out = construct.permute_dims(SA, axes=(1, 0))
    assert out.format == "coo"
    assert out.shape == (3, 2)
    # TODO change np.transpose to np.permute_dims when numpy 2 is min supported version
    assert_equal(out.toarray(), np.transpose(A, axes=(1, 0)))
    assert not out.has_canonical_format

