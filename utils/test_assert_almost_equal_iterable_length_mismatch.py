
def test_assert_almost_equal_iterable_length_mismatch():
    msg = """Iterable are different

Iterable length are different
\\[left\\]:  2
\\[right\\]: 3"""

    with pytest.raises(AssertionError, match=msg):
        tm.assert_almost_equal([1, 2], [3, 4, 5])

