
def test_resample_interpolate_irregular_sampling(all_1d_no_arg_interpolation_methods):
    pytest.importorskip("scipy")
    # GH#21351
    ser = Series(
        np.linspace(0.0, 1.0, 5),
        index=DatetimeIndex(
            [
                "2000-01-01 00:00:03",
                "2000-01-01 00:00:22",
                "2000-01-01 00:00:24",
                "2000-01-01 00:00:31",
                "2000-01-01 00:00:39",
            ]
        ),
    )

    # Resample to 5 second sampling and interpolate with the given method
    ser_resampled = ser.resample("5s").interpolate(all_1d_no_arg_interpolation_methods)

    # Check that none of the resampled values are NaN, except the first one
    # which lies 3 seconds before the first actual data point
    assert np.isnan(ser_resampled.iloc[0])
    assert not ser_resampled.iloc[1:].isna().any()

