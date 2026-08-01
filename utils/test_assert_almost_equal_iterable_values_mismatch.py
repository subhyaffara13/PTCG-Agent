
def test_assert_almost_equal_iterable_values_mismatch():
    msg = """Iterable are different

Iterable values are different \\(50\\.0 %\\)
\\[left\\]:  \\[1, 2\\]
\\[right\\]: \\[1, 3\\]"""

    with pytest.raises(AssertionError, match=msg):
        tm.assert_almost_equal([1, 2], [1, 3])

