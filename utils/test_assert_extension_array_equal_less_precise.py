
def test_assert_extension_array_equal_less_precise(decimals):
    rtol = 0.5 * 10**-decimals
    arr1 = SparseArray([0.5, 0.123456])
    arr2 = SparseArray([0.5, 0.123457])

    if decimals >= 5:
        msg = """\
ExtensionArray are different

ExtensionArray values are different \\(50\\.0 %\\)
\\[left\\]:  \\[0\\.5, 0\\.123456\\]
\\[right\\]: \\[0\\.5, 0\\.123457\\]"""

        with pytest.raises(AssertionError, match=msg):
            tm.assert_extension_array_equal(arr1, arr2, rtol=rtol)
    else:
        tm.assert_extension_array_equal(arr1, arr2, rtol=rtol)

