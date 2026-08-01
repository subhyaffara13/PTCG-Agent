
def test_assert_extension_array_equal_missing_values():
    arr1 = SparseArray([np.nan, 1, 2, np.nan])
    arr2 = SparseArray([np.nan, 1, 2, 3])

    msg = """\
ExtensionArray NA mask are different

ExtensionArray NA mask values are different \\(25\\.0 %\\)
\\[left\\]:  \\[True, False, False, True\\]
\\[right\\]: \\[True, False, False, False\\]"""

    with pytest.raises(AssertionError, match=msg):
        tm.assert_extension_array_equal(arr1, arr2)

