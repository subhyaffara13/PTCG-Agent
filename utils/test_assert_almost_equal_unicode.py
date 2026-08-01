
def test_assert_almost_equal_unicode():
    # see gh-20503
    msg = """numpy array are different

numpy array values are different \\(33\\.33333 %\\)
\\[left\\]:  \\[á, à, ä\\]
\\[right\\]: \\[á, à, å\\]"""

    with pytest.raises(AssertionError, match=msg):
        tm.assert_almost_equal(np.array(["á", "à", "ä"]), np.array(["á", "à", "å"]))

