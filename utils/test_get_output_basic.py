
def test_get_output_basic(dtype):
    shape = (2, 3)

    input_ = np.zeros(shape, dtype='float32')

    # For None, derive dtype from input
    expected_dtype = 'float32' if dtype is None else dtype

    # Output is dtype-specifier, retrieve shape from input
    result = _get_output(dtype, input_)
    assert result.shape == shape
    assert result.dtype == np.dtype(expected_dtype)

    # Output is dtype specifier, with explicit shape, overriding input
    result = _get_output(dtype, input_, shape=(3, 2))
    assert result.shape == (3, 2)
    assert result.dtype == np.dtype(expected_dtype)

    # Output is pre-allocated array, return directly
    output = np.zeros(shape, dtype=dtype)
    result = _get_output(output, input_)
    assert result is output

