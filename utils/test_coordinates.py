
def test_coordinates(temp_hdfstore):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )

    store = temp_hdfstore
    store.append("df", df)

    # all
    c = store.select_as_coordinates("df")
    assert (c.values == np.arange(len(df.index))).all()

