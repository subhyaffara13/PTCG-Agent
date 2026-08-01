
def test_assert_almost_equal_shape_mismatch_override():
    msg = """Index are different

Index shapes are different
\\[left\\]:  \\(2L*,\\)
\\[right\\]: \\(3L*,\\)"""
    with pytest.raises(AssertionError, match=msg):
        tm.assert_almost_equal(np.array([1, 2]), np.array([3, 4, 5]), obj="Index")

