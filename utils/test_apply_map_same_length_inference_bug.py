
def test_apply_map_same_length_inference_bug():
    s = Series([1, 2])

    def f(x):
        return (x, x + 1)

    result = s.apply(f, by_row="compat")
    expected = s.map(f)
    tm.assert_series_equal(result, expected)

