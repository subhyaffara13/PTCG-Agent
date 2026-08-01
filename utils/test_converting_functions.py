
def test_converting_functions():
    arr_list = [1, 2, 3, 4]
    arr_matrix = Matrix(((1, 2), (3, 4)))

    # list
    arr_ndim_array = ImmutableDenseNDimArray(arr_list, (2, 2))
    assert (isinstance(arr_ndim_array, ImmutableDenseNDimArray))
    assert arr_matrix.tolist() == arr_ndim_array.tolist()

    # Matrix
    arr_ndim_array = ImmutableDenseNDimArray(arr_matrix)
    assert (isinstance(arr_ndim_array, ImmutableDenseNDimArray))
    assert arr_matrix.tolist() == arr_ndim_array.tolist()
    assert arr_matrix.shape == arr_ndim_array.shape


def test_converting_functions():
    arr_list = [1, 2, 3, 4]
    arr_matrix = Matrix(((1, 2), (3, 4)))

    # list
    arr_ndim_array = MutableDenseNDimArray(arr_list, (2, 2))
    assert (isinstance(arr_ndim_array, MutableDenseNDimArray))
    assert arr_matrix.tolist() == arr_ndim_array.tolist()

    # Matrix
    arr_ndim_array = MutableDenseNDimArray(arr_matrix)
    assert (isinstance(arr_ndim_array, MutableDenseNDimArray))
    assert arr_matrix.tolist() == arr_ndim_array.tolist()
    assert arr_matrix.shape == arr_ndim_array.shape

