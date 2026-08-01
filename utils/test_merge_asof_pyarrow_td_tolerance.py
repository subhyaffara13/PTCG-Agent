
def test_merge_asof_pyarrow_td_tolerance():
    # GH 56486
    ser = pd.Series(
        [datetime.datetime(2023, 1, 1)], dtype="timestamp[us, UTC][pyarrow]"
    )
    df = pd.DataFrame(
        {
            "timestamp": ser,
            "value": [1],
        }
    )
    result = merge_asof(df, df, on="timestamp", tolerance=Timedelta("1s"))
    expected = pd.DataFrame(
        {
            "timestamp": ser,
            "value_x": [1],
            "value_y": [1],
        }
    )
    tm.assert_frame_equal(result, expected)

