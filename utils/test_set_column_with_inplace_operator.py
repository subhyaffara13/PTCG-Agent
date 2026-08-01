
def test_set_column_with_inplace_operator():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    # this should not raise any warning
    with tm.assert_produces_warning(None):
        df["a"] += 1

    # when it is not in a chain, then it should produce a warning
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    ser = df["a"]
    ser += 1

