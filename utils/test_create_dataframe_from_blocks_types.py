
def test_create_dataframe_from_blocks_types():
    df = pd.DataFrame(
        {
            "int": list(range(1, 4)),
            "uint": np.arange(3, 6).astype("uint8"),
            "float": [2.0, np.nan, 3.0],
            "bool": np.array([True, False, True]),
            "boolean": pd.array([True, False, None], dtype="boolean"),
            "string": list("abc"),
            "datetime": pd.date_range("20130101", periods=3),
            "datetimetz": pd.date_range("20130101", periods=3).tz_localize(
                "Europe/Brussels"
            ),
            "timedelta": pd.timedelta_range("1 day", periods=3),
            "period": pd.period_range("2012-01-01", periods=3, freq="D"),
            "categorical": pd.Categorical(["a", "b", "a"]),
            "interval": pd.IntervalIndex.from_tuples([(0, 1), (1, 2), (3, 4)]),
        }
    )

    result = create_dataframe_from_blocks(
        [(block.values, block.mgr_locs.as_array) for block in df._mgr.blocks],
        index=df.index,
        columns=df.columns,
    )
    tm.assert_frame_equal(result, df)

