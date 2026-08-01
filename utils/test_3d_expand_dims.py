
def test_3d_expand_dims():
    tgt = [[[[0, 0], [2, 6]]], [[[1, 5], [0, 7]]]]
    A = coo_array([[[0, 0], [2, 6]], [[1, 5], [0, 7]]])
    out = construct.expand_dims(A, axis=1)
    assert_equal(out.toarray(), tgt)

