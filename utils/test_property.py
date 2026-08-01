
def test_property() -> None:
    # https://github.com/pandas-dev/pandas/pull/63439
    df = pd.DataFrame({"a": [1, 2, 3]})
    expr = pd.col("a").index
    expected_str = "col('a').index"

    assert str(expr) == expected_str

    result = df.assign(b=expr)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [0, 1, 2]})
    tm.assert_frame_equal(result, expected)

