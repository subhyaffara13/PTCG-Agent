
def test_groupby_resample_interpolate_with_apply_syntax_off_grid(groupy_test_df):
    """Similar test as test_groupby_resample_interpolate_with_apply_syntax but
    with resampling that results in missing anchor points when interpolating.
    See GH#21351."""
    # GH#21351
    result = groupy_test_df.groupby("volume").apply(
        lambda x: x.resample("265h").interpolate(method="linear")
    )

    volume = [50, 50, 60]
    week_starting = pd.DatetimeIndex(
        [
            Timestamp("2018-01-07"),
            Timestamp("2018-01-18 01:00:00"),
            Timestamp("2018-01-14"),
        ]
    ).as_unit("ns")
    expected_ind = pd.MultiIndex.from_arrays(
        [volume, week_starting],
        names=["volume", "week_starting"],
    )

    expected = DataFrame(
        data={"price": [10.0, 9.5, 11.0]},
        index=expected_ind,
    )
    tm.assert_frame_equal(result, expected, check_names=False)

