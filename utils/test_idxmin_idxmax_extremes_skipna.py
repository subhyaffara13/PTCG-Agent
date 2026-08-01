
def test_idxmin_idxmax_extremes_skipna(skipna, how, float_numpy_dtype):
    # GH#57040
    min_value = np.finfo(float_numpy_dtype).min
    max_value = np.finfo(float_numpy_dtype).max
    df = DataFrame(
        {
            "a": Series(np.repeat(range(1, 5), repeats=2), dtype="intp"),
            "b": Series(
                [
                    np.nan,
                    min_value,
                    np.nan,
                    max_value,
                    min_value,
                    np.nan,
                    max_value,
                    np.nan,
                ],
                dtype=float_numpy_dtype,
            ),
        },
    )
    gb = df.groupby("a")

    if not skipna:
        msg = f"{how} with skipna=False"
        with pytest.raises(ValueError, match=msg):
            getattr(gb, how)(skipna=skipna)
        return
    result = getattr(gb, how)(skipna=skipna)
    expected = DataFrame(
        {"b": [1, 3, 4, 6]}, index=pd.Index(range(1, 5), name="a", dtype="intp")
    )
    tm.assert_frame_equal(result, expected)

