
def test_resample_dtype_preservation(unit):
    # GH 12202
    # validation tests for dtype preservation

    df = DataFrame(
        {
            "date": date_range(start="2016-01-01", periods=4, freq="W").as_unit(unit),
            "group": [1, 1, 2, 2],
            "val": Series([5, 6, 7, 8], dtype="int32"),
        }
    ).set_index("date")

    result = df.resample("1D").ffill()
    assert result.val.dtype == np.int32

    result = df.groupby("group").resample("1D").ffill()
    assert result.val.dtype == np.int32

