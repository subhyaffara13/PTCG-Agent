
def test_apply_function_index_return(function):
    # GH: 22541
    df = DataFrame([1, 2, 2, 2, 1, 2, 3, 1, 3, 1], columns=["id"])
    result = df.groupby("id").apply(function)
    expected = Series(
        [Index([0, 4, 7, 9]), Index([1, 2, 3, 5]), Index([6, 8])],
        index=Index([1, 2, 3], name="id"),
    )
    tm.assert_series_equal(result, expected)

