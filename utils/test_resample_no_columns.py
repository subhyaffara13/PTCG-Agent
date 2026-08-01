
def test_resample_no_columns():
    # GH#52484
    df = DataFrame(
        index=Index(
            pd.to_datetime(
                ["2018-01-01 00:00:00", "2018-01-01 12:00:00", "2018-01-02 00:00:00"]
            ),
            name="date",
        )
    )
    result = df.groupby([0, 0, 1]).resample(rule=pd.to_timedelta("06:00:00")).mean()
    index = pd.to_datetime(
        [
            "2018-01-01 00:00:00",
            "2018-01-01 06:00:00",
            "2018-01-01 12:00:00",
            "2018-01-02 00:00:00",
        ]
    )
    expected = DataFrame(
        index=pd.MultiIndex(
            levels=[np.array([0, 1], dtype=np.intp), index],
            codes=[[0, 0, 0, 1], [0, 1, 2, 3]],
            names=[None, "date"],
        )
    )

    # GH#52710 - Index comes out as 32-bit on 64-bit Windows
    tm.assert_frame_equal(result, expected, check_index_type=not is_platform_windows())

