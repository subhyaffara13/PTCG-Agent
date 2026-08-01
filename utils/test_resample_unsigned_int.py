
def test_resample_unsigned_int(any_unsigned_int_numpy_dtype, unit):
    # gh-43329
    df = DataFrame(
        index=date_range(start="2000-01-01", end="2000-01-03 23", freq="12h").as_unit(
            unit
        ),
        columns=["x"],
        data=[0, 1, 0] * 2,
        dtype=any_unsigned_int_numpy_dtype,
    )
    df = df.loc[(df.index < "2000-01-02") | (df.index > "2000-01-03"), :]

    result = df.resample("D").max()

    expected = DataFrame(
        [1, np.nan, 0],
        columns=["x"],
        index=date_range(start="2000-01-01", end="2000-01-03 23", freq="D").as_unit(
            unit
        ),
    )
    tm.assert_frame_equal(result, expected)

