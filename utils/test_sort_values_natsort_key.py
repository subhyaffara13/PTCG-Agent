
def test_sort_values_natsort_key():
    # GH#56081
    def split_convert(s):
        return tuple(int(x) for x in s.split("."))

    idx = pd.Index(["1.9", "2.0", "1.11", "1.10"])
    expected = pd.Index(["1.9", "1.10", "1.11", "2.0"])
    result = idx.sort_values(key=lambda x: tuple(map(split_convert, x)))
    tm.assert_index_equal(result, expected)

