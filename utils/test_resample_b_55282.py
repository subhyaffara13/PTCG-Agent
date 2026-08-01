
def test_resample_b_55282(unit):
    # https://github.com/pandas-dev/pandas/issues/55282
    dti = date_range("2023-09-26", periods=6, freq="12h", unit=unit)
    ser = Series([1, 2, 3, 4, 5, 6], index=dti)
    result = ser.resample("B", closed="right", label="right").mean()

    exp_dti = DatetimeIndex(
        [
            datetime(2023, 9, 26),
            datetime(2023, 9, 27),
            datetime(2023, 9, 28),
            datetime(2023, 9, 29),
        ],
        freq="B",
    ).as_unit(unit)
    expected = Series(
        [1.0, 2.5, 4.5, 6.0],
        index=exp_dti,
    )
    tm.assert_series_equal(result, expected)

