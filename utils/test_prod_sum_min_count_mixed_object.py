
def test_prod_sum_min_count_mixed_object():
    # https://github.com/pandas-dev/pandas/issues/41074
    df = DataFrame([1, "a", True])

    result = df.prod(axis=0, min_count=1, numeric_only=False)
    expected = Series(["a"], dtype=object)
    tm.assert_series_equal(result, expected)

    msg = re.escape("unsupported operand type(s) for +: 'int' and 'str'")
    with pytest.raises(TypeError, match=msg):
        df.sum(axis=0, min_count=1, numeric_only=False)

