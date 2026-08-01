
def test_groupby_string_dtype():
    # GH 40148
    df = DataFrame({"str_col": ["a", "b", "c", "a"], "num_col": [1, 2, 3, 2]})
    df["str_col"] = df["str_col"].astype("string")
    expected = DataFrame(
        {
            "str_col": [
                "a",
                "b",
                "c",
            ],
            "num_col": [1.5, 2.0, 3.0],
        }
    )
    expected["str_col"] = expected["str_col"].astype("string")
    grouped = df.groupby("str_col", as_index=False)
    result = grouped.mean()
    tm.assert_frame_equal(result, expected)

