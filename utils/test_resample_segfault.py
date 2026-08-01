
def test_resample_segfault(unit):
    # GH 8573
    # segfaulting in older versions
    all_wins_and_wagers = [
        (1, datetime(2013, 10, 1, 16, 20), 1, 0),
        (2, datetime(2013, 10, 1, 16, 10), 1, 0),
        (2, datetime(2013, 10, 1, 18, 15), 1, 0),
        (2, datetime(2013, 10, 1, 16, 10, 31), 1, 0),
    ]

    df = DataFrame.from_records(
        all_wins_and_wagers, columns=("ID", "timestamp", "A", "B")
    ).set_index("timestamp")
    df.index = df.index.as_unit(unit)
    result = df.groupby("ID").resample("5min").sum()
    expected = df.groupby("ID").apply(lambda x: x.resample("5min").sum())
    tm.assert_frame_equal(result, expected)

