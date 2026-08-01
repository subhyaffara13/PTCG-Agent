
def test_axis_expand_dims():
    A = coo_array([[2, 0], [3, 5]])
    with assert_raises(ValueError, match="Invalid axis"):
        construct.expand_dims(A, axis=-4)
    with assert_raises(ValueError, match="Invalid axis"):
        construct.expand_dims(A, axis=3)
    with assert_raises(ValueError, match="Invalid axis"):
        construct.expand_dims(A, axis=1.2)
    for i in range(3):
        assert_equal(
            construct.expand_dims(A, axis=i).toarray(),
            construct.expand_dims(A, axis=i - 3).toarray()
        )

