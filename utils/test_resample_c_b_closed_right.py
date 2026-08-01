
def test_resample_c_b_closed_right(freq: str, unit):
    # https://github.com/pandas-dev/pandas/issues/55281
    dti = date_range(start="2020-01-31", freq="1min", periods=6000, unit=unit)
    df = DataFrame({"ts": dti}, index=dti)
    grouped = df.resample(freq, closed="right")
    result = grouped.last()

    exp_dti = DatetimeIndex(
        [
            datetime(2020, 1, 30),
            datetime(2020, 1, 31),
            datetime(2020, 2, 3),
            datetime(2020, 2, 4),
        ],
        freq=freq,
    ).as_unit(unit)
    expected = DataFrame(
        {
            "ts": [
                datetime(2020, 1, 31),
                datetime(2020, 2, 3),
                datetime(2020, 2, 4),
                datetime(2020, 2, 4, 3, 59),
            ]
        },
        index=exp_dti,
    ).astype(f"M8[{unit}]")
    tm.assert_frame_equal(result, expected)

