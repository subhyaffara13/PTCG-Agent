
def test_multiindex():
    # Test the multiindex mentioned as the use-case in the documentation

    def _make_df_from_data(data):
        rows = {}
        for date in data:
            for level in data[date]:
                rows[(date, level[0])] = {"A": level[1], "B": level[2]}

        df = pd.DataFrame.from_dict(rows, orient="index")
        df.index.names = ("Date", "Item")
        return df

    rng = np.random.default_rng(2)
    ndates = 100
    nitems = 20
    dates = pd.date_range("20130101", periods=ndates, freq="D")
    items = [f"item {i}" for i in range(nitems)]

    multiindex_data = {}
    for date in dates:
        nitems_for_date = nitems - rng.integers(0, 12)
        levels = [
            (item, rng.integers(0, 10000) / 100, rng.integers(0, 10000) / 100)
            for item in items[:nitems_for_date]
        ]
        levels.sort(key=lambda x: x[1])
        multiindex_data[date] = levels

    df = _make_df_from_data(multiindex_data)
    result = df.groupby("Date", as_index=False).nth(slice(3, -3))

    sliced = {date: values[3:-3] for date, values in multiindex_data.items()}
    expected = _make_df_from_data(sliced)

    tm.assert_frame_equal(result, expected)

