
def test_searchsorted_gh31533():
    n = 100_000
    # all > 15 bytes -> arena
    values = [f"{i:020d}" for i in range(n)]
    haystack = np.array(values, dtype="T")
    # a handful of needles -> tiny arena
    needle_values = values[:: n // 23]
    expected = np.searchsorted(
        np.array(values, dtype="U20"), np.array(needle_values, dtype="U20")
    )

    needles = np.array(needle_values, dtype="T")
    assert_array_equal(np.searchsorted(haystack, needles), expected)
    assert_array_equal(
        np.searchsorted(haystack, needles, sorter=np.arange(n)), expected
    )

