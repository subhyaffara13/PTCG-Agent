
def test_concat_series_between_empty_and_tzaware_series(using_infer_string):
    tzaware_time = pd.Timestamp("2020-01-01T00:00:00+00:00")
    ser1 = Series(index=[tzaware_time], data=0, dtype=float)
    ser2 = Series(dtype=float)

    result = pd.concat([ser1, ser2], axis=1)
    expected = pd.DataFrame(
        data=[
            (0.0, None),
        ],
        index=[tzaware_time]
        if using_infer_string
        else pd.Index([tzaware_time], dtype=object),
        columns=[0, 1],
        dtype=float,
    )
    tm.assert_frame_equal(result, expected)

