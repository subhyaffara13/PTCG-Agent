
def test_3d_swapaxes():
    tgt = [[[0, 0], [2, 6]], [[1, 5], [0, 7]]]
    x = np.array([[[0, 1], [2, 0]], [[0, 5], [6, 7]]])
    A = coo_array(x) #[[[0, 1], [2, 0]], [[0, 5], [6, 7]]])
    out = construct.swapaxes(A, 0, 2)
    assert_equal(out.toarray(), tgt)
    assert_equal(out.toarray(), np.swapaxes(x, 0, 2))

