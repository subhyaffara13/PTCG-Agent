
def test_map_same_length_inference_bug():
    s = Series([1, 2])

    def f(x):
        return (x, x + 1)

    s = Series([1, 2, 3])
    result = s.map(f)
    expected = Series([(1, 2), (2, 3), (3, 4)])
    tm.assert_series_equal(result, expected)

    s = Series(["foo,bar"])
    result = s.map(lambda x: x.split(","))
    expected = Series([("foo", "bar")])
    tm.assert_series_equal(result, expected)

