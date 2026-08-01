
def test_invalid_terms(temp_hdfstore):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    df["string"] = "foo"
    df.loc[df.index[0:4], "string"] = "bar"

    temp_hdfstore.put("df", df, format="table")

    # some invalid terms
    msg = re.escape("__init__() missing 1 required positional argument: 'where'")
    with pytest.raises(TypeError, match=msg):
        Term()

    # more invalid
    msg = re.escape(
        "cannot process expression [df.index[3]], "
        "[2000-01-06 00:00:00] is not a valid condition"
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.select("df", "df.index[3]")

    msg = "invalid syntax"
    with pytest.raises(SyntaxError, match=msg):
        temp_hdfstore.select("df", "index>")

