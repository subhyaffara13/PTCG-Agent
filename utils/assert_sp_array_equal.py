
def assert_sp_array_equal(left, right) -> None:
    """
    Check that the left and right SparseArray are equal.

    Parameters
    ----------
    left : SparseArray
    right : SparseArray
    """
    _check_isinstance(left, right, pd.arrays.SparseArray)

    assert_numpy_array_equal(left.sp_values, right.sp_values)

    # SparseIndex comparison
    assert isinstance(left.sp_index, SparseIndex)
    assert isinstance(right.sp_index, SparseIndex)

    left_index = left.sp_index
    right_index = right.sp_index

    if not left_index.equals(right_index):
        raise_assert_detail(
            "SparseArray.index", "index are not equal", left_index, right_index
        )
    else:
        # Just ensure a
        pass

    assert_attr_equal("fill_value", left, right)
    assert_attr_equal("dtype", left, right)
    assert_numpy_array_equal(left.to_dense(), right.to_dense())

