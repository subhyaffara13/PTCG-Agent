
def test_assert_index_equal_mixed_dtype():
    # GH#39168
    idx = Index(["foo", "bar", 42])
    tm.assert_index_equal(idx, idx, check_order=False)

