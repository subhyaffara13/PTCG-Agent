
def test_concat_float_datetime64():
    # GH#32934
    df_time = DataFrame({"A": pd.array(["2000"], dtype="datetime64[ns]")})
    df_float = DataFrame({"A": pd.array([1.0], dtype="float64")})

    expected = DataFrame(
        {
            "A": [
                pd.array(["2000"], dtype="datetime64[ns]")[0],
                pd.array([1.0], dtype="float64")[0],
            ]
        },
        index=[0, 0],
    )
    result = concat([df_time, df_float])
    tm.assert_frame_equal(result, expected)

    expected = DataFrame({"A": pd.array([], dtype="object")})
    result = concat([df_time.iloc[:0], df_float.iloc[:0]])
    tm.assert_frame_equal(result, expected)

    expected = DataFrame({"A": pd.array([1.0], dtype="object")})
    result = concat([df_time.iloc[:0], df_float])
    tm.assert_frame_equal(result, expected)

    expected = DataFrame({"A": pd.array(["2000"], dtype="datetime64[ns]")}).astype(
        object
    )

    result = concat([df_time, df_float.iloc[:0]])
    tm.assert_frame_equal(result, expected)

