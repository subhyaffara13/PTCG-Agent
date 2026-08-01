
def test_replace_moar(any_string_dtype):
    # PR #1179
    ser = Series(
        ["A", "B", "C", "Aaba", "Baca", "", np.nan, "CABA", "dog", "cat"],
        dtype=any_string_dtype,
    )

    result = ser.str.replace("A", "YYY")
    expected = Series(
        ["YYY", "B", "C", "YYYaba", "Baca", "", np.nan, "CYYYBYYY", "dog", "cat"],
        dtype=any_string_dtype,
    )
    tm.assert_series_equal(result, expected)

    result = ser.str.replace("A", "YYY", case=False)
    expected = Series(
        [
            "YYY",
            "B",
            "C",
            "YYYYYYbYYY",
            "BYYYcYYY",
            "",
            np.nan,
            "CYYYBYYY",
            "dog",
            "cYYYt",
        ],
        dtype=any_string_dtype,
    )
    tm.assert_series_equal(result, expected)

    result = ser.str.replace("^.a|dog", "XX-XX ", case=False, regex=True)
    expected = Series(
        [
            "A",
            "B",
            "C",
            "XX-XX ba",
            "XX-XX ca",
            "",
            np.nan,
            "XX-XX BA",
            "XX-XX ",
            "XX-XX t",
        ],
        dtype=any_string_dtype,
    )
    tm.assert_series_equal(result, expected)

