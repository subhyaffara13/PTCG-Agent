
def test_invalid_filtering(temp_hdfstore):
    # can't use more than one filter (atm)

    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )

    temp_hdfstore.put("df", df, format="table")

    msg = "unable to collapse Joint Filters"
    # not implemented
    with pytest.raises(NotImplementedError, match=msg):
        temp_hdfstore.select("df", "columns=['A'] | columns=['B']")

    # in theory we could deal with this
    with pytest.raises(NotImplementedError, match=msg):
        temp_hdfstore.select("df", "columns=['A','B'] & columns=['C']")

