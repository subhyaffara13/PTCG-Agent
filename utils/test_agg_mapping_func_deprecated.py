
def test_agg_mapping_func_deprecated():
    # GH 53325
    df = DataFrame({"x": [1, 2, 3]})

    def foo1(x, a=1, c=0):
        return x + a + c

    def foo2(x, b=2, c=0):
        return x + b + c

    # single func already takes the vectorized path
    result = df.agg(foo1, 0, 3, c=4)
    expected = df + 7
    tm.assert_frame_equal(result, expected)

    result = df.agg([foo1, foo2], 0, 3, c=4)
    expected = DataFrame(
        [[8, 8], [9, 9], [10, 10]], columns=[["x", "x"], ["foo1", "foo2"]]
    )
    tm.assert_frame_equal(result, expected)

    # TODO: the result below is wrong, should be fixed (GH53325)
    result = df.agg({"x": foo1}, 0, 3, c=4)
    expected = DataFrame([2, 3, 4], columns=["x"])
    tm.assert_frame_equal(result, expected)


def test_agg_mapping_func_deprecated():
    # GH 53325
    s = Series([1, 2, 3])

    def foo1(x, a=1, c=0):
        return x + a + c

    def foo2(x, b=2, c=0):
        return x + b + c

    s.agg(foo1, 0, 3, c=4)
    s.agg([foo1, foo2], 0, 3, c=4)
    s.agg({"a": foo1, "b": foo2}, 0, 3, c=4)

