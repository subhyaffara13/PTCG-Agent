
def test_resample_ms_closed_right(unit):
    # https://github.com/pandas-dev/pandas/issues/55271
    dti = date_range(start="2020-01-31", freq="1min", periods=6000, unit=unit)
    df = DataFrame({"ts": dti}, index=dti)
    grouped = df.resample("MS", closed="right")
    result = grouped.last()
    exp_dti = DatetimeIndex(
        [datetime(2020, 1, 1), datetime(2020, 2, 1)], freq="MS"
    ).as_unit(unit)
    expected = DataFrame(
        {"ts": [datetime(2020, 2, 1), datetime(2020, 2, 4, 3, 59)]},
        index=exp_dti,
    ).astype(f"M8[{unit}]")
    tm.assert_frame_equal(result, expected)

