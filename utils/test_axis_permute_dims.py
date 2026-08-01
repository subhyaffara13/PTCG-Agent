
def test_axis_permute_dims():
    A = coo_array([[2, 0, 1], [3, 5, 0]])

    with assert_raises(ValueError, match="Incorrect number of axes"):
        construct.permute_dims(A, axes=(2, 0, 1))
    with assert_raises(ValueError, match="duplicate value in axis"):
        construct.permute_dims(A, axes=(0, 0))
    with assert_raises(TypeError, match="axis must be an integer/tuple"):
        construct.permute_dims(A, axes={1, 0})

    with assert_raises(ValueError, match="axis out of range"):
        construct.permute_dims(A, axes=(-3, 0))
    with assert_raises(ValueError, match="axis out of range"):
        construct.permute_dims(A, axes=(0, -3))
    with assert_raises(ValueError, match="axis out of range"):
        construct.permute_dims(A, axes=(2, 0))
    with assert_raises(ValueError, match="axis out of range"):
        construct.permute_dims(A, axes=(0, 2))
    with assert_raises(TypeError, match="axis must be an integer"):
        construct.permute_dims(A, axes=(1.2, 0))

    assert_equal(
        construct.permute_dims(A, axes=(1, 0), copy=True).toarray(),
        A.transpose(axes=(1, 0), copy=True).toarray()
    )
    # use lists for axes
    assert_equal(
        construct.permute_dims(A, axes=[1, 0], copy=True).toarray(),
        A.transpose(axes=[1, 0], copy=True).toarray()
    )
    assert_equal(
        construct.permute_dims(A, axes=None, copy=True).toarray(),
        A.transpose(axes=(1, 0), copy=True).toarray()
    )
    assert_equal(
        construct.permute_dims(A, axes=(0, 1), copy=True).toarray(), A.toarray()
    )

