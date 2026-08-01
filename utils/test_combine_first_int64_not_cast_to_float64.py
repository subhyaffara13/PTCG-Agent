
def test_combine_first_int64_not_cast_to_float64():
    # GH 28613
    df_1 = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_2 = DataFrame({"A": [1, 20, 30], "B": [40, 50, 60], "C": [12, 34, 65]})
    result = df_1.combine_first(df_2)
    expected = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [12, 34, 65]})
    tm.assert_frame_equal(result, expected)

