
def test_assert_extension_array_equal_not_exact(kwargs):
    # see gh-23709
    arr1 = SparseArray([-0.17387645482451206, 0.3414148016424936])
    arr2 = SparseArray([-0.17387645482451206, 0.3414148016424937])

    if kwargs.get("check_exact", False):
        msg = """\
ExtensionArray are different

ExtensionArray values are different \\(50\\.0 %\\)
\\[left\\]:  \\[-0\\.17387645482.*, 0\\.341414801642.*\\]
\\[right\\]: \\[-0\\.17387645482.*, 0\\.341414801642.*\\]"""

        with pytest.raises(AssertionError, match=msg):
            tm.assert_extension_array_equal(arr1, arr2, **kwargs)
    else:
        tm.assert_extension_array_equal(arr1, arr2, **kwargs)

