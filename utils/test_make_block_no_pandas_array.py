
def test_make_block_no_pandas_array(block_maker):
    # https://github.com/pandas-dev/pandas/pull/24866
    arr = pd.arrays.NumpyExtensionArray(np.array([1, 2]))

    depr_msg = "make_block is deprecated"
    warn = DeprecationWarning if block_maker is make_block else None

    # NumpyExtensionArray, no dtype
    with tm.assert_produces_warning(warn, match=depr_msg):
        result = block_maker(arr, BlockPlacement(slice(len(arr))), ndim=arr.ndim)
    assert result.dtype.kind in ["i", "u"]

    if block_maker is make_block:
        # new_block requires caller to unwrap NumpyExtensionArray
        assert result.is_extension is False

        # NumpyExtensionArray, NumpyEADtype
        with tm.assert_produces_warning(warn, match=depr_msg):
            result = block_maker(arr, slice(len(arr)), dtype=arr.dtype, ndim=arr.ndim)
        assert result.dtype.kind in ["i", "u"]
        assert result.is_extension is False

        # new_block no longer accepts dtype keyword
        # ndarray, NumpyEADtype
        with tm.assert_produces_warning(warn, match=depr_msg):
            result = block_maker(
                arr.to_numpy(), slice(len(arr)), dtype=arr.dtype, ndim=arr.ndim
            )
        assert result.dtype.kind in ["i", "u"]
        assert result.is_extension is False

