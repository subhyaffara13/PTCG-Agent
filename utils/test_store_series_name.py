
def test_store_series_name(temp_hdfstore):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    series = df["A"]

    temp_hdfstore["series"] = series
    recons = temp_hdfstore["series"]
    tm.assert_series_equal(recons, series)

