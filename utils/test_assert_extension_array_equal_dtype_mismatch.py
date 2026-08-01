
def test_assert_extension_array_equal_dtype_mismatch(check_dtype):
    end = 5
    kwargs = {"check_dtype": check_dtype}

    arr1 = SparseArray(np.arange(end, dtype="int64"))
    arr2 = SparseArray(np.arange(end, dtype="int32"))

    if check_dtype:
        msg = """\
ExtensionArray are different

Attribute "dtype" are different
\\[left\\]:  Sparse\\[int64, 0\\]
\\[right\\]: Sparse\\[int32, 0\\]"""

        with pytest.raises(AssertionError, match=msg):
            tm.assert_extension_array_equal(arr1, arr2, **kwargs)
    else:
        tm.assert_extension_array_equal(arr1, arr2, **kwargs)

