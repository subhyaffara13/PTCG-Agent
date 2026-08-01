
def test_agg_split_object_part_datetime():
    # https://github.com/pandas-dev/pandas/pull/31616
    df = DataFrame(
        {
            "A": pd.date_range("2000", periods=4),
            "B": ["a", "b", "c", "d"],
            "C": [1, 2, 3, 4],
            "D": ["b", "c", "d", "e"],
            "E": pd.date_range("2000", periods=4),
            "F": [1, 2, 3, 4],
        }
    ).astype(object)
    result = df.groupby([0, 0, 0, 0]).min()
    expected = DataFrame(
        {
            "A": [pd.Timestamp("2000")],
            "B": ["a"],
            "C": [1],
            "D": ["b"],
            "E": [pd.Timestamp("2000")],
            "F": [1],
        },
        index=np.array([0]),
        dtype=object,
    )
    tm.assert_frame_equal(result, expected)

