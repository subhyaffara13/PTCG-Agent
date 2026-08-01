
def test_3d_permute_dims():
    tgt = [[[0], [2], [0], [6]], [[1], [0], [5], [7]]]
    x = np.array([[[0, 1], [2, 0], [0, 5], [6, 7]]])
    A = coo_array(x)

    out = construct.permute_dims(A, axes=(2, 1, 0))
    assert_equal(out.shape, (2, 4, 1))
    assert_equal(out.toarray(), tgt)
    # TODO change np.transpose to np.permute_dims when numpy 2 is min supported version
    assert_equal(out.toarray(), np.transpose(x, axes=(2, 1, 0)))

