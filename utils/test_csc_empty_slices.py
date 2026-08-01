
def test_csc_empty_slices(matrix_input, axis, expected_shape):
    # see gh-11127 for related discussion
    slice_1 = matrix_input.toarray().shape[0] - 1
    slice_2 = slice_1
    slice_3 = slice_2 - 1

    if axis == 0:
        actual_shape_1 = matrix_input[slice_1:slice_2, :].toarray().shape
        actual_shape_2 = matrix_input[slice_1:slice_3, :].toarray().shape
    elif axis == 1:
        actual_shape_1 = matrix_input[:, slice_1:slice_2].toarray().shape
        actual_shape_2 = matrix_input[:, slice_1:slice_3].toarray().shape
    elif axis == 'both':
        actual_shape_1 = matrix_input[slice_1:slice_2, slice_1:slice_2].toarray().shape
        actual_shape_2 = matrix_input[slice_1:slice_3, slice_1:slice_3].toarray().shape

    assert actual_shape_1 == expected_shape
    assert actual_shape_1 == actual_shape_2

