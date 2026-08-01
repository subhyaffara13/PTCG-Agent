
def test_numpy_array_equal_unicode():
    # see gh-20503
    #
    # Test ensures that `tm.assert_numpy_array_equals` raises the right
    # exception when comparing np.arrays containing differing unicode objects.
    msg = """numpy array are different

numpy array values are different \\(33\\.33333 %\\)
\\[left\\]:  \\[á, à, ä\\]
\\[right\\]: \\[á, à, å\\]"""

    with pytest.raises(AssertionError, match=msg):
        tm.assert_numpy_array_equal(
            np.array(["á", "à", "ä"]), np.array(["á", "à", "å"])
        )

