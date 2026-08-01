
def test_axis_swapaxes():
    A = coo_array([[2, 0], [3, 5]])
    with assert_raises(ValueError, match="Invalid axis"):
        construct.swapaxes(A, -4, 0)
    with assert_raises(ValueError, match="Invalid axis"):
        construct.swapaxes(A, 0, -4)
    with assert_raises(ValueError, match="Invalid axis"):
        construct.swapaxes(A, 3, 0)
    with assert_raises(ValueError, match="Invalid axis"):
        construct.swapaxes(A, 0, 3)
    with assert_raises(ValueError, match="Invalid axis"):
        construct.swapaxes(A, 1.2, 1)
    with assert_raises(ValueError, match="Invalid axis"):
        construct.swapaxes(A, 1, 1.2)
    assert_equal(construct.swapaxes(A, 0, 0).toarray(), A.toarray())
    for i in range(2):
        assert_equal(
            construct.swapaxes(A, i, 1 - i).toarray(),
            construct.swapaxes(A, i - 2, -1 - i).toarray()
        )

